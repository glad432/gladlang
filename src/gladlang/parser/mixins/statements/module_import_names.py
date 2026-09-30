"""Parser helper for parsing the comma separated name (AS alias)? list in IMPORT statements."""

from gladlang.core.constants import GL_COMMA, GL_IDENTIFIER, GL_KEYWORD
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.parse_result import ParseResult


class StatementsImportNames:
    def _parse_named_imports(self):
        result = ParseResult()
        import_names = []

        while True:
            if self.current_token.type != GL_IDENTIFIER:
                return result.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        "Expected identifier",
                    )
                )

            import_name = self.current_token.value
            import_alias = import_name
            result.register_advancement()
            self.advance()

            if self.current_token.matches(GL_KEYWORD, "AS"):
                result.register_advancement()
                self.advance()

                if self.current_token.type != GL_IDENTIFIER:
                    return result.failure(
                        InvalidSyntaxError(
                            self.current_token.position_start,
                            self.current_token.position_end,
                            "Expected alias identifier after 'AS'",
                        )
                    )

                import_alias = self.current_token.value
                result.register_advancement()
                self.advance()

            import_names.append(("named", import_name, import_alias))

            if self.current_token.type != GL_COMMA:
                break

            result.register_advancement()
            self.advance()

        return result.success(import_names)
