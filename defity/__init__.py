from typing import Union
from pathlib import Path

from .defity import __version__  # noqa: F401

from . import defity as _mod


# The actual implementation is in Rust code, but that form of extension
# doesn't support Python type annotations yet, so we add a shortcut
# here with type annotations.

def from_file(path: Union[Path, str]) -> str:
    """Return mimetype of a file, from its path."""
    # The Rust function receives a PathBuf, not &str, but PyO3 will
    # automatically convert for us.
    # See: https://github.com/PyO3/pyo3/blob/0.14/src/conversions/path.rs#L16
    return _mod.from_file(str(path))
