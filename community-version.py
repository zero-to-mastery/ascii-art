# this project requires Pillow installation: https://pillow.readthedocs.io/en/stable/installation.html
<<<<<<< HEAD
#code credit goes to: https://www.hackerearth.com/practice/notes/beautiful-python-a-simple-ascii-art-generator-from-images/
#code modified to work with Python 3 by @aneagoie

import os
import sys
=======
# code credit goes to: https://www.hackerearth.com/practice/notes/beautiful-python-a-simple-ascii-art-generator-from-images/
# code modified to work with Python 3 by @aneagoie
from __future__ import division
import os

>>>>>>> eb24124d3925f2caef56d2886b9e3925cd4b2493
from PIL import Image
from asciimatics.effects import Print, Clock
from asciimatics.renderers import FigletText, Rainbow
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError




<<<<<<< HEAD
# Global Variables
OUT_FILE_PATH = "./output_images/"

ASCII_CHARS = [ '#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']

HELP_MSG = """
Usage  : python community-version.py [option] [input_file]
=======
import pyfiglet
import sys, time #used for displaying running text
import pygame #used for sound for running text
import random
help_msg = """
Usage  : python community-version.py [option] [input_file] [color]
>>>>>>> eb24124d3925f2caef56d2886b9e3925cd4b2493
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

<<<<<<< HEAD
FILE_ERROR_MSG = """
File type of [input_file] not valid, please make sure it is of type PNG.
"""


class ConvertImageToASCII():

    def __init__(self, file_path=None, option='-c'):
        ''' Default file_path is None and option to use is -c '''
        self.image_file_path = file_path
        self.option = option

    def scale_image(self, image, new_width=100):
        """Resizes an image preserving the aspect ratio.
        """
        (original_width, original_height) = image.size
        aspect_ratio = original_height/float(original_width)
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
        pixels_to_chars = [ASCII_CHARS[int(pixel_value/range_width)] for pixel_value in
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
        ''' Make to appropriate option provided to convert image '''
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
        ''' Make method to convert image with reverse ASCII charactes '''
        return self.convert_image_to_ascii(image)   # replace this with your reversed ascii image conversion

    def _createOutFilePath(self, file_name):
        ''' Create out file path if not exists and return filepath '''
        global OUT_FILE_PATH
        if not os.path.exists(OUT_FILE_PATH):
            os.mkdir(OUT_FILE_PATH)
        file_path = OUT_FILE_PATH + file_name
        return file_path
    
    def _saveConvertedImage(self, image):
        ''' Save converted image as a text file '''
        global OUT_FILE_PATH
        partition_file_path = self.image_file_path.split('/')
        output_file_name = partition_file_path[-1]
        output_file_name = output_file_name.split('.')[0] + "_output.txt"
        output_file_path = self._createOutFilePath(output_file_name)
=======
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


def map_pixels_to_ascii_chars(image, range_width=25):
    """Maps each pixel to an ascii char based on the range
    in which it lies.
    0-255 is divided into 11 ranges of 25 pixels each.
    """

    pixels_in_image = list(image.getdata())
    pixels_to_chars = [ASCII_CHARS[int(pixel_value / range_width)] for pixel_value in
                       pixels_in_image]

    return "".join(pixels_to_chars)


def convert_image_to_ascii(image, new_width=100):
    image = scale_image(image)
    image = convert_to_grayscale(image)

    pixels_to_chars = map_pixels_to_ascii_chars(image)
    len_pixels_to_chars = len(pixels_to_chars)

    image_ascii = [pixels_to_chars[index: index + new_width] for index in
                   range(0, len_pixels_to_chars, new_width)]

    return "\n".join(image_ascii)


def write_image_to_text_file(image_ascii):
    if "/" in image_file_path:
        split_file_name = image_file_path.split('/')
        image_name = split_file_name[-1]
    else:
        image_name = image_file_path
    split_image_name = image_name.split('.')
    file_name = split_image_name[0]
    text_file_name = file_name + ".txt"

    with open(text_file_name, "w") as f:
        f.write(image_ascii)


def color_change():
    arguments = [x for x in sys.argv]

    if arguments[-1] == "black":
        return arguments[-1]
    elif arguments[-1] == "red":
        return arguments[-1]
    elif arguments[-1] == "green":
        return arguments[-1]
    elif arguments[-1] == "yellow":
        return arguments[-1]
    elif arguments[-1] == "blue":
        return arguments[-1]
    elif arguments[-1] == "magenta":
        return arguments[-1]
    elif arguments[-1] == "cyan":
        return arguments[-1]
    elif arguments[-1] == "white":
        return arguments[-1]
    else:
        return "none"


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


def handle_image_conversion(image_filepath, arg=""):
    image = None
    try:
        image = Image.open(image_filepath)
    except Exception as e:
        print(f"Unable to open image file {image_filepath}.")
        print(e)
        return

    image_ascii = convert_image_to_ascii(image)

    if color_change() == 'none':
        print(image_ascii)
    else:
        os.system("cls")
        color = color_change()
        text = f"[[{color}]]" + image_ascii + "[[white]]"
        print(colorText(text))

    if arg == "-s":
        output_name = image_file_path.split('.')[0] + "_output.txt"
>>>>>>> eb24124d3925f2caef56d2886b9e3925cd4b2493
        try:
            with open(output_file_path, 'w') as out_file:
                out_file.write(image)
            print(f"Image (as a text) saved to -> {output_file_path}")
        except:
            print("An error occured while saving image as a text file !")
            return False
    
    def handle_image_conversion(self):
        image = None
        try:
            image = Image.open(self.image_file_path)
        except Exception as e:
            print(f"Unable to open image file {self.image_file_path}.")
            print(e)
            return

        convertedImage = self.map_option_to_convert(image)
        return convertedImage


<<<<<<< HEAD
def check_file(f):
    ''' Check file type, it should be png (as of now) '''
    global HELP_MSG
    allowed_inputs_file = ["png"]
    try:
        if f.split('.')[-1] in allowed_inputs_file:
            return True
        else:
            return False
    except:
        print(HELP_MSG)
        return False


def get_cli_input():
    ''' Check if program running through command line '''
    cli_input = [inp for inp in sys.argv]
    input_file = cli_input[-1]
    input_option = '-c'
    isFileTypeCorrect = check_file(input_file)
    if len(cli_input) > 2:
        input_option = cli_input[1]
    return isFileTypeCorrect, input_file, input_option
=======

def check_inputs():
    arguments = [x for x in sys.argv]
    if 2 > len(arguments) or len(arguments) > 4:
        print(help_msg)
        return False
    elif len(arguments) == 2:
        return ""
    elif len(arguments) == 3 and arguments[1] == "-r":
        return arguments[1]
    elif len(arguments) == 3 and arguments[1] == "-s":
        return arguments[1]
    elif len(arguments) == 3 and arguments[1] == "-rs":
        return arguments[1]
    elif len(arguments) == 4 and arguments[1] == "-r":
        return arguments[1]
    elif len(arguments) == 4 and arguments[1] == "-s":
        return arguments[1]
    elif len(arguments) == 4 and arguments[1] == "-rs":
        return arguments[1]
    else:
        return ""
>>>>>>> eb24124d3925f2caef56d2886b9e3925cd4b2493

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


#this is message ie the running text
message = "We The Members Of ZTM Community Will Grab That Tshirt By Showcasing Our Efforts In HacktoberFest "

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

<<<<<<< HEAD
if __name__=='__main__':
    isFile, cli_input_file, cli_input_option = get_cli_input()
    print(f"File {cli_input_file} is PNG ? {isFile}, called with option {cli_input_option} (-c is default)")
    if not isFile:
        print(HELP_MSG)
        raise Exception(FILE_ERROR_MSG)
    ascii_convert_obj = ConvertImageToASCII(file_path=cli_input_file, option=cli_input_option)
    print(ascii_convert_obj.handle_image_conversion())
=======


if __name__ == '__main__':
 	
    import sys

    pygame.mixer.init()
    pygame.mixer.music.load("typewriter.wav") #run typewriter sound file
    pygame.mixer.music.play(loops=-1)
    os.system('cls') #used for clearing the screen output
    typewriter(message) #calling the typewriter function
    pygame.mixer.music.stop()
    pygame.mixer.quit()

    arguments = [x for x in sys.argv]
    todo = check_inputs()
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

    else:

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
>>>>>>> eb24124d3925f2caef56d2886b9e3925cd4b2493
