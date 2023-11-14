# this project requires Pillow installation: https://pillow.readthedocs.io/en/stable/installation.html

#code credit goes to: https://www.hackerearth.com/practice/notes/beautiful-python-a-simple-ascii-art-generator-from-images/
#code modified to work with Python 3 by @aneagoiefrom PIL import Image
from PIL import Image
import tkinter


ASCII_CHARS = ['#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']

def scale_image(image, new_width):
    """Resizes an image preserving the aspect ratio.
    """
    (original_width, original_height) = image.size
    aspect_ratio = original_height *.6 /float(original_width)
    new_height = int(aspect_ratio * new_width)

    new_image = image.resize((new_width, new_height))
    return new_image

def convert_to_grayscale(image):
    return image.convert('L')

def map_pixels_to_ascii_chars(image, range_width=25):
    """Maps each pixel to an ASCII char based on the range in which it lies."""
    pixels_in_image = list(image.getdata())
    pixels_to_chars = [ASCII_CHARS[int(pixel_value / range_width)] for pixel_value in pixels_in_image]
    return "".join(pixels_to_chars)

def convert_image_to_ascii(image, new_width):
    image = scale_image(image, new_width)
    image = convert_to_grayscale(image)
    pixels_to_chars = map_pixels_to_ascii_chars(image)
    len_pixels_to_chars = len(pixels_to_chars)
    image_ascii = [pixels_to_chars[index: index + new_width] for index in
        range(0, len_pixels_to_chars, new_width)]

    return "\n".join(image_ascii)

def handle_image_conversion(image_filepath):
    image = None
    try:
        image = Image.open(image_filepath)
    except Exception as e:
        print(f"Unable to open image file {image_filepath}.")
        print(e)
        return

    image_size = image.size
    print(f"Original Image size: {image_size[0]} (width) x {image_size[1]} (height)")

    new_width = covert_raw_image_size_width(image_size)

    image_ascii = convert_image_to_ascii(image, new_width)
    create_popup(image_ascii)
    print(image_ascii)

def covert_raw_image_size_width(image_size):
    width_multiplier = width_multiplier_formula(image_size)
    new_width = int(image_size[0] * width_multiplier)
    return new_width

def width_multiplier_formula(image_size):
    width_pixels = int(image_size[0])

    if 0 < width_pixels <= 500:#good
        return 0.17
    elif 501 < width_pixels <= 750:
        return 0.15
    elif 751 < width_pixels <= 1000:
        return 0.13
    elif 1001 < width_pixels <= 1250: #good
        return 0.11
    elif 1251 < width_pixels <= 1500:
        return 0.09
    elif 1501 < width_pixels <= 1750:
        return 0.082
    elif 1751 < width_pixels <= 2000:  # good
        return 0.078
    elif 2001 < width_pixels <= 2250:
        return 0.055
    elif 2251 < width_pixels <= 2500:  # good
        return 0.02
    else:
        return 0.01


def create_popup(image_ascii):
    popup = tkinter.Tk()
    popup.title("Custom Popup")
    custom_font = ("Courier", 6)
    label_text = image_ascii
    label = tkinter.Label(popup, text=label_text, font=custom_font)
    label.pack(padx=20, pady=20)
    popup.mainloop()





if __name__ == '__main__':
    # image_file_path = sys.argv[1] # Uncomment this line after code is working
    #image_file_path = "vegan.png"
    #image_file_path = "raaghav.png"
    #image_file_path = "ztm-logo.png"
    image_file_path = "mountain.png"
    #image_file_path = "NORAH.jpg"
    #image_file_path = "raaghavHigh.png"

    print(image_file_path)
    handle_image_conversion(image_file_path)
