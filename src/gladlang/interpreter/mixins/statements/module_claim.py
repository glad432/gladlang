"""Interpreter module loader: resolves, claims, waits for, or re‑uses a module cache entry."""

import threading

from gladlang.core.errors import RuntimeError
from gladlang.core.util.settings import Settings
from gladlang.runtime.modules.path_security import resolve_module_path
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.module import Module


class InterpreterModuleClaim:
    def _load_module(self, source, position_start, position_end, context):
        result = RuntimeResult()
        state = self._module_thread_state
        resolved = result.register(
            resolve_module_path(
                source,
                state.current_directory,
                self.module_root,
                position_start,
                position_end,
                context,
            )
        )

        if result.error:
            return result

        absolute_path, cache_key = resolved
        if state.depth >= Settings.MAX_IMPORT_DEPTH:
            return result.failure(
                RuntimeError(
                    position_start,
                    position_end,
                    f"Maximum import depth exceeded ({Settings.MAX_IMPORT_DEPTH})",
                    context,
                )
            )

        module, event = self._claim_module(cache_key, state)
        if module is not None:
            return result.success(module)

        if event is not None:
            finished = event.wait(timeout=Settings.MAX_MODULE_WAIT_SECONDS)
            if not finished:
                return result.failure(
                    RuntimeError(
                        position_start,
                        position_end,
                        f"Timed out waiting for module '{source}' to finish loading on another thread",
                        context,
                    )
                )

            module = self.modules.get(cache_key)
            if module is None:
                return result.failure(
                    RuntimeError(
                        position_start,
                        position_end,
                        f"Failed to load module '{source}'",
                        context,
                    )
                )

            return result.success(module)

        return self._load_module_body(
            absolute_path, cache_key, position_start, context, state
        )

    def _claim_module(self, cache_key, state):
        with self._module_events_lock:
            if cache_key in state.loading_modules:
                return self.modules.get(cache_key), None

            event = self._module_events.get(cache_key)
            if event is not None:
                return None, event

            cached = self.modules.get(cache_key)
            if cached is not None:
                return cached, None

            self._module_events[cache_key] = threading.Event()
            module = Module(cache_key)
            self.modules.put(cache_key, module)
            state.loading_modules.add(cache_key)
            return None, None
