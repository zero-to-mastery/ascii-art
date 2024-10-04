# this project requires Pillow installation: https://pillow.readthedocs.io/en/stable/installation.html

#code credit goes to: https://www.hackerearth.com/practice/notes/beautiful-python-a-simple-ascii-art-generator-from-images/
#code modified to work with Python 3 by @aneagoie
from PIL import Image
from typing import List
import os
import argparse
import sys

ASCII_CHARS: List[str] = [ '#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']

def scale_image(image: Image.Image, new_width: int = 100) -> Image.Image:
    # Resizes an image preserving the aspect ratio
    (original_width, original_height) = image.size
    aspect_ratio: float = original_height/float(original_width)
    new_height: int = int(aspect_ratio * new_width)

    new_image: Image.Image = image.resize((new_width, new_height))
    return new_image

def convert_to_grayscale(image: Image.Image) -> Image.Image:
    return image.convert('L')

def map_pixels_to_ascii_chars(image: Image.Image, ascii_chars: List[str], range_width: int = 25) -> str:
    """Maps each pixel to an ascii char based on the range
    in which it lies.The range is dynamically calculated
    based on the number of ASCII characters provided.

    by default ASCII_CHARS: 0-255 is divided into 11 ranges of 25 pixels each.
    """
    # Calculate the number of possible ranges
    num_chars = len(ascii_chars)

    if num_chars == 0:
        raise ValueError("The ASCII character list cannot be empty.")

    # Dynamically calculate the range width based on the number of ASCII characters
    range_width: int = 256 // len(ascii_chars)

    pixels_in_image: List[int] = list(image.getdata())
    pixels_to_chars: List[int] = [ascii_chars[min(int(pixel_value//range_width), num_chars - 1)] for pixel_value in
            pixels_in_image]

    return "".join(pixels_to_chars)


def saving_image_to_file(image_ascii:str, output_path:str):
    output_directory = os.path.dirname(output_path)
    # Check if the directory exists
    if output_directory and not os.path.exists(output_directory):
        print(f"Directory '{output_directory}' does not exist. Attempting to create it...")
        try:
            os.makedirs(output_directory)
            print(f"Directory '{output_directory}' created successfully.")
        except Exception as e:
            print(f"Failed to create directory '{output_directory}. Error: {e}")
            return
    try:
        with open(output_path, "w") as f:
            f.write(image_ascii)
            print(f"ASCII art saved successfully to {output_path}.")
    except Exception as e:
        print(f"Failed to save ASCII art. Error: {e}")
    

def convert_image_to_ascii(image: Image.Image, ascii_chars: List[str], new_width: int = 100) -> str:
    image = scale_image(image, new_width)
    image = convert_to_grayscale(image)

    pixels_to_chars:str = map_pixels_to_ascii_chars(image, ascii_chars)
    len_pixels_to_chars: int = len(pixels_to_chars)

    image_ascii: List[str] = [pixels_to_chars[index: index + new_width] for index in
            range(0, len_pixels_to_chars, new_width)]

    return "\n".join(image_ascii)

def handle_image_conversion(image_filepath:str, ascii_chars: List[str], new_width:int) -> str:
    """Handles image conversion and prints the ASCII art."""

    # image: Image.Image = None
    try:
        image = Image.open(image_filepath)
    except Exception as e:
        print(f"Unable to open image file {image_filepath}.")
        print(e)
        return ""

    image_ascii: str = convert_image_to_ascii(image, ascii_chars, new_width)
    return image_ascii

def invert_image_colors(image:Image.Image) -> Image.Image:
    """
    Inverts the colors of the image.
    """

    
    return Image.eval(image, lambda x: 255 - x)

def interactive_prompt():

    print("\n--- Interactive Mode ---")

    image_path = input("(1) Enter the path to your image file (or press Enter to use default 'example/ztm-logo.png'): ")
    if not image_path.strip():
        image_path = "example/ztm-logo.png"

    output_path = input("(2) Enter the output file path (or press Enter to print to the console):")

    width = input("(3) Enter the width of the output (or press Enter to use default): ")
    width = int(width) if width.isdigit() else 100

    invert_colors = input("(4) Do you want to invert the colors? (y/n): ")
    invert_colors = invert_colors.lower() == 'y'

    custom_chars = input ("(5) Enter custom ASCII characters to use (or press Enter to use default): ")
    ascii_chars = list(set(custom_chars)) if custom_chars else ASCII_CHARS

    try:
        image = Image.open(image_path)
        if invert_colors:
            image = invert_image_colors(image)
            print("Invert the colors of the image.")
    except Exception as e:
        print(f"Failed to load image {image_path}. Error: {e}")
        exit(1)

    # Convert the image to ASCII
    ascii_image = convert_image_to_ascii(image, ascii_chars, width)

    # Save or print the result
    if output_path:
        saving_image_to_file(ascii_image, output_path)
    else:
        print("\nHere is your ASCII art:\n")
        print(ascii_image)

def process_command_line_arguments():

    print("\n### User Guide ###")
    print("Usage: python community-version.py [options] [image_path]")
    print("\nOptions:")
    print("  image_path           Path to the input image file (default: 'example/ztm-logo.png')")
    print("  -o, --output         Path to save the ASCII output (default: print to console)")
    print("  -w, --width          Width of the output ASCII art (default: 100)")
    print("  -i, --invert         Invert the colors of the image")
    print("  -c, --chars          Custom ASCII characters to use")
    print("\nExample:")
    # print("  python community-version.py  -o output.txt -w 80 -i -c '@%#' example/ztm-logo.png")
    print("  python community-version.py -w 200 -c '@%#' example/ztm-logo.png")


    # Ask user to input their command line
    command_line_input = input("\nPlease enter your command line: ")

    # Split the command line input into arguments
    import shlex
    args = shlex.split(command_line_input)

    parser = argparse.ArgumentParser(description="Convert images to ASCII art")

    parser.add_argument('image_path', nargs="?", default='example/ztm-logo.png', help="Path to the input image file (default: 'example/ztm-logo.png')")
    parser.add_argument('-o', '--output', help="Path to save the ASCII output (default: print to console)", default=None)
    parser.add_argument('-w', '--width', type=int, help="Width of the output ASCII art (default: 100)", default=100)
    parser.add_argument('-i', '--invert', help="Invert the colors of the image", action='store_true')
    parser.add_argument('-c', '--chars', help="Custom ASCII characters to use", default=None)

    # Parse the arguments from the command line input
    args = parser.parse_args()  

    # Use custom ASCII characters if provided
    ascii_chars = list(set(args.chars)) if args.chars else ASCII_CHARS

    # Handle image inversion
    try:
        image = Image.open(args.image_path)
        if args.invert:
            image = invert_image_colors(image)
            print("Inverted the colors of the image.")
    except Exception as e:
        print(f"Failed to load image {args.image_path}. Error: {e}")
        exit(1)

    # Convert image to ASCII
    ascii_image = handle_image_conversion(args.image_path, ascii_chars, args.width)

    # Save to file or print to console
    if args.output:
        saving_image_to_file(ascii_image, args.output)
        print(f"ASCII art saved to {args.output}.")  # Inform user that the ASCII art was saved
    else:
        print("\nHere is your ASCII art:\n")
        print(ascii_image)  # Print the ASCII image in the console




if __name__=='__main__':

    # Let the user decide if they want to use interactive mode or CLI arguments

    print("### Welcom to the ASCII Art Generator ###")
    choice = input("Do you want to use the interactive mode (1) or CLI arguments (2)? ")

    if choice.lower() == '1':
        interactive_prompt()    
    else:
        process_command_line_arguments()

