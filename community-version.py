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

ASCII_CHARS = [ '#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']

from asciimatics.effects import Print, Clock
from asciimatics.exceptions import ResizeScreenError
from asciimatics.renderers import FigletText, Rainbow
from asciimatics.scene import Scene
from asciimatics.screen import Screen
import random
import pyjokes


ASCII_CHARS = ['#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']
COLOR_OPTIONS = ['black', 'blue', 'cyan',
                 'green', 'magenta', 'red', 'white', 'yellow']
SUPPORTED_IMAGE_TYPES = ('.png', '.jpeg', '.jpg')
font = ['alligator', 'slant', '3-d', '3x5', '5lineoblique', 'banner3-D']





ASCII_CHARS = [ '#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']

import pyfiglet

import sys, time #used for displaying running text
import pygame #used for sound for running text

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

import os
import sys

image_file_path = sys.argv[1]


def save_ascii_art(image_ascii_art):
    """
    saving the ascii art 
    """
    image_output_folder = ""
    file_name=""
    
    try:        
        try:
            image_output_folder = sys.argv[2]
            file_path = os.path.split(image_file_path)[1]
            file_name = os.path.splitext(file_path)[0]
        except:
            image_output_folder="ztm-ascii"
            file_name="ztm-default-ascii"

        if not os.path.exists(image_output_folder):
            os.makedirs(image_output_folder)

        with open(f"{image_output_folder}/{file_name}.txt", mode='w') as my_file:
            my_file.write(image_ascii_art)
    except ValueError:
        print('please check image is converted to image ascii art.')



import sys

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
    aspect_ratio = original_height / float(original_width)
    new_height = int(aspect_ratio * new_width * 0.5)

    new_image = image.resize((new_width, new_height), Image.ANTIALIAS)
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
    pixels_to_chars = [
        ascii_chars[int(pixel_value / range_width)] for pixel_value in pixels_in_image]

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

    save_ascii_art(image_ascii)

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


def get_joke():
    return pyjokes.get_joke()


# typerwriter is the method for running the text
def typewriter(message):
    # the spaces are for format on the splash screen
    font = ['alligator', 'slant', '3-d', '3x5', '5lineoblique', 'banner3-D']
    print(pyfiglet.figlet_format("   zTm ", font=random.choice(font)).rstrip())
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

if __name__=='__main__':
    image_file_path = sys.argv[1]
    if sys.argv[2]:
        handle_image_conversion(image_file_path, 1)
    print(image_file_path)
    handle_image_conversion(image_file_path, 0)

    image_file_path = sys.argv[1]
    if sys.argv[2]:
        handle_image_conversion(image_file_path, 1)
    print(image_file_path)
    handle_image_conversion(image_file_path, 0)


    image_file_path = sys.argv[1]
    if sys.argv[2]:
        handle_image_conversion(image_file_path, 1)
    print(image_file_path)
    handle_image_conversion(image_file_path, 0)



if __name__=='__main__':

    image_file_path = sys.argv[1]
    if sys.argv[2]:
        handle_image_conversion(image_file_path, 1)
    print(image_file_path)
    handle_image_conversion(image_file_path, 0)


if __name__ == '__main__':
 	
    import sys

def ascii_text(): #function to convert simple text into random font ascii format text

def ascii_text():  # function to convert simple text into random font ascii format text

    text = str(input('\n Enter The Text To Convert To Ascii-Art \n'))
    print(pyfiglet.figlet_format(text, font=random.choice(font)).rstrip())


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

    message = (pyjokes.get_joke()) #this is message ie the running text obtained from pyjokes library function


    message = (pyjokes.get_joke(
    ))  # this is message ie the running text obtained from pyjokes library function

    pygame.mixer.init()
    pygame.mixer.music.load("typewriter.wav")
    pygame.mixer.music.play(loops=-1)
    os.system('cls')
    typewriter(message)
    pygame.mixer.music.stop()
    pygame.mixer.quit()

    arguments = [x for x in sys.argv]
    todo = check_inputs()
    ASCII_CHARS = [ '#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']

    image_file_path = ""

    try:
        image_file_path = sys.argv[2]
    except:
        image_file_path = "ztm-ascii/ztm-default-ascii.txt"

    if todo == "":
        image_file_path = sys.argv[1]
        print(image_file_path)
        handle_image_conversion(image_file_path)
    elif todo == '-r':
        ASCII_CHARS = [ '#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@'][::-1]
        print(image_file_path)
        handle_image_conversion(image_file_path)
    elif todo == "-s":
        print(image_file_path)
        handle_image_conversion(image_file_path, "-s")
    elif todo == "-rs":
        ASCII_CHARS = [ '#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@'][::-1]
        print(image_file_path)
        handle_image_conversion(image_file_path, "-s")
    ASCII_CHARS = ['#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']

    if len(arguments) == 2 and arguments[1] == "all":
        arr = os.listdir()
        listOfImages = []
        for i in arr:
            if i.lower().endswith(('.png', '.jpg')):
                listOfImages.append(i)
        if len(listOfImages) == 0:
            print("There is no image...please make sure that there is image for convert!")
        else:
            for images in listOfImages:
                image = Image.open(images)
                image_ascii = convert_image_to_ascii(image)
                print(image_ascii)
                im = images[:-4]
                im = im + ".txt"
                try:
                    f = open(im, "w")
                    f.write(image_ascii)
                    f.close
                    print(f"Image saved to -> {im}")
                except:
                    print("An error occured!")

    elif len(arguments) == 2 and arguments[1] == "clock":

    		try:
        		Screen.wrapper(demo)
        		sys.exit(0)
    		except ResizeScreenError:
        		pass



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
@click.option('--text', is_flag=True, help='Convert Simple Text Into Ascii Text Format, Enter Text After Prompt')
def cli(input_files, reverse, save, output, width, credits, clock, all, color, text):
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


        if todo == "":
            image_file_path = sys.argv[1]
            print(image_file_path)
            handle_image_conversion(image_file_path)
        elif todo == '-r':
            ASCII_CHARS = ['#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@'][::-1]
            image_file_path = sys.argv[2]
            print(image_file_path)
            handle_image_conversion(image_file_path)
        elif todo == "-s":
            image_file_path = sys.argv[2]
            print(image_file_path)
            handle_image_conversion(image_file_path, "-s")
        elif todo == "-rs":
            ASCII_CHARS = ['#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@'][::-1]
            image_file_path = sys.argv[2]
            print(image_file_path)
            handle_image_conversion(image_file_path, "-s")

    for file in input_files:
        process(file, reverse=reverse, save=save,
                output=output, width=width, color=color.lower())
    if not input_files:
        print("There is no image...please make sure that there is image for convert!")


if __name__ == '__main__':
    cli()

