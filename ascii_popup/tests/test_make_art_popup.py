import unittest
from PIL import Image

from ascii_popup.make_art_popup import validate_font_input, validate_width_input, scale_image
class TestMakeArtPopup(unittest.TestCase):
    def test_validate_font_input_is_valid_and_true(self):
        """Test that validate_font_input value is True and coverts string to integer """
        font_string = "2"
        result, valid_font_input = validate_font_input(font_string)
        self.assertTrue(result)
        self.assertEqual(valid_font_input, 2)

    def test_validate_font_input_is_invalid_and_false(self):
        """Test that validate_font_input value is False and string with text won't convert to integer"""
        font_string = "abc"
        result, valid_font_input = validate_font_input(font_string)
        self.assertFalse(result)
        self.assertIsNone(valid_font_input)

    def test_validate_font_input_is_out_of_range_and_false(self):
        """Test that validate_font_input value is False and integer is outside of range"""
        font_string = "10"
        result, valid_font_input = validate_font_input(font_string)
        self.assertFalse(result)
        self.assertIsNone(valid_font_input)

    def test_validate_width_input_is_valid_and_true(self):
        """Test that validate_width_input value is True and coverts string to integer """
        width_string = "100"
        result, valid_width_input = validate_width_input(width_string)
        self.assertTrue(result)
        self.assertEqual(valid_width_input, 100)

    def test_validate_width_input_is_invalid_and_false(self):
        """Test that validate_font_input value is False and string with text won't convert to integer"""
        width_string = "abc"
        result, valid_width_input = validate_font_input(width_string)
        self.assertFalse(result)
        self.assertIsNone(valid_width_input)

    def test_scale_image_scales_height_to_suit_new_width(self):
        """Test that checks if scale_image converts the new values mathematically correct against the correct values """
        test_image = Image.new('RGB', (100, 200))
        new_width = 100
        character_aspect_ratio = .6
        scaled_image = scale_image(test_image, new_width, character_aspect_ratio)
        self.assertEqual(scaled_image.size[0], new_width)
        self.assertEqual(scaled_image.size[1], int(new_width * (200 / 100) * .6))

if __name__ == '__main__':
    unittest.main()
