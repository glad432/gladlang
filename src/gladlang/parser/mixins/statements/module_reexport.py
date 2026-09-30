"""Parser mixin for standalone EXPORT name [AS alias], ... re-export statements."""

from gladlang.parser.ast import ReExportNode
from gladlang.parser.parse_result import ParseResult


class StatementsReExport:
    def _parse_reexport_statement(self, position_start):
        result = ParseResult()
        re_export_names, position_end = result.register(self._parse_reexport_names())

        if result.error:
            return result

        return result.success(
            ReExportNode(
                re_export_names,
                position_start,
                position_end,
            )
        )
