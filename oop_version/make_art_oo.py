# this project requires Pillow installation: https://pillow.readthedocs.io/en/stable/installation.html
# code credit goes to: https://www.hackerearth.com/practice/notes/beautiful-python-a-simple-ascii-art-generator-from-images/
# code modified to work with Python 3 by @aneagoie

import os
import sys
from PIL import Image

# Global Variables
OUT_FILE_PATH = "./output_images/"

ASCII_CHARS = ['#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']

HELP_MSG = """
Usage  : python community-version.py [option] [input_file]
Options:
         no options will run the default ASCII_CHARS
    -r   reverse the ASCII_CHARS
    -s   save the output to file (by default the output file is [input_file]_output.txt)
    -rs  save the reversed output to file
"""

FILE_ERROR_MSG = """
File type of [input_file] not valid, please make sure it is of type PNG.
"""


class ConvertImageToASCII:

    def __init__(self, file_path=None, option='-c'):
        """ Default file_path is None and option to use is -c """
        self.image_file_path = file_path
        self.option = option

    def scale_image(self, image, new_width=100):
        """Resizes an image preserving the aspect ratio.
        """
        (original_width, original_height) = image.size
        aspect_ratio = original_height / float(original_width)
        new_height = int(aspect_ratio * new_width)
        new_image = image.resize((new_width, new_height))
        return new_image

    def convert_to_grayscale(self, image):
        return image.convert('L')

    def map_pixels_to_ascii_chars(self, image, range_width=25):
        """Maps each pixel to an ascii char based on the range
        in which it lies.
        0-255 is divided into 11 ranges of 25 pixels each.
        """
        global ASCII_CHARS
        pixels_in_image = list(image.getdata())
        pixels_to_chars = [ASCII_CHARS[int(pixel_value / range_width)] for pixel_value in
                           pixels_in_image]

        return "".join(pixels_to_chars)

    def convert_image_to_ascii(self, image, new_width=100):
        image = self.scale_image(image)
        image = self.convert_to_grayscale(image)

        pixels_to_chars = self.map_pixels_to_ascii_chars(image)
        len_pixels_to_chars = len(pixels_to_chars)

        image_ascii = [pixels_to_chars[index: index + new_width] for index in
                       range(0, len_pixels_to_chars, new_width)]
        return "\n".join(image_ascii)

    def map_option_to_convert(self, image):
        """ Make to appropriate option provided to convert image """
        converted_image = self._defaultConversion(image)
        if 'r' in self.option:
            converted_image = self._reverseASCIIConversion(image)
        if 's' in self.option:
            self._saveConvertedImage(converted_image)
        return converted_image

    def _defaultConversion(self, image):
        default_ascii_image = self.convert_image_to_ascii(image)
        return default_ascii_image

    def _reverseASCIIConversion(self, image):
        """ Make method to convert image with reverse ASCII charactes """
        return self.convert_image_to_ascii(image)  # replace this with your reversed ascii image conversion

    def _createOutFilePath(self, file_name):
        """ Create out file path if not exists and return filepath """
        global OUT_FILE_PATH
        if not os.path.exists(OUT_FILE_PATH):
            os.mkdir(OUT_FILE_PATH)
        file_path = OUT_FILE_PATH + file_name
        return file_path

    def _saveConvertedImage(self, image):
        """ Save converted image as a text file """
        global OUT_FILE_PATH
        partition_file_path = self.image_file_path.split('/')
        output_file_name = partition_file_path[-1]
        output_file_name = output_file_name.split('.')[0] + "_output.txt"

        output_file_path = self._createOutFilePath(output_file_name)
        try:
            with open(output_file_path, 'w') as out_file:
                out_file.write(image)
            print(f"Image (as a text) saved to -> {output_file_path}")
            return output_file_path
        except Exception as e:
            print("An error occured while saving image as a text file !")
            print(e)
            return False

    def handle_image_conversion(self):
        try:
            image = Image.open(self.image_file_path)
        except Exception as e:
            print(f"Unable to open image file {self.image_file_path}.")
            print(e)
            return

        return self.map_option_to_convert(image)


def check_file(f):
    """ Check file type, it should be png (as of now) """
    global HELP_MSG
    allowed_inputs_file = ["png"]
    try:
        if f.split('.')[-1] in allowed_inputs_file:
            return True
        else:
            return False
    except Exception:
        print(HELP_MSG)
        return False


def get_cli_input():
    """ Check if program running through command line """
    cli_input = [inp for inp in sys.argv]
    input_file = cli_input[-1]
    input_option = '-c'
    is_file_type_correct = check_file(input_file)
    if len(cli_input) > 2:
        input_option = cli_input[1]
    return is_file_type_correct, input_file, input_option


if __name__ == '__main__':
    isFile, cli_input_file, cli_input_option = get_cli_input()
    print(f"File {cli_input_file} is PNG ? {isFile}, called with option {cli_input_option} (-c is default)")
    if not isFile:
        print(HELP_MSG)
        raise Exception(FILE_ERROR_MSG)
    ascii_convert_obj = ConvertImageToASCII(file_path=cli_input_file, option=cli_input_option)
    print(ascii_convert_obj.handle_image_conversion())
