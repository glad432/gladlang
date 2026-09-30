"""Parser mixin for IMPORT ... FROM "..." statements (named, aliased, and namespace imports)."""

from gladlang.core.constants import GL_IDENTIFIER, GL_KEYWORD, GL_MUL, GL_STRING
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.ast import ImportNode
from gladlang.parser.parse_result import ParseResult


class StatementsModuleImport:
    def _parse_import_statement(self):
        result = ParseResult()
        position_start = self.current_token.position_start.copy()
        result.register_advancement()
        self.advance()

        if self.current_token.type == GL_MUL:
            import_names = [result.register(self._parse_namespace_import())]
        else:
            import_names = result.register(self._parse_named_imports())

        if result.error:
            return result

        if not self.current_token.matches(GL_KEYWORD, "FROM"):
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected 'FROM'",
                )
            )

        result.register_advancement()
        self.advance()

        if self.current_token.type != GL_STRING:
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected a string literal module path after 'FROM'",
                )
            )

        source_token = self.current_token
        result.register_advancement()
        self.advance()

        return result.success(
            ImportNode(
                import_names,
                source_token,
                position_start,
                source_token.position_end,
            )
        )

    def _parse_namespace_import(self):
        result = ParseResult()
        result.register_advancement()
        self.advance()

        if not self.current_token.matches(GL_KEYWORD, "AS"):
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected 'AS' after '*'",
                )
            )

        result.register_advancement()
        self.advance()

        if self.current_token.type != GL_IDENTIFIER:
            return result.failure(
                InvalidSyntaxError(
                    self.current_token.position_start,
                    self.current_token.position_end,
                    "Expected namespace identifier",
                )
            )

        import_alias = self.current_token.value
        result.register_advancement()
        self.advance()

        return result.success(("namespace", None, import_alias))
