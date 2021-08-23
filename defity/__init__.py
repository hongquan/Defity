# The actual implementation is in Rust code. Here is a thin wrapper layer
# to provide type annotations and allow broader input data type.

from typing import Union, IO, AnyStr
import io
from pathlib import Path

from .defity import __version__  # noqa: F401
from . import defity as _mod


CHUNK_SIZE = 2048


def from_file(file: Union[Path, str, IO]) -> str:
    """Return mimetype of a file, from its path."""
    # The Rust function receives a PathBuf, not &str, but PyO3 will
    # automatically convert for us.
    # See: https://github.com/PyO3/pyo3/blob/0.14/src/conversions/path.rs#L16
    if not isinstance(file, (Path, str, io.RawIOBase, io.BufferedIOBase, io.TextIOBase)):
        raise TypeError('Input object must be a file path or file-like object')
    if isinstance(file, (Path, str)):
        return _mod.from_file(str(file))
    # File-like object
    # Make sure to read from the beginning of file.
    if file.seekable():
        file.seek(0)
    chunk: AnyStr = file.read(CHUNK_SIZE)
    if file.seekable():
        file.seek(0)
    return _mod.from_bytes(chunk.encode() if isinstance(chunk, str) else chunk)


def from_bytes(buf: bytes) -> str:
    """Return mimetype from content in form of bytes-like type."""
    if not isinstance(buf, (bytes, bytearray, memoryview)):
        raise TypeError('Data must be of bytes, bytearray or memoryview type')
    # We accept many input data types just for user's convenience. We still convert
    # it to immutable bytes to pass down to Rust function.
    return _mod.from_bytes(bytes(buf))
