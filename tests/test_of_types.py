from pathlib import Path

import defity


DATA = Path(__file__).parent / 'data'


def test_single_type():
    filepath = DATA / 'image.png'
    mime = 'image/png'
    matched = defity.is_file_of_type(filepath, mime)
    assert matched


def test_not_match_single_type():
    filepath = DATA / 'image.png'
    mime = 'image/jpeg'
    matched = defity.is_file_of_type(filepath, mime)
    assert not matched


def test_multiple_types():
    filepath = DATA / 'image.png'
    mimes = ('image/png', 'application/pdf')
    matched = defity.is_file_of_type(filepath, mimes)
    assert matched


def test_not_match_multiple_types():
    filepath = DATA / 'image.png'
    mimes = ('image/jpeg', 'application/pdf')
    matched = defity.is_file_of_type(filepath, mimes)
    assert not matched


def test_file_multiple_types():
    filepath = DATA / 'image.png'
    mimes = ('image/png', 'application/pdf')
    with filepath.open('rb') as f:
        matched = defity.is_file_of_type(f, mimes)
    assert matched


def test_bytes_multiple_types():
    filepath = DATA / 'image.png'
    mimes = ('image/png', 'application/pdf')
    matched = defity.is_bytes_of_type(filepath.read_bytes(), mimes)
    assert matched


def test_svg_matches_multiple_types():
    svg_file = Path(__file__).parent.parent / 'skunk.svg'
    svg_bytes = svg_file.read_bytes()

    for mime in ('image/svg+xml', 'text/plain', 'text/xml', 'application/octet-stream'):
        assert defity.is_file_of_type(svg_file, mime)
        assert defity.is_bytes_of_type(svg_bytes, mime)
