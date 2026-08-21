from pathlib import Path

import defity


DATA = Path(__file__).parent / 'data'


def test_from_bytes():
    img_file = DATA / 'image.png'
    mime = defity.from_bytes(img_file.read_bytes())
    assert mime == 'image/png'


def test_from_bytearray():
    img_file = Path(__file__).parent.parent / 'skunk.svg'
    mime = defity.from_bytes(bytearray(img_file.read_bytes()))
    assert mime == 'image/svg+xml'


def test_all_zeros():
    """Test that a general MIME type "application/octet-stream" is always returned for
    unknown file."""
    mime = defity.from_bytes(b"\0" * 1000)
    assert mime == 'application/octet-stream'
