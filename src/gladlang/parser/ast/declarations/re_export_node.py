"""ReExportNode – represents standalone EXPORT name [AS alias], ... re‑exports."""


class ReExportNode:
    def __init__(self, re_export_names, position_start, position_end):
        self.re_export_names = re_export_names
        self.position_start = position_start
        self.position_end = position_end
