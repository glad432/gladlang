"""ModuleThreadState – per-thread import stack (directory, module) and set of modules being loaded."""

import threading


class ModuleThreadState:
    def __init__(self, module_root):
        self._local = threading.local()
        self._module_root = module_root

    def _stack(self):
        if not hasattr(self._local, "stack"):
            self._local.stack = [(None, self._module_root)]
            self._local.loading_modules = set()

        return self._local.stack

    @property
    def current_module(self):
        return self._stack()[-1][0]

    @property
    def current_directory(self):
        return self._stack()[-1][1]

    @property
    def depth(self):
        return len(self._stack()) - 1

    @property
    def loading_modules(self):
        self._stack()
        return self._local.loading_modules

    def push(self, module, directory):
        self._stack().append((module, directory))

    def pop(self):
        self._stack().pop()
