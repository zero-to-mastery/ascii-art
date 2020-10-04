import unittest
import sys
from PIL import Image
import importlib
sys.path.insert(1,'../')
community_file = importlib.import_module('community-version', None)


class Testing(unittest.TestCase):

    def test_0_color_change(self):
        def_output = community_file.color_change()
        self.assertIs(def_output, "none")

    def test_1_check_inputs(self):
        def_output = community_file.check_inputs()
        help_msg = community_file.help_msg
        self.assertIs(def_output, "")

    def test_2_colorText(self):
        text = 'test'
        def_output = community_file.colorText(text)
        self.assertIs(type(def_output), str)


if __name__ == '__main__':
    unittest.main()
