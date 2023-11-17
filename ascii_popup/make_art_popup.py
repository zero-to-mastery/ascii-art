# this project requires Pillow installation: https://pillow.readthedocs.io/en/stable/installation.html

#code credit goes to: https://www.hackerearth.com/practice/notes/beautiful-python-a-simple-ascii-art-generator-from-images/
#code modified to work with Python 3 by @aneagoiefrom PIL import Image
from PIL import Image
import tkinter

ASCII_CHARS = ['#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']

font_size_dict = {1: [2, .67], 2: [6, 0.62], 3: [10, 0.49], 4: [14, 0.53]}
"""Key values match the selection the user makes and the value in index 0
 id for font size  and index 1 is for character_aspect_ratio """


def validate_font_input(font_input_string):
    """
    Args:
        font_input_string: The input the user has for their font size selection
    Return :
        valid_font_input: an integer value converted for the string that the user has input
        True: If guess is an integer in range a True value is returned to break the loop in the program
        False: If a guess is string or invalid range to keep the loop recurring till a correct guess is given
        None: if there is an invalid selection a None value is assigned to show Font selection has no valid value
    Raises:
        :ValueError
            :If a string is entered a ValueError is raised
    """
    try:
        valid_font_input = int(font_input_string)
        valid_range = range(min(font_size_dict), max(font_size_dict) + 1)
        if valid_font_input in valid_range:
            return True, valid_font_input
        else:
            print("Font size selection must be between 1 and 4.")
            return False, None
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return False, None


def validate_width_input(width_input_string):
    """
    Args:
        width_input_string: The input the user has for how many characters wide they want their ASCII art
    Return :
        valid_width_input: an integer value converted for the string that the user has input
        True: If guess is an integer in range a True value is returned to break the loop in the program
        False: If a guess is string or invalid character to keep the loop recurring till a correct guess is given
        None: if there is an invalid selection a None value is assigned to show Font selection has no valid value
    Raises:
        :ValueError
            :If a string is entered a ValueError is raised
     """
    try:
        valid_width_input = int(width_input_string)
        return True, valid_width_input
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return False, None


def scale_image(image, new_width, character_aspect_ratio):
    """
    Resizes an image preserving the aspect ratio.

    Args:
        image: The image that the user has selected for their ASCII art
        new_width: A integer value for the width of how many characters the user wants to have for their ASCII art
        character_aspect_ratio: a float value that adjust the height of the ASCII art to suit the width of the
        ASCII art.
    Return :
        new_image: the image resized to be used is ASCII conversion
    """

    original_width = image.size[0]
    original_height = image.size[1]
    aspect_ratio = original_height / original_width
    new_height = int(new_width * aspect_ratio * character_aspect_ratio)
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
    image = scale_image(image, new_width, character_aspect_ratio)
    image = convert_to_grayscale(image)
    pixels_to_chars = map_pixels_to_ascii_chars(image)
    len_pixels_to_chars = len(pixels_to_chars)
    image_ascii = [pixels_to_chars[index: index + new_width] for index in
        range(0, len_pixels_to_chars, new_width)]
    return "\n".join(image_ascii)


def handle_image_conversion(image_filepath):
    try:
        image = Image.open(image_filepath)
    except Exception as e:
        print(f"Unable to open image file {image_filepath}.")
        print(e)
        return

    image_ascii = convert_image_to_ascii(image, new_width)
    create_popup(image_ascii)


def create_popup(image_ascii):
    """
      Creates a pop-up window of the users ASCII art work there is no unit test for this as the function is just
      applying values to the attributes of the instance of the tkinter object. The image_ascii variable is just a
      string that can contain any type of characters as defined in the ASCII_CHARS list. The conversion is
      handled by convert_image_to_ascii function.

      Args:
         image_ascii: The image that the user has selected for their ASCII art
      Return :
          Pop-up window of the users ASCII art
      """
    popup = tkinter.Tk()
    popup.title("ASCII art")
    popup_font = ("Courier", font_size)
    label_text = image_ascii
    label = tkinter.Label(popup, text=label_text, font=popup_font)
    label.pack(padx=20, pady=20)
    popup.mainloop()


if __name__ == '__main__':
    import sys

    valid_width_input = False
    while not valid_width_input:
        width_input_string = input("How many characters wide do you want the ASCII art :")
        valid_width_input, new_width = validate_width_input(width_input_string)

    valid_font_input = False
    while not valid_font_input:
        font_input_string = input("What font size do you want the ASCII art ?\n"
                                  "1 = Small, 2 = Medium, 3 = Large and 4 = extra large :")
        valid_font_input, font_selection = validate_font_input(font_input_string)

    if valid_font_input:
        selected_font = font_size_dict[font_selection]
        font_size = selected_font[0]
        character_aspect_ratio = selected_font[1]

    image_file_path = sys.argv[1]
    handle_image_conversion(image_file_path)

