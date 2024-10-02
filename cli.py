import sys
from PIL import Image
from streamlit_app import convert_image_to_ascii, ASCII_CHARS

def handle_image_conversion(image_path, output_path=None):
    try:
        with Image.open(image_path) as img:
            ascii_art = convert_image_to_ascii(img, 100, ASCII_CHARS)
            if output_path:
                with open(output_path, 'w') as f:
                    f.write(ascii_art)
                print(f"ASCII art saved to {output_path}")
            else:
                print(ascii_art)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python cli.py <image_path> [output_path]")
        sys.exit(1)

    image_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    handle_image_conversion(image_path, output_path)