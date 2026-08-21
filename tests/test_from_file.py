import tempfile
import os
import io
from pathlib import Path

import pytest
import defity


DATA = Path(__file__).parent / 'data'
# This file can be copied from Windows, we are not allowed to redistribute it here
UNRECOGNIZED_FILE = DATA / 'mib.bin'


def test_from_path():
    filepath = DATA / 'image.png'
    mime = defity.from_file(filepath)
    assert mime == 'image/png'


def test_from_string_path():
    filepath = str(DATA / 'image.png')
    mime = defity.from_file(filepath)
    assert mime == 'image/png'


def test_from_opened_file():
    filepath = Path(__file__).parent.parent / 'skunk.svg'
    with filepath.open() as f:
        mime = defity.from_file(f)
    assert mime == 'image/svg+xml'


def test_from_in_memory_binary_stream():
    original = (DATA / 'image.png').read_bytes()
    floating = io.BytesIO(original)
    mime = defity.from_file(floating)
    assert mime == 'image/png'


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        filepath = DATA / 'not-exist.jpg'
        defity.from_file(filepath)


def test_passing_directory():
    assert defity.from_file(DATA) == "inode/directory"


@pytest.mark.skipif(not hasattr(Path, "chmod"), reason=f'Path.chmod needs to be available')
@pytest.mark.skipif(os.geteuid() == 0, reason=f'Cannot run this test as root')
def test_file_permisson():
    with tempfile.TemporaryDirectory() as tmp_dir:
        filepath = Path(tmp_dir) / "test.txt"

        assert filepath.write_bytes(b"Hallo, Welt!")

        filepath.chmod(0)  # disable reading

        with pytest.raises(PermissionError):
            defity.from_file(filepath)

        filepath.unlink()

    assert not Path(tmp_dir).exists()


@pytest.mark.skipif(not Path(UNRECOGNIZED_FILE).exists(),
                    reason=f'Please copy a Windows file to {UNRECOGNIZED_FILE}')
def test_unrecognized_file():
    """Test that a general MIME type "application/octet-stream" is always returned for
    unknown file."""
    mime = defity.from_file(UNRECOGNIZED_FILE)
    assert mime == 'application/octet-stream'
