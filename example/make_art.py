# this project requires Pillow installation: https://pillow.readthedocs.io/en/stable/installation.html

# code credit goes to: https://www.hackerearth.com/practice/notes/beautiful-python-a-simple-ascii-art-generator-from-images/
# code modified to work with Python 3 by @aneagoie
from PIL import Image

import os
import sys

ASCII_CHARS = [ '#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']

ASCII_CHARS = ['#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']


image_file_path = sys.argv[1]

def save_ascii_art(image_ascii_art):
    """
    saving the ascii art 
    """
    try:
        image_output_folder = sys.argv[2]
        file_path = os.path.split(image_file_path)[1]
        file_name = os.path.splitext(file_path)[0]

        if not os.path.exists(image_output_folder):
            os.makedirs(image_output_folder)

        with open(f"{image_output_folder}/{file_name}.txt", mode='w') as my_file:
            my_file.write(image_ascii_art)
    except ValueError:
        print('please check image is converted to image ascii art.')


def scale_image(image, new_width=100):
    """Resizes an image preserving the aspect ratio.
    """
    (original_width, original_height) = image.size
    aspect_ratio = original_height/float(original_width)
    new_height = int(aspect_ratio * new_width)

    new_image = image.resize((new_width, new_height), Image.ANTIALIAS)

    return new_image


def convert_to_grayscale(image):
    return image.convert('L')


def map_pixels_to_ascii_chars(image, range_width=25):
    """Maps each pixel to an ascii char based on the range
    in which it lies.

    0-255 is divided into 11 ranges of 25 pixels each.
    """

    pixels_in_image = list(image.getdata())
    pixels_to_chars = [ASCII_CHARS[int(pixel_value/range_width)] for pixel_value in
                       pixels_in_image]

    return "".join(pixels_to_chars)


def convert_image_to_ascii(image, new_width=100):
    image = scale_image(image)
    image = convert_to_grayscale(image)

    pixels_to_chars = map_pixels_to_ascii_chars(image)
    len_pixels_to_chars = len(pixels_to_chars)

    image_ascii = [pixels_to_chars[index: index + new_width] for index in
                   range(0, len_pixels_to_chars, new_width)]

    image_ascii_art = "\n".join(image_ascii)

    save_ascii_art(image_ascii_art)

    return image_ascii_art


def handle_image_conversion(image_filepath):
    image = None
    try:
        image = Image.open(image_filepath)
    except Exception as e:
        print(f"Unable to open image file {image_filepath}.")
        print(e)
        return

    image_ascii = convert_image_to_ascii(image)
    print(image_ascii)


if __name__=='__main__':


if __name__ == '__main__':
    import sys


    print(image_file_path)
    handle_image_conversion(image_file_path)


