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
import pygame
from PIL import Image
from asciimatics.effects import Print, Clock
from asciimatics.exceptions import ResizeScreenError
from asciimatics.renderers import FigletText, Rainbow
from asciimatics.scene import Scene
from asciimatics.screen import Screen
import random

ASCII_CHARS = ['#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']
COLOR_OPTIONS = ['black', 'blue', 'cyan', 'green', 'magenta', 'red', 'white', 'yellow']
SUPPORTED_IMAGE_TYPES = ('.png', '.jpeg', '.jpg')



import pyjokes #return running random jokes at every starting of the code
help_msg = """
Usage  : python community-version.py [option] [input_file] [color]
Options:
         no options will run the default ASCII_CHARS
    -r   reverse the ASCII_CHARS
    -s   save the output to file (by default the output file is [input_file]_output.txt)
    -rs  save the reversed output to file
    
Colors:
    "black"
    "red"
    "green"
    "yellow"
    "blue"
    "magenta"
    "cyan"
    "white"
    
Or you can convert multiple images at once in current directory like this:
Usage  : python community-version.py all

You can type clock to show clock as a colorful animation:
Usage  : python community-version.py clock
< resize the terminal or press "q" or "x" to exit the clock >

    
"""

def scale_image(image, new_width=100):
    """Resizes an image preserving the aspect ratio.
    """
    (original_width, original_height) = image.size
    aspect_ratio = original_height / float(original_width)
    new_height = int(aspect_ratio * new_width)

    new_image = image.resize((new_width, new_height))
    return new_image


def convert_to_grayscale(image):
    return image.convert('L')


def map_pixels_to_ascii_chars(image, reverse, range_width=25):
        """Maps each pixel to an ascii char based on the range
        in which it lies.
        0-255 is divided into 11 ranges of 25 pixels each.
        """

        # We make a local copy on reverse so we don't modify the global array.
        ascii_chars = ASCII_CHARS if not reverse else ASCII_CHARS[::-1]

        pixels_in_image = list(image.getdata())
        pixels_to_chars = [ascii_chars[int(pixel_value / range_width)] for pixel_value in pixels_in_image]

        return "".join(pixels_to_chars)


def convert_image_to_ascii(image, reverse=False, new_width=None):
    if not new_width:
        new_width = image.width
    image = scale_image(image, new_width)
    image = convert_to_grayscale(image)

    pixels_to_chars = map_pixels_to_ascii_chars(image, reverse, new_width)
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


def handle_image_conversion(image_filepath, reverse, width):
    try:
        image = Image.open(image_filepath)
    except Exception as e:
        print(f"Unable to open image file {image_filepath}.")
        print(e)
        return None

    return convert_image_to_ascii(image, reverse, width)


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

message = (pyjokes.get_joke()) #this is message ie the running text obtained from pyjokes library function



#typerwriter is the method for running the text
def typewriter(message):
    #the spaces are for format on the splash screen
    font = ['alligator', 'slant', '3-d', '3x5','5lineoblique','banner3-D']
    print(pyfiglet.figlet_format("   zTm ", font = random.choice(font)).rstrip())
    print(pyfiglet.figlet_format("Community Presents -- "))
    print(pyfiglet.figlet_format("                           ASCII ART"))
    # print(pyfiglet.figlet_format("==> "))

    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        if char!= '\n':
            time.sleep(0.1)
        else:
            time.sleep(1)


def is_supported(path):
    if not path:
        return False
    _, ext = os.path.splitext(path)
    return ext.lower() in SUPPORTED_IMAGE_TYPES


def check_file(path):
    """Check if the path leads to a supported image supported"""
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
    """Works out the ascii filename from the input name"""
    return f"{os.path.splitext(input if input else '')[0]}_output.txt"


def show_credits():
    """Show credits"""
    message = "We The Members Of ZTM Community Will Grab That Tshirt By Showcasing Our Efforts In HacktoberFest "
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


def process(input_file, reverse=False, save=False, output=None, width=None, color=None):
    """Orchestrates the conversion of a single image to ascii."""
    check_file(input_file)
    save = save or (output is not None)
    if save and not output:
        output = output_name(input_file)
    ascii_str = handle_image_conversion(input_file, reverse, width)

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
def cli(input_files, reverse, save, output, width, credits, clock, all, color):
    if clock:
        show_clock()
        return
    if credits:
        show_credits()
        print()

    if all:
        input_files = all_supported_files()

    for file in input_files:
        process(file, reverse=reverse, save=save, output=output, width=width, color=color.lower())
    if not input_files:
        print("There is no image...please make sure that there is image for convert!")


if __name__ == '__main__':
    cli()
