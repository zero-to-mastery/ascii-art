import pytest

from ascii_art import ascii_art


def test_1_colorText():
    text = 'test'
    def_output = ascii_art.colorText(text)
    assert type(def_output) is str


def test_2_is_supported():
    path = '../ztm-logo.png'
    def_output = ascii_art.is_supported(path)
    assert def_output


def test_3_is_supported():
    bad_path = '.ztm-logo'
    def_output = ascii_art.is_supported(bad_path)
    assert not def_output


def test_4_check_file():
    path = '../ztm-logo.png'
    def_output = ascii_art.check_file(path)
    assert def_output is None


def test_5_write_file():
    def_output = ascii_art.write_file('test', 'test')
    assert def_output


def test_6_write_file():
    def_output = ascii_art.write_file('', 'test')
    assert not def_output


def test_7_write_file():
    with pytest.raises(TypeError):
        ascii_art.write_file('')


def test_8_output_name():
    assert type(ascii_art.output_name('test')) is str


def test_9_output_name():
    with pytest.raises(TypeError):
        ascii_art.output_name()


def test_10_all_supported_files():
    assert type(ascii_art.all_supported_files()) is list


def test_ascii_chars():
    ASCII_CHARS = ['#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']
    assert ASCII_CHARS == ascii_art.ASCII_CHARS


def test_color_options():
    COLOR_OPTIONS = ['black', 'blue', 'cyan', 'green', 'magenta', 'red', 'white', 'yellow']
    assert COLOR_OPTIONS == ascii_art.COLOR_OPTIONS


def test_supported_image_types():
    SUPPORTED_IMAGE_TYPES = ('.png', '.jpeg', '.jpg')
    assert SUPPORTED_IMAGE_TYPES == ascii_art.SUPPORTED_IMAGE_TYPES
