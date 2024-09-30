## Community Version

from PIL import Image

# List of ASCII characters to map pixel values to, ordered from darkest ('#') to lightest ('@')
ASCII_CHARS = ['#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']

def scale_image(image, new_width=100):
    """
    Resizes an image while preserving its aspect ratio.
    
    Parameters:
    - image: The original image to be resized.
    - new_width: The new width for the resized image (default is 100 pixels).

    Returns:
    - new_image: The resized image with the same aspect ratio as the original.
    """
    (original_width, original_height) = image.size  # Get original image dimensions
    aspect_ratio = original_height / float(original_width)  # Calculate aspect ratio
    new_height = int(aspect_ratio * new_width)  # Adjust height to preserve aspect ratio

    # Resize the image to the new dimensions
    new_image = image.resize((new_width, new_height))
    return new_image

def convert_to_grayscale(image):
    """
    Converts the given image to grayscale.

    Parameters:
    - image: The original image.

    Returns:
    - Grayscale version of the image.
    """
    return image.convert('L')  # 'L' mode is for grayscale in PIL

def map_pixels_to_ascii_chars(image, range_width=25):
    """
    Maps each pixel value to an ASCII character based on its intensity.
    
    Parameters:
    - image: Grayscale image where each pixel is a value between 0 (black) and 255 (white).
    - range_width: Defines how pixel values are divided into ranges (default is 25).

    Returns:
    - A string of ASCII characters representing the image.
    
    Explanation:
    - Pixel values (0-255) are divided into 11 ranges, each corresponding to an ASCII character.
    """
    # Get pixel values from the grayscale image
    pixels_in_image = list(image.getdata())
    
    # Map each pixel value to an ASCII character based on its intensity range
    pixels_to_chars = [ASCII_CHARS[int(pixel_value / range_width)] for pixel_value in pixels_in_image]

    # Join all ASCII characters into a single string
    return "".join(pixels_to_chars)

def convert_image_to_ascii(image, new_width=100):
    """
    Converts an image to ASCII art.
    
    Parameters:
    - image: The original image to be converted.
    - new_width: The new width of the ASCII art (default is 100 characters wide).

    Returns:
    - A string representing the image in ASCII art.
    """
    image = scale_image(image, new_width)  # Scale the image to fit the desired width
    image = convert_to_grayscale(image)  # Convert the image to grayscale

    # Map each pixel in the grayscale image to an ASCII character
    pixels_to_chars = map_pixels_to_ascii_chars(image)
    
    # Calculate the number of pixels to form each line based on the new width
    len_pixels_to_chars = len(pixels_to_chars)
    
    # Split the string of ASCII characters into rows to form the ASCII art
    image_ascii = [pixels_to_chars[index: index + new_width] for index in range(0, len_pixels_to_chars, new_width)]

    # Join the rows into a single string, separated by newline characters
    return "\n".join(image_ascii)

def handle_image_conversion(image_filepath):
    """
    Handles the entire process of converting an image file to ASCII art.
    
    Parameters:
    - image_filepath: The path to the image file that needs to be converted.
    
    This function:
    - Opens the image file.
    - Converts the image to ASCII art.
    - Prints the ASCII art to the console.
    """
    image = None
    try:
        # Try opening the image file
        image = Image.open(image_filepath)
    except Exception as e:
        # If there's an issue with opening the file, print an error message
        print(f"Unable to open image file {image_filepath}.")
        print(e)
        return

    # Convert the image to ASCII and print it
    image_ascii = convert_image_to_ascii(image)
    print(image_ascii)

if __name__ == '__main__':
    import sys

    # Get the image file path from command line arguments
    image_file_path = sys.argv[1]

    # Print the image file path for verification
    print(image_file_path)

    # Handle the image conversion process
    handle_image_conversion(image_file_path)
