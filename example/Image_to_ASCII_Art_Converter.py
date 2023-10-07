from PIL import Image

# Define the ASCII characters to represent different shades of gray
ASCII_CHARS = "@%#*+=-:. "

# Resize the image and convert it to grayscale
def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width / 1.65
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def image_to_ascii(image, new_width=100):
    image = resize_image(image)
    grayscale_image = image.convert("L")  # Convert to grayscale
    pixels = grayscale_image.getdata()
    ascii_str = ""
    for pixel_value in pixels:
        ascii_str += ASCII_CHARS[pixel_value // 25]  # Map pixel value to ASCII character
    return ascii_str

# Save the ASCII art to a text file
def save_ascii_to_file(ascii_art, output_file):
    with open(output_file, "w") as f:
        f.write(ascii_art)

# Load an image, convert it to ASCII art, and save it to a file
if __name__ == "__main__":
    image_path = "your_image.jpg"  # Replace with the path to your image
    output_file = "output.txt"  # Replace with the desired output file name
    
    try:
        image = Image.open(image_path)
        ascii_art = image_to_ascii(image)
        save_ascii_to_file(ascii_art, output_file)
        print(f"ASCII art saved to {output_file}")
    except Exception as e:
        print(f"Error: {e}")
