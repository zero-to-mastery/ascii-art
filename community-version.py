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
    """Converts an image to grayscale."""
    return image.convert('L')

def map_pixels_to_ascii_chars(image, make_silhouette=False, range_width=25, brightness=1.0):
    """Maps pixel values to ASCII characters based on a specified range and brightness."""
    pixels_in_image = list(image.getdata())

    if make_silhouette:
        pixels_in_image = [r for r,g,b,a in pixels_in_image]

    adjusted_pixels = [int(pixel * brightness) for pixel in pixels_in_image]

    pixels_to_chars = [ASCII_CHARS[int(pixel_value / range_width)] for pixel_value in adjusted_pixels]
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

def handle_image_conversion(image_filepath, make_silhouette = False, output_file_path='output.txt', brightness=1.0):
    """Handles the conversion of an image to ASCII art with adjustable brightness.
    Saves the output to a file if output_file_path is provided.
    """
    try:
        image = Image.open(image_filepath)
    except FileNotFoundError:
        print(f"Error: File not found - {image_filepath}")
        return
    except PermissionError:
        print(f"Error: Permission denied - {image_filepath}")
        return
    except Exception as e:
        print(f"Error: Unable to open image file {image_filepath}.")
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

    return file_path

if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--path", help="path to image file", required=False)
    parser.add_argument("-s", "--silhouette", help="Make ASCII silhouette", required=False)
    parser.add_argument("-o", "--output", help="Output file and path", required=False)
    parser.add_argument("-b", "--brightness", help="Alter brightness of image (e.g. -b 1.0)", required=False)
    args = parser.parse_args()
    make_silhouette = False
    brightness = 1.0
    image_file_path = args.path
    output_file_path = 'output.txt'

    """ use file dialog if no arguments are passed """
    if len(sys.argv) < 2:
        image_file_path = get_image_path()

    if len(sys.argv) > 2:
        if args.silhouette is not None:
            make_silhouette = args.silhouette.lower() in ['true', 'yes', 'y', 't']
    if args.brightness is not None:
        brightness = float(args.brightness)
    if args.output is not None:
        output_file_path = args.output

    print(image_file_path)
    handle_image_conversion(image_file_path, make_silhouette, output_file_path, brightness)
