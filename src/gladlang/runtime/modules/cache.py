"""ModuleCache – LRU‑evicting store of loaded Module values, guarded by a thread‑safe lock."""

from collections import OrderedDict
from threading import RLock
from gladlang.core.util.locking import NoLock
from gladlang.core.util.settings import Settings


class ModuleCache:
    def __init__(self, threading_enabled=True):
        self._module_cache = OrderedDict()
        self._cache_lock = RLock() if threading_enabled else NoLock()

    def __contains__(self, module_path):
        with self._cache_lock:
            return module_path in self._module_cache

    def get(self, module_path):
        with self._cache_lock:
            module_value = self._module_cache.get(module_path)
            if module_value is not None:
                self._module_cache.move_to_end(module_path)

            return module_value

    def put(self, module_path, module_value):
        with self._cache_lock:
            self._module_cache[module_path] = module_value
            self._module_cache.move_to_end(module_path)
            while len(self._module_cache) > Settings.MAX_MODULE_CACHE:
                self._module_cache.popitem(last=False)

    def discard(self, module_path):
        with self._cache_lock:
            self._module_cache.pop(module_path, None)

    def __len__(self):
        with self._cache_lock:
            return len(self._module_cache)
