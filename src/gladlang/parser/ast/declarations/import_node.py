"""ImportNode – represents IMPORT statements (named, aliased, or namespace imports)."""


class ImportNode:
    def __init__(self, import_names, source_token, position_start, position_end):
        self.import_names = import_names
        self.source_token = source_token
        self.position_start = position_start
        self.position_end = position_end
