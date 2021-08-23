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
