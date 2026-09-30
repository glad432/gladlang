"""Resolves an IMPORT source string to an absolute path confined to the module root."""

import os

from gladlang.core.errors import RuntimeError
from gladlang.runtime.runtime_result import RuntimeResult


def resolve_module_path(
    source_path,
    importing_directory,
    module_root,
    position_start,
    position_end,
    error_context,
):
    result = RuntimeResult()

    if not isinstance(source_path, str) or source_path == "":
        return result.failure(
            RuntimeError(
                position_start,
                position_end,
                "Import path must be a non-empty string",
                error_context,
            )
        )

    if "\x00" in source_path:
        return result.failure(
            RuntimeError(
                position_start,
                position_end,
                "Invalid import path",
                error_context,
            )
        )

    if os.path.isabs(source_path):
        return result.failure(
            RuntimeError(
                position_start,
                position_end,
                "Absolute import paths are not allowed",
                error_context,
            )
        )

    if not source_path.lower().endswith(".glad"):
        return result.failure(
            RuntimeError(
                position_start,
                position_end,
                f"Import path '{source_path}' must point to a '.glad' file",
                error_context,
            )
        )

    module_root_path = os.path.realpath(module_root)
    candidate_path = os.path.normpath(os.path.join(importing_directory, source_path))

    if not os.path.exists(candidate_path):
        return result.failure(
            RuntimeError(
                position_start,
                position_end,
                f"Module not found: '{candidate_path}'",
                error_context,
            )
        )

    real_candidate_path = os.path.realpath(candidate_path)

    try:
        common_path = os.path.commonpath([module_root_path, real_candidate_path])
    except ValueError:
        common_path = None

    if common_path != module_root_path:
        return result.failure(
            RuntimeError(
                position_start,
                position_end,
                f"Import path '{source_path}' escapes the module root",
                error_context,
            )
        )

    cache_key = os.path.relpath(
        candidate_path,
        module_root_path,
    ).replace(os.sep, "/")

    return result.success((candidate_path, cache_key))
