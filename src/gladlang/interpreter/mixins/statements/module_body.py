"""Interpreter helper that runs a claimed module's body and cleans up cache/event/thread state."""

import os

from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult


class InterpreterModuleBody:
    def _load_module_body(
        self, absolute_path, cache_key, position_start, context, state
    ):
        result = RuntimeResult()
        module = self.modules.get(cache_key)
        state.push(module, os.path.dirname(absolute_path))
        try:
            error = self._execute_module(
                absolute_path, cache_key, context, position_start
            )
        except Exception as exception:
            error = RuntimeError(
                position_start,
                position_start,
                f"Unexpected error while loading module '{cache_key}': {exception}",
                context,
            )
        finally:
            state.pop()
            state.loading_modules.discard(cache_key)

        if error is not None:
            self.modules.discard(cache_key)

        with self._module_events_lock:
            event = self._module_events.pop(cache_key, None)

        if event is not None:
            event.set()

        if error is not None:
            return result.failure(error)

        return result.success(module)
