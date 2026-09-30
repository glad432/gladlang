"""Interpreter construction: dispatch cache, instruction budget, binary operator table."""

import os
from threading import RLock
from gladlang.core.util.locking import NoLock
from gladlang.core.util.settings import Settings
from gladlang.runtime.modules.cache import ModuleCache
from gladlang.runtime.modules.thread_state import ModuleThreadState


class InterpreterCore:
    def __init__(self, instruction_limit=None, module_root=None):
        self.dispatch_cache = {}
        self.instruction_limit = instruction_limit
        self._binary_operator_dispatch = self._build_binary_operator_dispatch()
        self.module_root = os.path.normpath(
            os.path.abspath(module_root) if module_root else os.getcwd()
        )

        self.modules = ModuleCache(threading_enabled=Settings.THREADING_ENABLED)
        self._module_thread_state = ModuleThreadState(self.module_root)
        self._module_events = {}
        self._module_events_lock = RLock() if Settings.THREADING_ENABLED else NoLock()
