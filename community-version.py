#!/usr/bin/python3
## Community Version
"""This is class SIMPLEcmd"""

import os
from PIL import Image
import cmd
from example.make_art import convert_image_to_ascii


def is_image_file(path_to_file):
    """
    This function checks if the the file is valid image
    """
    if not os.path.isabs(path_to_file):
        path_to_file = os.path.abspath(path_to_file)

    try:
        with Image.open(path_to_file) as img:
            return True
    except Exception as not_image:
        return False


class SimpleCmd(cmd.Cmd):
    """this is command interpreter class"""
    prompt = "(hackfest) "

    def do_quit(self, arg):
        """This method exit the program"""
        return True

    def do_EOF(self, arg):
        """Exits the program without crashing"""
        print()
        return True

    def helf_quit(self):
        """This is quit method help message"""
        print("Quit command to exit the program\n")

    def do_ascii(self, args):
        """
        converts images to 
        
        convert image to ascii
        Usage: ascii  <image_file_path>
        Example: ascii image.jpg

        when creating multiple images
        Usage: ascii <image_file_path> <image_file_path> <image_file_path>
        Example: ascii imgege1.png image2.png image3.png
        """

        if not args:
            print("** Image missing **")
            return
        all_images = args.split()

        
        def create_many_instances(file):
            
            if is_image_file(file):
                try:
                    with Image.open(file) as image:
                        ascii_img = convert_image_to_ascii(image)
                    print()
                    print(ascii_img)
                    print()
                    print()

                except Exception as e:
                    print("Error occured!", e)
                    return
            else:
                print()
                print(f"{file} is not a valid image file")
                return

        if len(all_images) < 2:
            create_many_instances(all_images[0])
        elif len(all_images) > 1:
            for image in all_images:
                create_many_instances(image)


if __name__ == "__main__":
    SimpleCmd().cmdloop()

## Community Version

# this project requires Pillow installation: https://pillow.readthedocs.io/en/stable/installation.html

# code credit goes to: https://www.hackerearth.com/practice/notes/beautiful-python-a-simple-ascii-art-generator-from-images/
# code modified to work with Python 3 by @aneagoie

from PIL import Image
from tkinter import Tk, filedialog

ASCII_CHARS = ["#", "?", "%", ".", "S", "+", ".", "*", ":", ",", "@"]

def scale_image(image, new_width=100):
    """Resizes an image preserving the aspect ratio."""
    (original_width, original_height) = image.size
    aspect_ratio = original_height / float(original_width)
    new_height = int(aspect_ratio * new_width)

    new_image = image.resize((new_width, new_height))
    return new_image

def convert_to_grayscale(image):
    return image.convert('L')

def map_pixels_to_ascii_chars(image, make_silhouette=False, range_width=25):
    """Maps each pixel to an ascii char based on the range
    in which it lies.

    0-255 is divided into 11 ranges of 25 pixels each.
    """

    pixels_in_image = list(image.getdata())

    if make_silhouette:
        pixels_in_image = [x[3] for x in image.getdata()]

    pixels_to_chars = [ASCII_CHARS[int(pixel_value/range_width)] for pixel_value in
                       pixels_in_image]

    return "".join(pixels_to_chars)


def convert_image_to_ascii(image, make_silhouette=False, new_width=100):
    image = scale_image(image)
    image = convert_to_grayscale(image)

	if not make_silhouette:
		image = convert_to_grayscale(image)  # PIL image
    pixels_to_chars = map_pixels_to_ascii_chars(image, make_silhouette)
    len_pixels_to_chars = len(pixels_to_chars)

    image_ascii = [
        pixels_to_chars[index : index + new_width]
        for index in range(0, len_pixels_to_chars, new_width)
    ]

    return "\n".join(image_ascii)

def handle_image_conversion(image_filepath, make_silhouette):
    image = None
    try:
        image = Image.open(image_filepath)
    except Exception as e:

        print(
            "Unable to open image file {image_filepath}.".format(
                image_filepath=image_filepath
            )
        )
        print(e)
        return

    image_ascii = convert_image_to_ascii(image)
    print(image_ascii)

def get_image_path():
    """Open a file dialog to select an image and return its path."""
    root = Tk()
    root.withdraw()  # Hide the root window

    file_path = filedialog.askopenfilename()
    root.destroy()  # Destroy the root window after selection

    return file_path

if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--path", help="path to image file", required=True)
    parser.add_argument("-s", "--silhouette",
                        help="Make ASCII silhouette", required=False)
    args = parser.parse_args()
    make_silhouette = False
    image_file_path = args.path

	""" use file dialog if no arguments are passed """
	if len(sys.argv < 2):
		image_file_path = get_image_path()

    if len(sys.argv) > 2:
        if args.silhouette is not None:
            make_silhouette = args.silhouette.lower() in [
                'true', 'yes', 'y', 't']
    
    print(image_file_path)
    handle_image_conversion(image_file_path, make_silhouette)
