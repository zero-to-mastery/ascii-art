# this project requires Pillow installation: https://pillow.readthedocs.io/en/stable/installation.html

#code credit goes to: https://www.hackerearth.com/practice/notes/beautiful-python-a-simple-ascii-art-generator-from-images/
#code modified to work with Python 3 by @aneagoie
from PIL import Image
from typing import List

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

def map_pixels_to_ascii_chars(image: Image.Image, range_width: int = 25) -> str:
    """Maps each pixel to an ascii char based on the range
    in which it lies.

    0-255 is divided into 11 ranges of 25 pixels each.
    """

    pixels_in_image: List[int] = list(image.getdata())
    pixels_to_chars: List[int] = [ASCII_CHARS[int(pixel_value/range_width)] for pixel_value in
            pixels_in_image]

    return "".join(pixels_to_chars)

def convert_image_to_ascii(image: Image.Image, new_width: int = 100) -> str:
    image = scale_image(image)
    image = convert_to_grayscale(image)

    pixels_to_chars:str = map_pixels_to_ascii_chars(image)
    len_pixels_to_chars: int = len(pixels_to_chars)

    image_ascii: List[str] = [pixels_to_chars[index: index + new_width] for index in
            range(0, len_pixels_to_chars, new_width)]

    return "\n".join(image_ascii)

def handle_image_conversion(image_filepath) -> None:
    image: Image.Image = None
    try:
        image = Image.open(image_filepath)
    except Exception as e:
        print(f"Unable to open image file {image_filepath}.")
        print(e)
        return

    image_ascii: str = convert_image_to_ascii(image)
    print(image_ascii)

if __name__=='__main__':
    import sys

    image_file_path: str = sys.argv[1]
    print(image_file_path)
    handle_image_conversion(image_file_path)