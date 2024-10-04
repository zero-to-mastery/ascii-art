# this project requires Pillow installation: https://pillow.readthedocs.io/en/stable/installation.html

#code credit goes to: https://www.hackerearth.com/practice/notes/beautiful-python-a-simple-ascii-art-generator-from-images/
#code modified to work with Python 3 by @aneagoie
from PIL import Image, ImageEnhance
from typing import List
import os
import sys

ASCII_CHARS: List[str] = [ '#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']

def scale_image(image: Image.Image, new_width: int = 100) -> Image.Image:
    (original_width, original_height) = image.size
    aspect_ratio: float = original_height / float(original_width)
    new_height: int = int(aspect_ratio * new_width)
    new_image: Image.Image = image.resize((new_width, new_height))
    return new_image

def convert_to_grayscale(image: Image.Image) -> Image.Image:
    return image.convert('L')

def invert_image_colors(image: Image.Image) -> Image.Image:
    """
    Inverts the colors of the image.
    """
    return Image.eval(image, lambda x: 255 - x)

def adjust_brightness(image: Image.Image, factor: float) -> Image.Image:
    """
    Adjusts the brightness of the image by a given factor.
    1.0 means no change, less than 1.0 darkens the image, greater than 1.0 brightens it.
    """
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def adjust_contrast(image: Image.Image, factor: float) -> Image.Image:
    """
    Adjusts the contrast of the image by a given factor.
    1.0 means no change, less than 1.0 decreases contrast, greater than 1.0 increases contrast.
    """
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def map_pixels_to_ascii_chars(image: Image.Image, range_width: int = 25) -> str:
    pixels_in_image: List[int] = list(image.getdata())
    pixels_to_chars: List[str] = [ASCII_CHARS[int(pixel_value / range_width)] for pixel_value in pixels_in_image]
    return "".join(pixels_to_chars)

def convert_image_to_ascii(image: Image.Image, new_width: int = 100) -> str:
    image = scale_image(image)
    image = convert_to_grayscale(image)
    pixels_to_chars = map_pixels_to_ascii_chars(image)
    len_pixels_to_chars = len(pixels_to_chars)

    image_ascii: List[str] = [pixels_to_chars[index: index + new_width] for index in range(0, len_pixels_to_chars, new_width)]
    return "\n".join(image_ascii)

def handle_image_conversion(image_filepath: str, invert: bool = False, brightness: float = 1.0, contrast: float = 1.0) -> str:
    image: Image.Image = None
    try:
        image = Image.open(image_filepath)
    except Exception as e:
        print(f"Unable to open image file {image_filepath}.")
        print(e)
        return

    # Apply brightness adjustment
    if brightness != 1.0:
        print(f"Adjusting brightness by factor: {brightness}")
        image = adjust_brightness(image, brightness)

    # Apply contrast adjustment
    if contrast != 1.0:
        print(f"Adjusting contrast by factor: {contrast}")
        image = adjust_contrast(image, contrast)

    # Invert the image if the invert flag is set
    if invert:
        print("Inverting image colors...")
        image = invert_image_colors(image)

    image_ascii: str = convert_image_to_ascii(image)
    print(image_ascii)
    return image_ascii

def saving_image_to_txt(image_ascii: str, image_path: str):
    image_directory = os.path.dirname(image_path)
    if image_directory and not os.path.exists(image_directory):
        print(f"Directory '{image_directory}' does not exist. Attempting to create it...")
        try:
            os.makedirs(image_directory)
            print(f"Directory '{image_directory}' created successfully.")
        except Exception as e:
            print(f"Failed to create directory '{image_directory}'. Error: {e}")
            return

    try:
        with open(image_path, "w") as f:
            f.write(image_ascii)
            print("ASCII art saved successfully.")
    except Exception as e:
        print(f"Failed to save ASCII art. Error: {e}")

if __name__ == '__main__':
    # Check for command-line arguments
    image_file_path: str = sys.argv[1]
    invert_flag = '--invert' in sys.argv  # Check if the invert flag is passed
    txt_file_path = sys.argv[2] if len(sys.argv) >= 3 else None

    # Parse brightness and contrast from command-line arguments
    brightness = 1.0
    contrast = 1.0
    for arg in sys.argv:
        if arg.startswith("--brightness="):
            brightness = float(arg.split("=")[1])
        elif arg.startswith("--contrast="):
            contrast = float(arg.split("=")[1])

    print(f"Processing image: {image_file_path} (Invert: {invert_flag}, Brightness: {brightness}, Contrast: {contrast})")
    
    # Convert image to ASCII
    ascii_image = handle_image_conversion(image_file_path, invert=invert_flag, brightness=brightness, contrast=contrast)

    # Save to file if a file path is provided
    if txt_file_path:
        saving_image_to_txt(ascii_image, txt_file_path)
