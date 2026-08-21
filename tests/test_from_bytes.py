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
    zeros = b"\0" * 1000
    mime = defity.from_bytes(zeros)
    assert mime == 'application/octet-stream'
    assert defity.is_bytes_of_type(zeros, 'application/octet-stream')
