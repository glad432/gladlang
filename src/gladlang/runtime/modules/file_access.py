"""Safely reads a module's source text: rejects symlinks, enforces the size limit, and validates UTF-8."""

import os
from pathlib import Path

from gladlang.core.errors import RuntimeError
from gladlang.core.util.settings import Settings
from gladlang.runtime.runtime_result import RuntimeResult


def read_module_source(module_path, position_start, position_end, error_context):
    result = RuntimeResult()

    if Path(module_path).is_symlink():
        return result.failure(
            RuntimeError(
                position_start,
                position_end,
                f"Access denied: '{module_path}' is a symbolic link",
                error_context,
            )
        )

    if not os.path.isfile(module_path):
        return result.failure(
            RuntimeError(
                position_start,
                position_end,
                f"Module not found: '{module_path}'",
                error_context,
            )
        )

    try:
        try:
            file_descriptor = os.open(
                module_path,
                os.O_RDONLY | os.O_NOFOLLOW,
            )
        except AttributeError:
            file_descriptor = os.open(module_path, os.O_RDONLY)

    except OSError as error:
        return result.failure(
            RuntimeError(
                position_start,
                position_end,
                f"Could not open module '{module_path}': {error.strerror}",
                error_context,
            )
        )

    try:
        file_size = os.fstat(file_descriptor).st_size

        if file_size > Settings.MAX_SOURCE_BYTES:
            os.close(file_descriptor)
            return result.failure(
                RuntimeError(
                    position_start,
                    position_end,
                    f"Module too large: '{module_path}' "
                    f"({file_size:,} bytes, maximum "
                    f"{Settings.MAX_SOURCE_BYTES:,})",
                    error_context,
                )
            )

        with os.fdopen(
            file_descriptor,
            "r",
            encoding="utf-8",
        ) as module_file:
            return result.success(module_file.read())

    except UnicodeDecodeError:
        return result.failure(
            RuntimeError(
                position_start,
                position_end,
                f"Module is not valid UTF-8: '{module_path}'",
                error_context,
            )
        )

    except OSError as error:
        return result.failure(
            RuntimeError(
                position_start,
                position_end,
                f"Could not read module '{module_path}': {error.strerror}",
                error_context,
            )
        )
