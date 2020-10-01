# this project requires Pillow installation: https://pillow.readthedocs.io/en/stable/installation.html

# code credit goes to: https://www.hackerearth.com/practice/notes/beautiful-python-a-simple-ascii-art-generator-from-images/
# code modified to work with Python 3 by @aneagoie

# Example of run multiple image:
# python3 community-version.py example/ztm-logo.png example/one.png example/two.png

from PIL import Image

ASCII_CHARS = ['#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']


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
    # scale the width of image to 100px
    image = scale_image(image)
    # convert image into gray scale image
    image = convert_to_grayscale(image)
    # change gray scale image into ascii art
    pixels_to_chars = map_pixels_to_ascii_chars(image)
    len_pixels_to_chars = len(pixels_to_chars)

    image_ascii = [pixels_to_chars[index: index + new_width] for index in
                   range(0, len_pixels_to_chars, new_width)]

    return "\n".join(image_ascii)


def write_image_to_text_file(image_ascii, b):

    b = b[:-4]
    b = b + '_ASCII.txt'
    with open(b, "w") as f:
        f.write(image_ascii)


def handle_image_conversion(image_filepath):
    image = None
    try:
        # open image by Image by Pillow
        image = Image.open(image_filepath)
    except Exception as e:
        print(f"Unable to open image file {image_filepath}.")
        print(e)
        return
    # send image to convert_image_to_ascii function to convert
    image_ascii = convert_image_to_ascii(image)
    print(image_ascii)
    # send image and its path to write_image_to_text_file function to make the ascii art text file of the image
    write_image_to_text_file(image_ascii, image_filepath)


if __name__ == '__main__':
    import sys

    # The script can take multiple images and turns them into ASCII arts
    image_file_path = sys.argv[1:]
    # send them to handle-image-conversion function one by one
    for i in image_file_path:
        print(i)
        handle_image_conversion(i)
