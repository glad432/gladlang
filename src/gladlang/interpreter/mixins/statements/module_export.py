"""Interpreter visitor for EXPORT statements – runs the declaration and records it as a module export."""

from gladlang.runtime.runtime_result import RuntimeResult


class InterpreterModuleExport:
    def visit_ExportNode(self, node, context):
        result = RuntimeResult()
        error = self._check_export_allowed(node, context)
        if error is not None:
            return result.failure(error)

        value = result.register(self.visit(node.declaration_node, context))
        if result.error:
            return result

        current_module = self._module_thread_state.current_module
        current_module.exports[node.exported_name] = value
        return result.success(value)
