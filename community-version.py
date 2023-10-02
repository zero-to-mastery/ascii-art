# this project requires Pillow installation: https://pillow.readthedocs.io/en/stable/installation.html

# code credit goes to: https://www.hackerearth.com/practice/notes/beautiful-python-a-simple-ascii-art-generator-from-images/
# code modified to work with Python 3 by @aneagoie

from PIL import Image

ASCII_CHARS = ['#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']

def scale_image(image, new_width=100):
    """Resizes an image while preserving the aspect ratio."""
    (original_width, original_height) = image.size
    aspect_ratio = original_height / float(original_width)
    new_height = int(aspect_ratio * new_width)
    new_image = image.resize((new_width, new_height))
    return new_image

def convert_to_grayscale(image):
    """Converts an image to grayscale."""
    return image.convert('L')

def map_pixels_to_ascii_chars(image, range_width=25, brightness=1.0):
    """Maps pixel values to ASCII characters based on a specified range and brightness."""
    pixels_in_image = list(image.getdata())
    adjusted_pixels = [int(pixel_value * brightness) for pixel_value in pixels_in_image]
    pixels_to_chars = [ASCII_CHARS[int(pixel_value / range_width)] for pixel_value in adjusted_pixels]
    return "".join(pixels_to_chars)

def convert_image_to_ascii(image, brightness=1.0):
    """Converts an image to ASCII art with adjustable brightness."""
    image = scale_image(image)
    image = convert_to_grayscale(image)
    pixels_to_chars = map_pixels_to_ascii_chars(image, brightness=brightness)
    len_pixels_to_chars = len(pixels_to_chars)
    image_ascii = [pixels_to_chars[index: index + 100] for index in range(0, len_pixels_to_chars, 100)]
    return "\n".join(image_ascii)

def handle_image_conversion(image_filepath, output_file_path='output.txt', brightness=1.0):
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

    image_ascii = convert_image_to_ascii(image, brightness=brightness)
    print(image_ascii)
    
    if output_file_path:
        save_ascii_art_to_file(image_ascii, output_file_path)
        print(f"ASCII art saved to {output_file_path}")

def save_ascii_art_to_file(image_ascii, output_file_path):
    """Saves the ASCII art to a file."""
    with open(output_file_path, 'w') as f:
        f.write(image_ascii)

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python script.py <image_file_path> [output_file_path] [brightness]")
    else:
        image_file_path = sys.argv[1]
        output_file_path = sys.argv[2] if len(sys.argv) > 2 else 'output.txt'
        brightness = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0

        handle_image_conversion(image_file_path, output_file_path, brightness)
