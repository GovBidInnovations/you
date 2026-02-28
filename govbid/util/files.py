"""File utility functions."""

from __future__ import annotations

from pathlib import Path


def require_file(path: Path, hint: str = "") -> None:
    """Ensure that the specified file exists.

    Args:
        path: Path to the required file.
        hint: Optional hint message to include in the exception.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not path.exists():
        msg = f"Required file missing: {path}"
        if hint:
            msg += f"\nHint: {hint}"
        raise FileNotFoundError(msg)
