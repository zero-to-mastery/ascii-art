# this project requires Pillow installation: https://pillow.readthedocs.io/en/stable/installation.html

#code credit goes to: https://www.hackerearth.com/practice/notes/beautiful-python-a-simple-ascii-art-generator-from-images/
#code modified to work with Python 3 by @aneagoie
from PIL import Image
ASCII_CHARS = [ '#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']

def scale_image(image, new_width=100):
    """Resizes an image preserving the aspect ratio.
    """
    (original_width, original_height) = image.size
    aspect_ratio = original_height/float(original_width)
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
    pixels_to_chars = [ASCII_CHARS[int(pixel_value/range_width)] for pixel_value in
            pixels_in_image]

    return "".join(pixels_to_chars)

def convert_image_to_ascii(image, new_width=100):
    image = scale_image(image, new_width)
    image = convert_to_grayscale(image)

    pixels_to_chars = map_pixels_to_ascii_chars(image)
    len_pixels_to_chars = len(pixels_to_chars)

    image_ascii = [pixels_to_chars[index: index + new_width] for index in
            range(0, len_pixels_to_chars, new_width)]

    return "\n".join(image_ascii)

def handle_image_conversion(image_filepath, new_width=100, gray=False):
    width = new_width
    image = None
    try:
        image = Image.open(image_filepath)
    except Exception as e:
        print(f"Unable to open image file {image_filepath}.")
        print(e)
        return
    if gray==False:
        image_ascii = convert_image_to_ascii(image, new_width)
        print(image_ascii)
    else:
        image_ascii = convert_to_grayscale(image)
        image_ascii = convert_image_to_ascii(image, new_width)
        print(image_ascii)

if __name__=='__main__':
    import sys

    if len(sys.argv) == 2:
        image_file_path = sys.argv[1]
        print(image_file_path)
        handle_image_conversion(image_file_path)

    elif len(sys.argv) == 4:
        image_file_path = sys.argv[1]
        scale_size = sys.argv[2]
        gray_bool = bool(sys.argv[3])

        print(image_file_path)
        handle_image_conversion(image_file_path, int(scale_size), gray_bool)

    else:
        print("Incorrect number of arguments")