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
        
def handle_image_conversion(image_filepath, save):
    image = None
    try:
        image = Image.open(image_filepath)
    except Exception as e:
        print(f"Unable to open image file {image_filepath}.")
        print(e)
        return

    image_ascii = convert_image_to_ascii(image)
    print(image_ascii)
    if save == 1:
        write_image_to_text_file(image_ascii)

if __name__=='__main__':
    import sys

    image_file_path = sys.argv[1]
    if sys.argv[2]:
        handle_image_conversion(image_file_path, 1)
    print(image_file_path)
    handle_image_conversion(image_file_path, 0)
