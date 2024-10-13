import streamlit as st
from PIL import Image, ImageOps, ImageEnhance, ImageFilter, ImageDraw, ImageFont
import numpy as np
import random
import argparse
import sys

# ASCII patterns and color themes
ASCII_PATTERNS = {
    'basic': ['@', '#', 'S', '%', '?', '*', '+', '-', '/', ';', ':', ',', '.'],
    'complex': ['▓', '▒', '░', '█', '▄', '▀', '▌', '▐', '▆', '▇', '▅', '▃', '▂'],
    'emoji': ['😁', '😎', '🤔', '😱', '🤩', '😏', '😴', '😬', '😵', '😃'],
}

COLOR_THEMES = {
    'neon': [(57, 255, 20), (255, 20, 147), (0, 255, 255)],
    'pastel': [(255, 179, 186), (255, 223, 186), (186, 255, 201), (186, 225, 255)],
    'grayscale': [(i, i, i) for i in range(0, 255, 25)],
}

# Function to apply filters to the image
def apply_image_filters(image: Image.Image, brightness: float, contrast: float, blur: bool,
                        sharpen: bool) -> Image.Image:
    if brightness != 1.0:
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(brightness)

    if contrast != 1.0:
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(contrast)

    if blur:
        image = image.filter(ImageFilter.BLUR)

    if sharpen:
        image = image.filter(ImageFilter.SHARPEN)

    return image

# Function to create contours
def create_contours(image: Image.Image) -> Image.Image:
    return image.filter(ImageFilter.FIND_EDGES)

# Function to flip image
def flip_image(image: Image.Image, flip_horizontal: bool, flip_vertical: bool) -> Image.Image:
    if flip_horizontal:
        image = ImageOps.mirror(image)  # Flip horizontally
    if flip_vertical:
        image = ImageOps.flip(image)  # Flip vertically
    return image

# Function to dynamically adjust aspect ratio based on ASCII pattern
def get_aspect_ratio(pattern: str) -> float:
    if pattern == 'basic':
        return 0.55
    elif pattern == 'complex':
        return 0.65
    elif pattern == 'emoji':
        return 1.0
    return 0.55

# Function to resize the image dynamically based on the aspect ratio of the selected pattern
def resize_image(image: Image.Image, width: int, pattern: str) -> Image.Image:
    aspect_ratio = get_aspect_ratio(pattern)
    new_height = int(aspect_ratio * image.height / image.width * width)
    return image.resize((width, new_height))

# Function to map pixels to ASCII characters
def map_pixels_to_ascii(image: Image.Image, pattern: list) -> str:
    grayscale_image = image.convert('L')
    pixels = np.array(grayscale_image)
    ascii_chars = np.vectorize(lambda pixel: pattern[min(pixel // (256 // len(pattern)), len(pattern) - 1)])(pixels)
    ascii_image = "\n".join(["".join(row) for row in ascii_chars])
    return ascii_image

# Function to create colorized ASCII art in HTML format
def create_colorized_ascii_html(image: Image.Image, pattern: list, theme: str) -> str:
    image = resize_image(image, 80, 'basic')
    pixels = np.array(image)

    ascii_image_html = """
    <div style='font-family: monospace; white-space: pre;'>
    """

    color_palette = COLOR_THEMES.get(theme, COLOR_THEMES['grayscale'])

    for row in pixels:
        for pixel in row:
            ascii_char = pattern[int(np.mean(pixel) / 255 * (len(pattern) - 1))]
            color = random.choice(color_palette)
            ascii_image_html += f"<span style='color:rgb({color[0]},{color[1]},{color[2]})'>{ascii_char}</span>"
        ascii_image_html += "<br>"

    ascii_image_html += "</div>"
    return ascii_image_html

# Streamlit app for the ASCII art generator
def run_streamlit_app():
    st.title("🌟 Customizable ASCII Art Generator")

    # Sidebar for options and settings
    st.sidebar.title("Settings")
    pattern_type = st.sidebar.selectbox("Choose ASCII Pattern", options=['basic', 'complex', 'emoji'])
    colorize = st.sidebar.checkbox("Enable Colorized ASCII Art")
    color_theme = st.sidebar.selectbox("Choose Color Theme", options=list(COLOR_THEMES.keys()))
    width = st.sidebar.slider("Set ASCII Art Width", 50, 150, 100)

    # New Flip Image Feature
    flip_horizontal = st.sidebar.checkbox("Flip Image Horizontally")
    flip_vertical = st.sidebar.checkbox("Flip Image Vertically")

    # Image filters
    brightness = st.sidebar.slider("Brightness", 0.5, 2.0, 1.0)
    contrast = st.sidebar.slider("Contrast", 0.5, 2.0, 1.0)
    apply_blur = st.sidebar.checkbox("Apply Blur")
    apply_sharpen = st.sidebar.checkbox("Apply Sharpen")
    
    # New Contour Feature
    apply_contours = st.sidebar.checkbox("Apply Contours")

    # Upload image
    uploaded_file = st.file_uploader("Upload an image (JPEG/PNG)", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)

        # Apply filters to the image
        image = apply_image_filters(image, brightness, contrast, apply_blur, apply_sharpen)

        # Apply contour effect if selected
        if apply_contours:
            image = create_contours(image)

        # Flip the image if requested
        image = flip_image(image, flip_horizontal, flip_vertical)

        # Display the original processed image
        st.image(image, caption="Processed Image", use_column_width=True)

        # Resize the image based on the pattern type's aspect ratio
        image_resized = resize_image(image, width, pattern_type)

        # Generate ASCII art
        ascii_pattern = ASCII_PATTERNS[pattern_type]
        if colorize:
            st.subheader("Colorized ASCII Art Preview:")
            ascii_html = create_colorized_ascii_html(image_resized, ascii_pattern, color_theme)
            st.markdown(ascii_html, unsafe_allow_html=True)
        else:
            st.subheader("Grayscale ASCII Art Preview:")
            ascii_art = map_pixels_to_ascii(image_resized, ascii_pattern)
            st.text(ascii_art)

        # Download options
        if colorize:
            st.download_button("Download ASCII Art as HTML", ascii_html, file_name="ascii_art.html", mime="text/html")
        else:
            st.download_button("Download ASCII Art as Text", ascii_art, file_name="ascii_art.txt", mime="text/plain")

    # Instructions for the user
    st.markdown("""
        - 🎨 Use the **Settings** panel to customize your ASCII art with patterns, colors, and image filters.
        - 📤 Upload an image in JPEG or PNG format to start generating your ASCII art.
        - 💾 Download your creation as a **text file** or **HTML** for colorized output.
    """)

# Check if the file path is valid
def is_valid_image_path(file_path: str) -> bool:
    if not os.path.exists(file_path):
        return False
    if not os.path.isfile(file_path):
        return False
    return True


# Command Line Interface (CLI) Function
def run_cli(input_image: str, output: str, pattern_type: str, width: int, brightness: float, contrast: float,
            blur: bool, sharpen: bool, colorize: bool, theme: str, apply_contours: bool):
    image = Image.open(input_image)

    # Apply filters
    image = apply_image_filters(image, brightness, contrast, blur, sharpen)

    # Apply contour effect if selected
    if apply_contours:
        image = create_contours(image)

    # Resize image
    image_resized = resize_image(image, width, pattern_type)

    # Generate ASCII art
    ascii_pattern = ASCII_PATTERNS[pattern_type]
    if colorize:
        ascii_html = create_colorized_ascii_html(image_resized, ascii_pattern, theme)
        with open(output, 'w', encoding='utf-8') as file:  # Use UTF-8 encoding
            file.write(ascii_html)
    else:
        ascii_art = map_pixels_to_ascii(image_resized, ascii_pattern)
        with open(output, 'w', encoding='utf-8') as file:  # Use UTF-8 encoding
            file.write(ascii_art)

    print(f"ASCII art saved to {output}")

# Main function for CLI execution
if __name__ == "__main__":
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description="Generate ASCII art from an image.")
        parser.add_argument("input_image", help="Path to the input image file.")
        parser.add_argument("-o", "--output", default="output.txt", help="Output file name.")
        parser.add_argument("-p", "--pattern", choices=ASCII_PATTERNS.keys(), default="basic", help="ASCII pattern.")
        parser.add_argument("-w", "--width", type=int, default=100, help="Width of ASCII art.")
        parser.add_argument("-b", "--brightness", type=float, default=1.0, help="Brightness factor.")
        parser.add_argument("-c", "--contrast", type=float, default=1.0, help="Contrast factor.")
        parser.add_argument("--blur", action="store_true", help="Apply blur effect.")
        parser.add_argument("--sharpen", action="store_true", help="Apply sharpen effect.")
        parser.add_argument("--colorize", action="store_true", help="Enable colorized ASCII art.")
        parser.add_argument("-t", "--theme", choices=COLOR_THEMES.keys(), default="grayscale", help="Color theme.")
        parser.add_argument("--contours", action="store_true", help="Apply contour effect to the image.")

        args = parser.parse_args()
        run_cli(args.input_image, args.output, args.pattern, args.width, args.brightness, args.contrast,
                 args.blur, args.sharpen, args.colorize, args.theme, args.contours)
    else:
        run_streamlit_app()
