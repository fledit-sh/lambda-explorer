from __future__ import annotations

"""Project version information."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("lambda-explorer")
except PackageNotFoundError:  # pragma: no cover - package not installed
    __version__ = "0.0.3"
