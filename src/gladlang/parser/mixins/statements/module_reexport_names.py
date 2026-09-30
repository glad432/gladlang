"""Parser helper for parsing the comma separated name (AS alias)? list in standalone EXPORT."""

from gladlang.core.constants import GL_COMMA, GL_IDENTIFIER, GL_KEYWORD
from gladlang.core.errors import InvalidSyntaxError
from gladlang.parser.parse_result import ParseResult


class StatementsReExportNames:
    def _parse_reexport_names(self):
        result = ParseResult()
        re_export_names = []

        while True:
            if self.current_token.type != GL_IDENTIFIER:
                return result.failure(
                    InvalidSyntaxError(
                        self.current_token.position_start,
                        self.current_token.position_end,
                        "Expected identifier",
                    )
                )

            local_name = self.current_token.value
            exported_name = local_name
            position_end = self.current_token.position_end

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
                            "Expected an export alias identifier after 'AS'",
                        )
                    )

                exported_name = self.current_token.value
                position_end = self.current_token.position_end
                result.register_advancement()
                self.advance()

            re_export_names.append((local_name, exported_name))

            if self.current_token.type != GL_COMMA:
                break

            result.register_advancement()
            self.advance()

        return result.success((re_export_names, position_end))
