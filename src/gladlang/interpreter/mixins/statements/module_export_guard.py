"""Shared guard for EXPORT statements: disallows in REPL and outside modules, and enforces top‑level placement."""

from gladlang.core.errors import RuntimeError


class InterpreterModuleExportGuard:
    def _check_export_allowed(self, node, context):
        current_module = self._module_thread_state.current_module
        if context.is_repl:
            return RuntimeError(
                node.position_start,
                node.position_end,
                "EXPORT is not allowed in REPL mode",
                context,
            )

        if current_module is None:
            return RuntimeError(
                node.position_start,
                node.position_end,
                "EXPORT can only be used inside a module",
                context,
            )

        if context.display_name != f"<module {current_module.name}>":
            return RuntimeError(
                node.position_start,
                node.position_end,
                "EXPORT must appear at the top level of a module (not inside functions, classes, loops, or conditionals)",
                context,
            )

        return None
