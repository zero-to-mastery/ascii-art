# this project requires Pillow installation: https://pillow.readthedocs.io/en/stable/installation.html

#code credit goes to: https://www.hackerearth.com/practice/notes/beautiful-python-a-simple-ascii-art-generator-from-images/
#code modified to work with Python 3 by @aneagoie
from PIL import Image

help_msg = """
Usage  : python community-version.py [option] [input_file]
Options:
         no options will run the default ASCII_CHARS
    -r   reverse the ASCII_CHARS
    -s   save the output to file (by default the output file is [input_file]_output.txt)
    -rs  save the reversed output to file
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

def handle_image_conversion(image_filepath, arg=""):
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


    if arg == "-s":
        output_name = image_file_path.split('.')[0] + "_output.txt" 
        try:
            f = open(output_name, "w")
            f.write(image_ascii)
            f.close
            print(f"Image saved to -> {output_name}")
        except:
            print("An error occured!")
            return False

def check_file(f):
    allowed_inputs_file = ["png"]
    try:
        if f.split('.')[-1] in allowed_inputs_file:
            return True
        else:
            return False
    except:
        print(help_msg)
        return False

def check_inputs():
    arguments = [x for x in sys.argv]
    if 2 > len(arguments) or len(arguments) > 3 or check_file(arguments[-1]) == False:
        print(help_msg)
        return False
    elif len(arguments) == 2 and check_file(arguments[-1]):
        return ""
    elif len(arguments) == 3 and arguments[1] == "-r" and check_file(arguments[-1]):
        return arguments[1]
    elif len(arguments) == 3 and arguments[1] == "-s" and check_file(arguments[-1]):
        return arguments[1]
    elif len(arguments) == 3 and arguments[1] == "-rs" and check_file(arguments[-1]):
        return arguments[1]


if __name__ == '__main__':
    import sys

    todo = check_inputs()
    ASCII_CHARS = [ '#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']

    if todo == "":
        image_file_path = sys.argv[1]
        print(image_file_path)
        handle_image_conversion(image_file_path)
    elif todo == '-r':
        ASCII_CHARS = [ '#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@'][::-1]
        image_file_path = sys.argv[2]
        print(image_file_path)
        handle_image_conversion(image_file_path)
    elif todo == "-s":
        image_file_path = sys.argv[2]
        print(image_file_path)
        handle_image_conversion(image_file_path, "-s")
    elif todo == "-rs":
        ASCII_CHARS = [ '#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@'][::-1]
        image_file_path = sys.argv[2]
        print(image_file_path)
        handle_image_conversion(image_file_path, "-s")
