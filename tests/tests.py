import unittest
import sys
from PIL import Image
import importlib
sys.path.insert(1,'../')
community_file = importlib.import_module('community-version', None)


class Testing(unittest.TestCase):

    def test_1_colorText(self):
        text = 'test'
        def_output = community_file.colorText(text)
        self.assertIs(type(def_output), str)


if __name__ == '__main__':
    unittest.main()
