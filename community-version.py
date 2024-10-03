import streamlit as st
from PIL import Image, ImageOps, ImageFilter
import numpy as np
import argparse
import os

# ASCII character
ASCII_CHARS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']

# Convert image to grayscale
def convert_to_grayscale(image: Image.Image) -> Image.Image:
    return image.convert('L')


# Resize image to fit the new width while maintaining aspect ratio
def scale_image(image: Image.Image, new_width: int) -> Image.Image:
    (original_width, original_height) = image.size
    aspect_ratio = original_height / float(original_width)
    new_height = int(aspect_ratio * new_width * 0.55)
    new_image = image.resize((new_width, new_height))
    return new_image


# Map pixels to ASCII characters
def map_pixels_to_ascii_chars(image: Image.Image, ascii_chars: list, range_width: int = 25) -> str:
    pixels_in_image = list(image.getdata())
    ascii_str = [ascii_chars[int(pixel_value / range_width)] for pixel_value in pixels_in_image]
    return "".join(ascii_str)


# Convert image to ASCII art (grayscale)
def convert_image_to_ascii(image: Image.Image, new_width: int) -> str:
    image = scale_image(image, new_width)
    image = convert_to_grayscale(image)
    ascii_str = map_pixels_to_ascii_chars(image, ASCII_CHARS)
    ascii_len = len(ascii_str)
    ascii_image = [ascii_str[i:i + new_width] for i in range(0, ascii_len, new_width)]
    return "\n".join(ascii_image)


# Generate colored ASCII art using HTML and inline styles for RGB color mapping
def convert_to_colored_ascii_html(image: Image.Image, new_width: int) -> str:
    image = scale_image(image, new_width)
    pixels = np.array(image) # (height, width, 3)

    ascii_image_html = """
    <div style='overflow-x: auto; white-space: nowrap; max-width: 100%;'>
    <pre style='font-family: monospace; line-height: 1; letter-spacing: 0;'>
    """

    for row in pixels:
        for pixel in row:
            ascii_char = ASCII_CHARS[int(np.mean(pixel) / 255 * (len(ASCII_CHARS) - 1))]
            ascii_image_html += f"<span style='color:rgb({pixel[0]},{pixel[1]},{pixel[2]})'>{ascii_char}</span>"
        ascii_image_html += "<br>"

    ascii_image_html += "</pre></div>"
    return ascii_image_html


# Command-line interface for running the project via terminal
def handle_image_conversion(image_filepath, new_width=100, color=False, invert=False, blur=False, edge=False):
    try:
        image = Image.open(image_filepath)

        # Apply filters
        if invert:
            image = ImageOps.invert(image.convert('RGB'))
        if blur:
            image = image.filter(ImageFilter.BLUR)
        if edge:
            image = image.filter(ImageFilter.FIND_EDGES)

        if color:
            # Generate colored ASCII art (only displayed in HTML)
            ascii_art_html = convert_to_colored_ascii_html(image, new_width)
            html_output = f"{os.path.splitext(image_filepath)[0]}_ascii_art.html"
            with open(html_output, "w") as f:
                f.write(ascii_art_html)
            print(f"Colored ASCII art saved as: {html_output}")
        else:
            # Generate grayscale ASCII art
            ascii_art = convert_image_to_ascii(image, new_width)
            print(ascii_art)
            text_output = f"{os.path.splitext(image_filepath)[0]}_ascii_art.txt"
            with open(text_output, "w") as f:
                f.write(ascii_art)
            print(f"Grayscale ASCII art saved as: {text_output}")
    except Exception as e:
        print(f"Unable to open image file: {image_filepath}")
        print(e)


# Streamlit interface
def run_streamlit_app():
    st.title("🎨 ASCII-Art Generator")

    # Sidebar for settings
    st.sidebar.title("Settings")
    width = st.sidebar.slider("Set ASCII Art Width", 50, 150, 100)
    color_mode = st.sidebar.checkbox("Enable Colored ASCII Art")
    invert_colors = st.sidebar.checkbox("Invert Colors")
    apply_blur = st.sidebar.checkbox("Apply Blur Filter")
    apply_edge = st.sidebar.checkbox("Apply Edge Detection Filter")

    # File upload for images
    uploaded_file = st.file_uploader("Upload an image (JPEG/PNG)", type=["jpg", "jpeg", "png"])

    # Display the original image and show ASCII art preview
    if uploaded_file:
        image = Image.open(uploaded_file)

        # Apply filters based on user choices
        if invert_colors:
            image = ImageOps.invert(image.convert('RGB'))
        if apply_blur:
            image = image.filter(ImageFilter.BLUR)
        if apply_edge:
            image = image.filter(ImageFilter.FIND_EDGES)

        # Display original image
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Generate ASCII art
        if color_mode:
            st.subheader("Colored ASCII Art Preview:")
            ascii_art_html = convert_to_colored_ascii_html(image.convert('RGB'), width)
            st.markdown(ascii_art_html, unsafe_allow_html=True)
        else:
            st.subheader("Grayscale ASCII Art Preview:")
            ascii_art = convert_image_to_ascii(image, width)
            st.text(ascii_art)

        # Download options
        if color_mode:
            # For colored ASCII art, allow download as HTML
            st.download_button(
                label="Download ASCII Art as HTML",
                data=ascii_art_html,
                file_name="ascii_art.html",
                mime="text/html"
            )
        else:
            # For grayscale ASCII art, download as plain text
            st.download_button(
                label="Download ASCII Art as .txt",
                data=ascii_art,
                file_name="ascii_art.txt",
                mime="text/plain"
            )

    # Instructions
    st.markdown("""
        - 🎨 Adjust the settings in the sidebar to create unique ASCII art.
        - ✏️ Use the toggle to apply filters or switch to colored ASCII art.
        - 💾 Save your ASCII art for later by downloading the text file or HTML file.
    """)


# Command-line argument parser for CLI usage
def main():
    parser = argparse.ArgumentParser(description="Generate ASCII art from an image.")
    parser.add_argument("image_filepath", help="Path to the image file")
    parser.add_argument("--width", type=int, default=100, help="Width of the ASCII art (default: 100)")
    parser.add_argument("--color", action="store_true", help="Enable colored ASCII art (HTML output)")
    parser.add_argument("--invert", action="store_true", help="Invert colors")
    parser.add_argument("--blur", action="store_true", help="Apply blur filter")
    parser.add_argument("--edge", action="store_true", help="Apply edge detection filter")
    args = parser.parse_args()

    handle_image_conversion(args.image_filepath, new_width=args.width, color=args.color,
                            invert=args.invert, blur=args.blur, edge=args.edge)


if __name__ == "__main__":
    try:
        # If no command-line arguments are passed, run Streamlit app
        if len(os.sys.argv) == 1:
            run_streamlit_app()
        else:
            main()
    except Exception as e:
        print(f"Error: {e}")
