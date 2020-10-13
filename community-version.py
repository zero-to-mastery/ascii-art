#!/usr/bin/env python3
# code credit goes to:
#   https://www.hackerearth.com/practice/notes/beautiful-python-a-simple-ascii-art-generator-from-images/
# code modified to work with Python 3 by @aneagoie
from __future__ import division

import os
import sys
import time

import click
import pyfiglet
import pyjokes
import random

from asciimatics.effects import Print, Clock
from asciimatics.exceptions import ResizeScreenError
from asciimatics.renderers import FigletText, Rainbow
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from PIL import Image
from math import ceil

# Silence pygame message. This must precede the lib import
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

ASCII_CHARS = ['#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']
ASCII_CHARS_HR = ['-', '_', '+', '<', '>', 'i', '!', 'l', 'I', '?',
                  '/', '\\', '|', '(', ')', '1', '{', '}', '[', ']',
                  'r', 'c', 'v', 'u', 'n', 'x', 'z', 'j', 'f', 't',
                  'L', 'C', 'J', 'U', 'Y', 'X', 'Z', 'O', '0', 'Q',
                  'o', 'a', 'h', 'k', 'b', 'd', 'p', 'q', 'w', 'm',
                  '*', 'W', 'M', 'B', '8', '&', '%', '$', '#', '@']
COLOR_OPTIONS = ['black', 'blue', 'cyan', 'green', 'magenta', 'red', 'white', 'yellow']
FONTS = ['alligator', 'slant', '3-d', '3x5', '5lineoblique', 'banner3-D']
SUPPORTED_IMAGE_TYPES = ('.png', '.jpeg', '.jpg')


def scale_image(image, new_width=100):
    """Resizes an image preserving the aspect ratio."""
    (original_width, original_height) = image.size
    aspect_ratio = original_height / float(original_width)
    new_height = int(aspect_ratio * new_width * 0.5)

    return image.resize((new_width, new_height), Image.ANTIALIAS)


def convert_to_grayscale(image):
    return image.convert('L')


def map_pixels_to_ascii_chars(image, reverse, highres=False):
    """Maps each pixel to an ascii char based on the range
    in which it lies.
    0-255 is divided into ranges of pixels based on the number of
    characters in ASCII_CHARS.
    """
    # We make a local copy on reverse so we don't modify the global array.
    if highres:
        ascii_chars = ASCII_CHARS_HR if not reverse else ASCII_CHARS_HR[::-1]
    else:
        ascii_chars = ASCII_CHARS if not reverse else ASCII_CHARS[::-1]

    # Calculates the ranges of pixels based on the number of characters in ascii_chars
    range_width = ceil(255/len(ascii_chars))
    pixels_in_image = list(image.getdata())
    pixels_to_chars = [
        ascii_chars[int(pixel_value / range_width)] for pixel_value in pixels_in_image]

    return "".join(pixels_to_chars)


def convert_image_to_ascii(image, reverse=False, new_width=None, highres=False):
    if not new_width:
        new_width = image.width
    image = scale_image(image, new_width)
    image = convert_to_grayscale(image)
    pixels_to_chars = map_pixels_to_ascii_chars(image, reverse, highres)

    len_pixels_to_chars = len(pixels_to_chars)

    image_ascii = [pixels_to_chars[index: index + new_width] for index in
                   range(0, len_pixels_to_chars, new_width)]

    return "\n".join(image_ascii)


def colorText(text):
    COLORS = {
        "black": "\u001b[30;1m",
        "red": "\u001b[31;1m",
        "green": "\u001b[32m",
        "yellow": "\u001b[33;1m",
        "blue": "\u001b[34;1m",
        "magenta": "\u001b[35m",
        "cyan": "\u001b[36m",
        "white": "\u001b[37m",

    }
    for color in COLORS:
        text = text.replace("[[" + color + "]]", COLORS[color])
    return text


def open_image(path: str) -> Image:
    """
    Wrapper for creation of an Image.
    We just use this to handle errors when opening the file.
    """
    try:
        return Image.open(path)
    except Exception as e:
        print(f"Unable to open image file {path}.\n{e}")
        return None


def demo(screen):
    effects = [
        Print(screen, Rainbow(screen, FigletText("Hacktoberfest")),
              y=screen.height//2 - 8),
        Print(screen, Rainbow(screen, FigletText("ASCII Art 2020")),
              y=screen.height//2 + 3),
        Clock(screen, screen.width//2, screen.height//2, screen.height//2),
    ]
    screen.play([Scene(effects, -1)], stop_on_resize=True)
    screen.refresh()


def show_clock():
    try:
        Screen.wrapper(demo)
        sys.exit(0)
    except ResizeScreenError:
        pass


def get_joke():
    return pyjokes.get_joke()


# typerwriter is the method for running the text
def typewriter(message):
    # the spaces are for format on the splash screen
    print(pyfiglet.figlet_format("   zTm ", font=random.choice(FONTS)).rstrip())
    print(pyfiglet.figlet_format("Community Presents -- "))
    print(pyfiglet.figlet_format("                           ASCII ART"))
    # print(pyfiglet.figlet_format("==> "))

    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        if char != '\n':
            time.sleep(0.1)
        else:
            time.sleep(1)


def ascii_text():
    """Converts simple text into random font ascii format text"""
    text = str(input('\n Enter The Text To Convert To Ascii-Art \n'))
    print(pyfiglet.figlet_format(text, font=random.choice(FONTS)).rstrip())


def is_supported(path):
    """
    Returns True if given path points to a supported image,
            False otherwise
    """
    if not path:
        return False
    _, ext = os.path.splitext(path)
    return ext.lower() in SUPPORTED_IMAGE_TYPES


def check_file(path):
    """
    Does validation.
    Check if the given path leads to a supported image type. It exits the program (with printed message) if
    the image is unsupported.
    """
    if not is_supported(path):
        print(f"{path} is not supported")
        print("Supported file types: ", end='')
        print(', '.join(SUPPORTED_IMAGE_TYPES))
        sys.exit(1)


def write_file(ascii, filename):
    """Write ascii text to file"""
    if not ascii or not filename:
        return False
    try:
        with open(filename, "w") as f:
            f.write(ascii)
            return True
    except:
        return False


def output_name(input):
    """
    Works out the ascii filename from the input name.
    It'll attempt to save the output in the same directory as that of the input file.
    """
    return f"{os.path.splitext(input if input else '')[0]}_output.txt"


def show_credits():
    """Show credits"""
    message = (pyjokes.get_joke())  # this is message ie the running text obtained from pyjokes library function

    pygame.mixer.init()
    pygame.mixer.music.load("typewriter.wav")
    pygame.mixer.music.play(loops=-1)
    os.system('cls')
    typewriter(message)
    pygame.mixer.music.stop()
    pygame.mixer.quit()


def all_supported_files():
    return [f for f in os.listdir() if is_supported(f)]


def set_color(image_ascii, color):
    if not color or color == 'black':
        return image_ascii
    text = f"[[{color}]]{image_ascii}[[white]]"
    return colorText(text)


def process(input_file, reverse=False, save=False, output=None, width=None, color=None, highres=False):
    """Orchestrates the conversion of a single image to ascii."""
    check_file(input_file)
    save = save or (output is not None)
    if save and not output:
        output = output_name(input_file)
    image = open_image(input_file)
    ascii_str = convert_image_to_ascii(image, reverse, width, highres)

    if save:
        if write_file(ascii_str, output):
            print(f"Image saved to -> {output}")
        else:
            print(f"Error writing to file: {output}")
    else:
        print(set_color(ascii_str, color))


@click.command()
@click.argument('input_files', type=click.Path(exists=True), nargs=-1)
@click.option('-r', '--reverse', is_flag=True, help='reverse the ASCII_CHARS')
@click.option('-s', '--save', is_flag=True,
              help='save the output to file (by default the output file is [input_file]_output.txt)')
@click.option('-o', '--output', default=None, type=click.Path(),
              help='Specify the name of the output file instead of using the default. -s is implied.')
@click.option('-w', '--width', default=100, type=int,
              help='scale the image to fit a custom width')
@click.option('--credits', is_flag=True, help="Show credits")
@click.option('--clock', is_flag=True,
              help='show clock as a colorful animation. resize the terminal or press "q" or "x" to exit the clock.')
@click.option('--all', is_flag=True, help='convert all supported files')
@click.option('-c', '--color', type=click.Choice(COLOR_OPTIONS, case_sensitive=False), default='black',
              help='Set output color')
@click.option('--text', is_flag=True, help='Convert Simple Text Into Ascii Text Format, Enter Text After Prompt')
@click.option('--types', is_flag=True, help='list supported image formats and exit.')
@click.option('-hr', '--highres', is_flag=True, help='Converts using a wide range of Ascii characters.')
def cli(input_files, reverse, save, output, width, credits, clock, all, color, text, types, highres):
    """
    Processes the command-line arguments and starts the relevant processes.
    Arguments shouldn't be accessed beyond this function.
    """
    if types:
        print(', '.join(SUPPORTED_IMAGE_TYPES))
        return
    if clock:
        show_clock()
        return
    if credits:
        show_credits()
        print()

    if all:
        input_files = all_supported_files()

    if text:
        ascii_text()
        return

    for file in input_files:
        process(file, reverse=reverse, save=save,
                output=output, width=width, color=color.lower(),highres=highres)
    if not input_files and len(sys.argv) == 0:
        print("Image not specified. Please specify image or add --help for help.")


if __name__ == '__main__':
    cli()
