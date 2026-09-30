"""Interpreter visitor for standalone EXPORT – re‑exports an already‑declared local name."""

from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult
from gladlang.values.primitives.number import Number


class InterpreterModuleReExport:
    def visit_ReExportNode(self, node, context):
        result = RuntimeResult()
        error = self._check_export_allowed(node, context)
        if error is not None:
            return result.failure(error)

        current_module = self._module_thread_state.current_module
        for local_name, exported_name in node.re_export_names:
            value = context.symbol_table.get(local_name)
            if value is None:
                return result.failure(
                    RuntimeError(
                        node.position_start,
                        node.position_end,
                        f"'{local_name}' is not defined",
                        context,
                    )
                )

            current_module.exports[exported_name] = value

        return result.success(Number.null.copy())
