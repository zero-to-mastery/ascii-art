import streamlit as st
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import numpy as np
import random
import argparse
import sys

# ASCII patterns and color themes
ASCII_PATTERNS = {
    'basic': ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.'],
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


# Function to dynamically adjust aspect ratio based on ASCII pattern
def get_aspect_ratio(pattern: str) -> float:
    if pattern == 'basic':
        return 0.55  # Basic ASCII characters have a slight vertical aspect
    elif pattern == 'complex':
        return 0.65  # Complex characters are usually wider
    elif pattern == 'emoji':
        return 1.0   # Emojis are generally square, so no aspect correction
    return 0.55


# Function to resize the image dynamically based on the aspect ratio of the selected pattern
def resize_image(image: Image.Image, width: int, pattern: str) -> Image.Image:
    aspect_ratio = get_aspect_ratio(pattern)
    new_height = int(aspect_ratio * image.height / image.width * width)
    return image.resize((width, new_height))


# Function to map pixels to ASCII characters
def map_pixels_to_ascii(image: Image.Image, pattern: list) -> str:
    grayscale_image = image.convert('L')  # Convert to grayscale
    pixels = np.array(grayscale_image)

    # Ensure that the index for the ASCII pattern doesn't go out of bounds
    ascii_chars = np.vectorize(lambda pixel: pattern[min(pixel // (256 // len(pattern)), len(pattern) - 1)])(pixels)

    ascii_image = "\n".join(["".join(row) for row in ascii_chars])
    return ascii_image


# Function to create colorized ASCII art in HTML format
def create_colorized_ascii_html(image: Image.Image, pattern: list, theme: str) -> str:
    image = resize_image(image, 80, 'basic')  # Resizing for better ASCII mapping
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

    # Image filters
    brightness = st.sidebar.slider("Brightness", 0.5, 2.0, 1.0)
    contrast = st.sidebar.slider("Contrast", 0.5, 2.0, 1.0)
    apply_blur = st.sidebar.checkbox("Apply Blur")
    apply_sharpen = st.sidebar.checkbox("Apply Sharpen")

    # Upload image
    uploaded_file = st.file_uploader("Upload an image (JPEG/PNG)", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)

        # Apply filters to the image
        image = apply_image_filters(image, brightness, contrast, apply_blur, apply_sharpen)

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


# Command Line Interface (CLI) Function
def run_cli(input_image: str, output: str, pattern_type: str, width: int, brightness: float, contrast: float,
            blur: bool, sharpen: bool, colorize: bool, theme: str):
    image = Image.open(input_image)

    # Apply filters
    image = apply_image_filters(image, brightness, contrast, blur, sharpen)

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



def main():
    parser = argparse.ArgumentParser(description="Generate ASCII Art from an image.")
    parser.add_argument('input_image', type=str, help='Path to the input image (JPEG/PNG)')
    parser.add_argument('--output', type=str, default='output.txt', help='Path to save the generated ASCII art')
    parser.add_argument('--pattern', type=str, default='basic', choices=ASCII_PATTERNS.keys(),
                        help='Choose an ASCII pattern (basic, complex, emoji)')
    parser.add_argument('--width', type=int, default=100, help='Width of the ASCII art')
    parser.add_argument('--brightness', type=float, default=1.0, help='Brightness adjustment')
    parser.add_argument('--contrast', type=float, default=1.0, help='Contrast adjustment')
    parser.add_argument('--blur', action='store_true', help='Apply blur filter')
    parser.add_argument('--sharpen', action='store_true', help='Apply sharpen filter')
    parser.add_argument('--colorize', action='store_true', help='Enable colorized ASCII art')
    parser.add_argument('--theme', type=str, default='grayscale', choices=COLOR_THEMES.keys(),
                        help='Choose a color theme for colorized ASCII art')

    args = parser.parse_args()

    # Run the CLI mode if executed from command line
    run_cli(args.input_image, args.output, args.pattern, args.width, args.brightness, args.contrast,
            args.blur, args.sharpen, args.colorize, args.theme)


if __name__ == "__main__":

    # Check if the script is being run with command-line arguments
    if len(sys.argv) > 1:
        main()  # Run the CLI mode
    else:
        try:
            run_streamlit_app()  # Run the Streamlit app
        except:
            main()  # Fallback to CLI mode if Streamlit fails
