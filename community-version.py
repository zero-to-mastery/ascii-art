#!/usr/bin/python3
"""This is the SIMPLEcmd class for ASCII art conversion."""

import os
import sys

import self
from PIL import Image
import cmd
from tkinter import Tk, filedialog
import argparse

from example.convertartpython3 import handle_image_conversion

ASCII_CHARS = ["#", "?", "%", ".", "S", "+", ".", "*", ":", ",", "@"]


class ImageToAsciiConverter:
    def __init__(self, new_width=100, brightness=1.0):
        self.new_width = new_width
        self.brightness = brightness

    @staticmethod
    def scale_image(image):
        """Resize an image preserving the aspect ratio."""
        (original_width, original_height) = image.size
        aspect_ratio = original_height / float(original_width)
        new_height = int(aspect_ratio * self.new_width)
        new_image = image.resize((self.new_width, new_height))
        return new_image

    @staticmethod
    def convert_to_grayscale(image):
        """Convert an image to grayscale."""
        return image.convert('L')

    @staticmethod
    def map_pixels_to_ascii_chars(image, make_silhouette=False, range_width=25):
        """Map pixel values to ASCII characters based on a specified range and brightness."""
        pixels_in_image = list(image.getdata())
        if make_silhouette:
            pixels_in_image = [m[3] for m in image.getdata()]
        adjusted_pixels = [int(pixel * self.brightness) for pixel in pixels_in_image]
        pixels_to_chars = [ASCII_CHARS[min(int(pixel_value / range_width), len(ASCII_CHARS) - 1)] for pixel_value in
                           adjusted_pixels]
        return "".join(pixels_to_chars)

    def convert_image_to_ascii(self, image, make_silhouette=False):
        """Convert an image to ASCII art with adjustable brightness."""
        image = self.scale_image(image)
        if not make_silhouette:
            image = self.convert_to_grayscale(image)
        pixels_to_chars = self.map_pixels_to_ascii_chars(image, make_silhouette=make_silhouette)
        len_pixels_to_chars = len(pixels_to_chars)
        image_ascii = [pixels_to_chars[index: index + self.new_width] for index in
                       range(0, len_pixels_to_chars, self.new_width)]
        return "\n".join(image_ascii)


def is_image_file(path_to_file):
    """Check if the file is a valid image."""
    if not os.path.isabs(path_to_file):
        path_to_file = os.path.abspath(path_to_file)

    try:
        with Image.open(path_to_file) as img:
            return True
    except Exception as not_image:
        return False


class SimpleCmd(cmd.Cmd):
    prompt = "(hackfest) "

    def do_quit(self, arg):
        """Exit the program."""
        return True

    def do_EOF(self, arg):
        """Exit the program without crashing."""
        print()
        return True

    def help_quit(self):
        """Display help message for the quit command."""
        print("Quit command to exit the program\n")

    def do_ascii(self, args):
        """
        Convert images to ASCII art.

        Usage: ascii <image_file_path>
        Example: ascii image.jpg

        When creating multiple images:
        Usage: ascii <image_file_path> <image_file_path> ...
        Example: ascii image1.png image2.png image3.png
        """
        if not args:
            print("** Image missing **")
            return
        all_images = args.split()

        for image_path in all_images:
            self.process_image(image_path)

    def process_image(self, image_path):
        if is_image_file(image_path):
            try:
                with Image.open(image_path) as image:
                    ascii_img = self.converter.convert_image_to_ascii(image)
                print()
                print(ascii_img)
                print()
                print()
            except Exception as e:
                print("Error occurred!", e)
        else:
            print()
            print(f"{image_path} is not a valid image file")


def get_image_path():
    """Open a file dialog to select an image and return its path."""
    root = Tk()
    root.withdraw()  # Hide the root window

    file_path = filedialog.askopenfilename()
    root.destroy()  # Destroy the root window after selection

    if not file_path:
        print("No file selected. Exiting.")
        sys.exit()

    return file_path


def main():
    parser = argparse.ArgumentParser(description="Convert images to ASCII art.")
    parser.add_argument("-i", "--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("-f", "--file", help="Image file path")
    parser.add_argument("-s", "--silhouette", help="Make ASCII silhouette", action="store_true", default=False)
    parser.add_argument("-o", "--output", help="Output file and path")
    parser.add_argument("-b", "--brightness", help="Alter brightness of image (e.g., -b 1.0)")

    args = parser.parse_args()

    if args.interactive:
        converter = ImageToAsciiConverter()
        SimpleCmd(converter).cmdloop()
    else:
        if args.file is None or (args.file == "-s"):
            image_path = get_image_path()
        else:
            image_path = args.file

        converter = ImageToAsciiConverter(brightness=float(args.brightness) if args.brightness else 1.0)
        handle_image_conversion(image_path)


if __name__ == '__main__':
    main()
