"""Module – runtime representation of a loaded GladLang module (cache entry)."""

from gladlang.core.errors import RuntimeError
from gladlang.values.value import Value


class Module(Value):
    __slots__ = ("name", "exports")

    def __init__(self, name):
        self.name = name
        self.exports = {}

    def is_true(self):
        return True

    def copy(self):
        from gladlang.values.module import Module

        module_copy = Module(self.name)
        module_copy.exports = self.exports
        module_copy.set_context(self.context)
        module_copy.set_position(self.position_start, self.position_end)
        return module_copy

    def get_attribute(self, name_token, context=None):
        attribute_name = name_token.value

        if attribute_name in self.exports:
            return self.exports[attribute_name], None

        return None, RuntimeError(
            name_token.position_start,
            name_token.position_end,
            f"Module '{self.name}' has no export '{attribute_name}'",
            self.context,
        )

    def set_attribute(
        self,
        name_token,
        value,
        context=None,
        visibility=None,
        as_final=False,
    ):
        return None, RuntimeError(
            name_token.position_start,
            name_token.position_end,
            f"Cannot assign to module export '{name_token.value}'",
            self.context,
        )

    def __repr__(self):
        return f"<module {self.name}>"
