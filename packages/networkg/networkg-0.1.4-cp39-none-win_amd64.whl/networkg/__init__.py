"""A graph processing library built in Rust."""

try:
    from importlib.metadata import PackageNotFoundError, version  # type: ignore
except ImportError:
    # Needed for Python<3.8 support.
    from importlib_metadata import PackageNotFoundError, version  # type: ignore

from . import graph

__all__ = ["graph"]

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "unknown"
