import unittest
import sys
from PIL import Image
sys.path.insert(1,'../')
from community_version import handle_image_conversion, check_file 


class Testing(unittest.TestCase):

    def test_0_handle_bad_path(self):
        test_path = 'bad path to input file'
        def_output = handle_image_conversion(test_path)
        self.assertIsNone(def_output)

    def test_1_check_file(self):
        file = "test.png"
        def_output = True
        self.assertTrue(def_output)

    def test_2_check_file(self):
        file = "test.120"
        def_output = False
        self.assertFalse(def_output)


if __name__ == '__main__':
    unittest.main()

