# The actual implementation is in Rust code. Here is a thin wrapper layer
# to provide type annotations and allow broader input data type.

from typing import Union, IO, AnyStr, Tuple, Any
import io
from pathlib import Path

from .defity import __version__  # noqa: F401
from . import defity as _mod


CHUNK_SIZE = 2048


def from_file(file: Union[Path, str, IO]) -> str:
    """Return MIME type of a file, from its path, or from file-like object.

    The file must be opened in binary mode.

    Example:

      >>> import defity
      >>> defity.from_file('path/to/landscape.png')
      'image/png'
      >>> with open('path/to/landscape.png', 'rb') as f:
      ...     defity.from_file(f)
      ...
      'image/png'

    """

    # The Rust function receives a PathBuf, not &str, but PyO3 will
    # automatically convert for us.
    # See: https://github.com/PyO3/pyo3/blob/0.14/src/conversions/path.rs#L16
    _guard_file_arg(file)
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
    """Return MIME type from content in form of bytes-like type.

    Example:

      >>> import defity
      >>> defity.from_bytes(b'some-binary-content')
      'image/png'

    """

    _guard_buf_arg(buf)
    # We accept many input data types just for user's convenience. We still convert
    # it to immutable bytes to pass down to Rust function.
    return _mod.from_bytes(bytes(buf))


def is_file_of_type(file: Union[Path, str, IO], mimetype: Union[str, Tuple[str, ...]]):
    """Test if given file is of one of given MIME types.

    The file must be opened in binary mode.

    Example:

      >>> import defity
      >>> defity.is_file_of_type('path/to/landscape.png', 'image/png')
      True
      >>> with open('path/to/landscape.png', 'rb') as f:
      ...     defity.from_file(f, ('image/png', 'image/jpeg', 'application/pdf'))
      ...
      True

    """

    _guard_file_arg(file)
    if isinstance(mimetype, str):
        types = (mimetype,)
    elif isinstance(mimetype, tuple) and all(isinstance(t, str) for t in mimetype):
        types = mimetype
    else:
        raise TypeError('mimetype argument must be a string or tuple of strings.')
    if isinstance(file, (Path, str)):
        return _mod.is_file_of_type(str(file), types)
    # File-like object
    # Make sure to read from the beginning of file.
    if file.seekable():
        file.seek(0)
    chunk: AnyStr = file.read(CHUNK_SIZE)
    if file.seekable():
        file.seek(0)
    return _mod.is_bytes_of_type(chunk.encode() if isinstance(chunk, str) else chunk, types)


def is_bytes_of_type(buf: bytes, mimetype: Union[str, Tuple[str, ...]]):
    """Test if given file content is of one of given MIME types."""

    _guard_buf_arg(buf)
    if isinstance(mimetype, str):
        types = (mimetype,)
    elif isinstance(mimetype, tuple) and all(isinstance(t, str) for t in mimetype):
        types = mimetype
    else:
        raise TypeError('mimetype argument must be a string or tuple of strings.')
    return _mod.is_bytes_of_type(buf, types)


def _guard_file_arg(file: Any):
    if not isinstance(file, (Path, str, io.RawIOBase, io.BufferedIOBase, io.TextIOBase)):
        raise TypeError('Input object must be a file path or file-like object')


def _guard_buf_arg(buf: Any):
    if not isinstance(buf, (bytes, bytearray, memoryview)):
        raise TypeError('Data must be of bytes, bytearray or memoryview type')
