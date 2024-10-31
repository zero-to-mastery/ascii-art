import sys
import os
from PIL import Image
import numpy as np
import streamlit as st
from typing import List

# Check FEATURES.md for installation guide before running the code

# ASCII characters for the command-line version and Streamlit app
ASCII_CHARS: List[str] = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']

# Image Scaling - Resizes an image while maintaining the aspect ratio
def scale_image(image: Image.Image, new_width: int = 100) -> Image.Image:
    (original_width, original_height) = image.size
    aspect_ratio: float = original_height / float(original_width)
    new_height: int = int(aspect_ratio * new_width * 0.55)
    new_image: Image.Image = image.resize((new_width, new_height))
    return new_image

# Convert image to grayscale
def convert_to_grayscale(image: Image.Image) -> Image.Image:
    return image.convert('L')

# Map pixels to ASCII characters
def map_pixels_to_ascii_chars(image: Image.Image, ascii_chars=ASCII_CHARS, range_width: int = 25) -> str:
    pixels_in_image: List[int] = list(image.getdata())
    pixels_to_chars: List[int] = [ascii_chars[int(pixel_value / range_width)] for pixel_value in pixels_in_image]
    return "".join(pixels_to_chars)

# Convert image to ASCII art
def convert_image_to_ascii(image: Image.Image, new_width: int = 100, ascii_chars=ASCII_CHARS) -> str:
    image = scale_image(image, new_width)
    image = convert_to_grayscale(image)
    pixels_to_chars = map_pixels_to_ascii_chars(image, ascii_chars)
    len_pixels_to_chars: int = len(pixels_to_chars)
    ascii_image: List[str] = [pixels_to_chars[index: index + new_width] for index in range(0, len_pixels_to_chars, new_width)]
    return "\n".join(ascii_image)

# Save ASCII art to a text file
def saving_image_to_txt(image_ascii, image_path):
    image_directory = os.path.dirname(image_path)
    if image_directory and not os.path.exists(image_directory):
        print(f"Directory '{image_directory}' does not exist. Attempting to create it...")
        try:
            os.makedirs(image_directory)
            print(f"Directory '{image_directory}' created successfully.")
        except Exception as e:
            print(f"Failed to create directory '{image_directory}. Error: {e}")
            return
    try:
        with open(image_path, "w") as f:
            f.write(image_ascii)
            print("ASCII art saved successfully.")
    except Exception as e:
        print(f"Failed to save ASCII art. Error: {e}")

# Edge detection using OpenCV
def apply_edge_detection(image: Image.Image) -> Image.Image:
    img_array = np.array(image)
    edges = cv2.Canny(img_array, 100, 200)
    return Image.fromarray(edges)

# Handle image conversion for CLI and Streamlit
def handle_image_conversion(image_path, output_path=None):
    try:
        with Image.open(image_path) as img:
            ascii_art = convert_image_to_ascii(img, 100, ASCII_CHARS)
            if output_path:
                saving_image_to_txt(ascii_art, output_path)
            else:
                print(ascii_art)
    except Exception as e:
        print(f"Error: {str(e)}")

# Streamlit main function for interactive ASCII art generation
def main():
    st.set_page_config(page_title="ASCII Art Generator", layout="wide")
    st.title("🎨 ASCII Art Generator")
    st.sidebar.header("Controls")
    uploaded_image = st.sidebar.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
    draw_image = st.sidebar.checkbox("Draw your own image")

    if draw_image:
        col1, col2 = st.columns(2)

        with col1:
            drawing_mode = st.selectbox("Drawing tool:", ("freedraw", "line", "rect", "circle", "transform"))
            stroke_width = st.slider("Stroke width: ", 1, 25, 3)
        with col2:
            stroke_color = st.color_picker("Stroke color:")
            bg_color = st.color_picker("Background color: ", "#eee")

        bg_image = st.file_uploader("Background image:", type=["png", "jpg"])

        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=stroke_width,
            stroke_color=stroke_color,
            background_color=bg_color,
            background_image=Image.open(bg_image) if bg_image else None,
            update_streamlit=True,
            height=500,
            width=700,
            drawing_mode=drawing_mode,
            key="canvas",
        )

        if canvas_result.image_data is not None:
            image = Image.fromarray(canvas_result.image_data.astype('uint8'))
        else:
            image = None
    elif uploaded_image is not None:
        image = Image.open(uploaded_image)
    else:
        image = None

    if image is not None:
        apply_edge = st.sidebar.checkbox("Apply Edge Detection")
        if apply_edge:
            image = apply_edge_detection(image)

        new_width = st.sidebar.slider("Adjust ASCII art width", min_value=50, max_value=300, value=100)
        ascii_chars = st.sidebar.text_input("Custom ASCII characters (optional)", value="".join(ASCII_CHARS))
        ascii_chars = list(ascii_chars) if ascii_chars else ASCII_CHARS

        if st.sidebar.button("Generate ASCII Art"):
            st.write("Generating ASCII art...")

            ascii_art = convert_image_to_ascii(image, new_width, ascii_chars)

            st.subheader("Original Image")
            st.image(image, caption='Original Image', use_column_width=True)

            st.subheader("ASCII Art")
            st.text(ascii_art)

            st.markdown("### Download Options")
            st.download_button(
                label="Download ASCII Art as Text",
                data=ascii_art,
                file_name="ascii_art.txt",
                mime="text/plain",
            )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Fun Fact about ASCII Art")
    fun_facts = [
        "ASCII art began in the early days of computers when graphical interfaces weren’t available, using characters to create images.",
        "Artists use a set of 128 ASCII characters to form images, making creativity essential due to these constraints.",
        "ASCII art is not just for visual pleasure; it has been used in early computer games and even for data compression!",
        "ASCII art inspired modern emoticons and eventually evolved into emojis and kaomoji.",
    ]
    st.sidebar.write(np.random.choice(fun_facts))

# Command-line execution and Streamlit app start
if __name__ == '__main__':
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else None
        handle_image_conversion(image_path, output_path)
    else:
        main()
