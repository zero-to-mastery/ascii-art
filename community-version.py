#!/usr/bin/python3
## Community Version
"""
This is class SIMPLEcmd
"""

import sys
import argparse
import os
from PIL import Image, ImageDraw, ImageFont
import cmd
from example.make_art import convert_image_to_ascii
import requests
from io import BytesIO


# changing ascii-art to image
text_file = "./custom_text.txt"
def art_to_image(text_file):
    with open(text_file, 'r') as f:
        ascii_text = f.read()
    
    # Get dimensions
    im = Image.new("RGBA", (0, 0))
    draw = ImageDraw.Draw(im)
    (_, _, right, bottom) = draw.multiline_textbbox((0, 0), ascii_text) # get width and height in px

    # draw the image based on the dimensions
    im = Image.new("RGBA", (right, bottom), "white")
    draw = ImageDraw.Draw(im)
    draw.text((0, 0), ascii_text, fill="black")

    # Save Image
    im.save("final.png", "PNG")


def is_image_file(path_to_file):
    """
    This function checks if the the file is valid image
    @param path_to_file :path to the file to be checked
    @return Boolean Flag indicating if tje path is valid or not
    """
    if not os.path.isabs(path_to_file):
        path_to_file = os.path.abspath(path_to_file)

    try:
        with Image.open(path_to_file) as img:
            return True
    except Exception as not_image:
        return False


class SimpleCmd(cmd.Cmd):
    """
    this is command interpreter class
    """
    prompt = "(hackfest) "

    def do_quit(self, arg):
        """
        This method exit the program
        """
        return True

    def do_EOF(self, arg):
        """
        Exits the program without crashing
        """
        print()
        return True

    def helf_quit(self):
        """
        This is quit method help message
        """
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
        """Creates multiple instances of a model at once.

  Args:
    data: An array of objects, each of which represents a single instance of the model.
    options: An object of options that can be used to customize the behavior of the function.

  Returns:
    An array of objects, each of which represents an instance of the model that was created. """

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

    def do_ascii_text(self, args):
        """
        converts text to image and then to ascii art 
        
        Usage: ascii_text <Text>
        Example: ascii_text Hello World
        """
        if not args:
            print("** Text missing **")
            return
        
        else:
        
            # print(args)
            
            # Width and height of the image in pixels
            # color in RGB
            width = 500  
            height = 300  
            # background_color = (211, 211, 211)  
            background_color = (255, 255, 255)

            img = Image.new("RGB", (width, height), background_color)

            # Define the font size and load a font
            font_size = 85
            # font = ImageFont.truetype("comicbd.ttf", font_size)
            font = ImageFont.truetype("arial.ttf", font_size)

            # draw on image
            if len(args) > 6 :
                toptext=str(args)[:6]
                bottomtext=str(args)[6:]

                img_draw = ImageDraw.Draw(img)
                img_draw.text((50, 50), toptext, fill=(0,0,0), font=font)   
                img_draw.text((50, 150), bottomtext, fill=(0,0,0), font=font)

            else:
                img_draw = ImageDraw.Draw(img)
                img_draw.text((50, 50), args, fill=(0,0,0), font=font)

            """
            not using bytesio
            """
            ascii_img = convert_image_to_ascii(img, new_width=100)
            print(ascii_img)

        return True
# this project requires Pillow installation: https://pillow.readthedocs.io/en/stable/installation.html

# code credit goes to: https://www.hackerearth.com/practice/notes/beautiful-python-a-simple-ascii-art-generator-from-images/
# code modified to work with Python 3 by @aneagoie


from tkinter import Tk, filedialog

import string

ascii_printable = string.printable
ASCII_CHARS = list(ascii_printable)

def scale_image(image, new_width=100):
    """
    This Function Resizes an image preserving the aspect ratio.
    @param image:input image to be resized
    @param new_width(optional):The new width required by default it is 100

    @return the newly resized image
    """
    (original_width, original_height) = image.size
    aspect_ratio = original_height / float(original_width)
    new_height = int(aspect_ratio * new_width)

    new_image = image.resize((new_width, new_height))
    return new_image

def convert_to_grayscale(image):
    """
    This Function Converts an image to grayscale.
    @param image:The image to be converted to grey

    @return the grey scale image
    """
    return image.convert('L')

def map_pixels_to_ascii_chars(image, make_silhouette=False, range_width=25, brightness=1.0):
    """
    Maps pixel values to ASCII characters based on a specified range and brightness.
    @param image:The image to be converted to ASCII
    @param make_silhouette:Flag to indicate if the image required to be silhouette
    @param range_width:The range of the result width
    @param brightness:The brightness of the image [0-1]

    @return the new ASCII image
    """
    pixels_in_image = list(image.getdata())

    if make_silhouette:
        pixels_in_image = [m[3] for m in image.getdata()]

    adjusted_pixels = [int(pixel * brightness) for pixel in pixels_in_image]

    pixels_to_chars = [ASCII_CHARS[min(int(pixel_value / range_width),
                                       len(ASCII_CHARS) - 1)] for pixel_value in adjusted_pixels]
    return "".join(pixels_to_chars)

def convert_image_to_ascii(image, make_silhouette=False, new_width=100, brightness=1.0):
    """
    Converts an image to ASCII art with adjustable brightness.
    """
    image = scale_image(image)

    if not make_silhouette:
        image = convert_to_grayscale(image)

    pixels_to_chars = map_pixels_to_ascii_chars(image, make_silhouette=make_silhouette, brightness=brightness)

    len_pixels_to_chars = len(pixels_to_chars)
    image_ascii = [pixels_to_chars[index: index + new_width] for index in range(0, len_pixels_to_chars, new_width)]
    return "\n".join(image_ascii)

def fetch_image_from_url(url):
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        try:
            image = Image.open(BytesIO(response.content))
        except Exception as e:
            print("There is a problem when fetching image from url")
            return e
    else:
        print("Can't get request - Return status code", response.status_code)
        raise Exception('Status code is not 200')
    return image


def handle_image_conversion(image_filepath, url, make_silhouette=False, output_file_path='output.txt', brightness=1.0, output_image=False):
    """Handles the conversion of an image to ASCII art with adjustable brightness.
    Saves the output to a file if output_file_path is provided.
    """
    try:
        if not url:
            # read image from file
            image = Image.open(image_filepath)
        else: 
            image = fetch_image_from_url(url)
    except FileNotFoundError:
        print(f"Error: File not found - {image_filepath}")
        return
    except PermissionError:
        print(f"Error: Permission denied - {image_filepath}")
        return
    except Exception as e:
        print(f"Unable to open image file {image_filepath}.")
        print(f"Make sure the file you are trying to use resides on the given path {image_filepath}.")

        print(e)
        return

    image_ascii = convert_image_to_ascii(image, make_silhouette=make_silhouette, brightness=brightness)
    print(image_ascii)

    if output_file_path:
        save_ascii_art_to_file(image_ascii, output_file_path)
        print(f"ASCII art saved to {output_file_path}")
    
    if output_image:
        try:
            save_ascii_art_to_jpg(image_ascii, image)
        except Exception as exception:
            print(str(exception))
            return


def save_ascii_art_to_file(image_ascii, output_file_path):
    """
    Saves the ASCII art to a file.
    @param image_ascii:The ASCII image to be saved
    @param output_file_path:The path of the output image

    @return None
    """
    with open(output_file_path, 'w') as f:
        f.write(image_ascii)

def save_ascii_art_to_jpg(image_ascii, image):
    if not image:
        raise Exception('Image object is invalid')
    if len(image_ascii) <= 0:
        raise Exception('ASCII art string is of invalid length')
    
    # Dimensions of the original image
    original_image_width, original_image_height = image.size
    characters_count_in_width = len(image_ascii.split()[0])
    characters_count_in_height = len(image_ascii.split())

    # Dimensions of the output image
    output_image_width = 6*characters_count_in_width
    output_image_height = 15*characters_count_in_height

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    try:
        # Create a blank image of black background
        image = Image.new("RGB", (output_image_width, output_image_height), BLACK)
        draw = ImageDraw.Draw(image)

        # Draw the text on the blank image from top left corner with font color of white
        draw.text((0, 0), image_ascii, fill=WHITE)

        # Resize the output image as per the original image's dimensions
        resized_image = image.resize((original_image_width, original_image_height))
        resized_image.save('output.jpg')
        print('ASCII art image saved to output.jpg')
    except Exception as exception:
        raise exception

def get_image_path():
    """
    Open a file dialog to select an image and return its path.
    """
    root = Tk()
    root.withdraw()  # Hide the root window

    file_path = filedialog.askopenfilename()
    root.destroy()  # Destroy the root window after selection

    if not file_path:  # if no file uploaded exit peacefully
        print("No file selected. Exiting.")
        sys.exit()

    return file_path


if __name__ == '__main__':
    print("To change Image to ASCII Art type '1'")
    print("To change ASCII Art to Image type '2'")
    print("Note! If you type '2', make sure you have 'custom_text.txt' file already in root directory with ASCII-Art in it.")

    answer = input("Please type either '1' or '2': ")
  
    if answer == '2':
        if os.path.isfile(f'./{text_file}'):
            art_to_image(text_file)
        else:
            print("You did not create 'custom_text.txt' file in home directory. Program ends here.")
        exit()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--interactive", action="store_true", help="Run in interactive mode"
    )

    parser.add_argument("-f", "--file", help="Image file path")

    parser.add_argument("-s", "--silhouette", help="Make ASCII silhouette", action="store_true", default=False)
    parser.add_argument("-o", "--output", help="Output file and path")
    parser.add_argument("-b", "--brightness", help="Alter brightness of image (e.g. -b 1.0)", required=False)
    parser.add_argument("-l", "--url", help="Link to image's url on the internet")
    parser.add_argument("-c", "--chars", help="DIY the chars list to draw your unique ascii art", required=False)
    parser.add_argument("-u", "--output-image", help="Creates an output.jpg file of the ASCII art", action="store_true", default=False)

    args = parser.parse_args()
    # make_silhouette = False
    # image_file_path = args.path

    """ 
    use file dialog if no arguments are passed 
    """
    if args.interactive:
        SimpleCmd().cmdloop()
    else:
        source, file_name = 'Local file', ''
        if (args.file is None or (args.file == "-s")) and args.url is None:
            args.file = get_image_path()
            file_name = args.file
        elif args.url:
            file_name = args.url
            source = 'External URL'
        else:
            file_name = args.file
        
        if args.chars:
            ASCII_CHARS = list(set(args.chars))
        
        print("Image from {}: {}".format(source, file_name))

        handle_image_conversion(file_name, args.url,
                                make_silhouette=args.silhouette,
                                output_file_path=args.output if args.output else 'output.txt',
                                brightness=float(args.brightness) if args.brightness else 1.0,
                                output_image=args.output_image
                                )


