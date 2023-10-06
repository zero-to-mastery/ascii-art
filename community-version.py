#!/usr/bin/python3
## Community Version
"""This is class SIMPLEcmd"""

import os
from PIL import Image
import cmd
from example.make_art import convert_image_to_ascii
import requests
from io import BytesIO


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


# this project requires Pillow installation: https://pillow.readthedocs.io/en/stable/installation.html

# code credit goes to: https://www.hackerearth.com/practice/notes/beautiful-python-a-simple-ascii-art-generator-from-images/
# code modified to work with Python 3 by @aneagoie


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
    """Converts an image to grayscale."""
    return image.convert('L')

def map_pixels_to_ascii_chars(image, make_silhouette=False, range_width=25, brightness=1.0):
    """Maps pixel values to ASCII characters based on a specified range and brightness."""
    pixels_in_image = list(image.getdata())

    if make_silhouette:
        pixels_in_image = [m[3] for m in image.getdata()]

    adjusted_pixels = [int(pixel * brightness) for pixel in pixels_in_image]

    pixels_to_chars = [ASCII_CHARS[min(int(pixel_value / range_width),
        len(ASCII_CHARS) - 1)] for pixel_value in adjusted_pixels]
    return "".join(pixels_to_chars)

def convert_image_to_ascii(image, make_silhouette=False, new_width=100, brightness=1.0):
    """Converts an image to ASCII art with adjustable brightness."""
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

def handle_image_conversion(image_filepath, url, make_silhouette = False, output_file_path='output.txt', brightness=1.0):
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

def save_ascii_art_to_file(image_ascii, output_file_path):
    """Saves the ASCII art to a file."""
    with open(output_file_path, 'w') as f:
        f.write(image_ascii)

def get_image_path():
    """Open a file dialog to select an image and return its path."""
    root = Tk()
    root.withdraw()  # Hide the root window

    file_path = filedialog.askopenfilename()
    root.destroy()  # Destroy the root window after selection
    
    if not file_path: # if no file uploaded exit peacefully
        print("No file selected. Exiting.")
        sys.exit()

    return file_path

if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument(
            "-i", "--interactive", action="store_true", help="Run in interactive mode"
            )

    parser.add_argument("-f", "--file", help="Image file path")
    
    parser.add_argument("-s", "--silhouette", help="Make ASCII silhouette", action="store_true",default=False)
    parser.add_argument("-o", "--output", help="Output file and path")
    parser.add_argument("-b", "--brightness", help="Alter brightness of image (e.g. -b 1.0)", required=False)
    parser.add_argument("-l", "--url", help="Link to image's url on the internet")
    
    args = parser.parse_args()
   # make_silhouette = False
   # image_file_path = args.path
    

    """ use file dialog if no arguments are passed """
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
        
        print("Image from {}: {}".format(source, file_name))

        handle_image_conversion(args.file, args.url, args.silhouette,
                args.output if args.output else 'output.txt',
                float(args.brightness) if args.brightness else 1.0
                )
        

