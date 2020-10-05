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

    def test_2_is_supported(self):
        path = '../ztm-logo.png'
        def_output = community_file.is_supported(path)
        self.assertTrue(def_output)

    def test_3_is_supported(self):
        bad_path = '.ztm-logo'
        def_output = community_file.is_supported(bad_path)
        self.assertFalse(def_output)

    def test_4_check_file(self):
        path = '../ztm-logo.png'
        def_output = community_file.check_file(path)
        self.assertIsNone(def_output)

    def test_5_write_file(self):
        def_output = community_file.write_file('test','test')
        self.assertTrue(def_output)

    def test_6_write_file(self):
        def_output = community_file.write_file('','test')
        self.assertFalse(def_output)

    def test_7_write_file(self):
        self.assertRaises(TypeError, lambda: community_file.write_file(''))

    def test_8_output_name(self):
        self.assertIs(type(community_file.output_name('test')), str)

    def test_9_output_name(self):
        self.assertRaises(TypeError, lambda: community_file.output_name())

    def test_10_all_supported_files(self):
        self.assertIs(type(community_file.all_supported_files()),list)


if __name__ == '__main__':
    unittest.main()
