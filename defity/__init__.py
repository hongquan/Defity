from .defity import __version__  # noqa: F401

from . import defity as _mod


# The actual implementation is in Rust code, but that form of extension
# doesn't support Python type annotations yet, so we add a shortcut
# here with type annotations.

def from_file(path: str) -> str:
    """Return mimetype of a file, from its path."""
    return _mod.from_file(path)
