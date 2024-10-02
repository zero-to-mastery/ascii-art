import streamlit as st
from PIL import Image
import numpy as np
from streamlit_drawable_canvas import st_canvas
import cv2

# ASCII characters
ASCII_CHARS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']

# Scaling the image while maintaining the aspect ratio
def scale_image(image, new_width):
    (original_width, original_height) = image.size
    aspect_ratio = original_height / float(original_width)
    new_height = int(aspect_ratio * new_width * 0.55)
    new_image = image.resize((new_width, new_height))
    return new_image

# Image to grayscale
def convert_to_grayscale(image):
    return image.convert('L')

# Pixels to ASCII characters
def map_pixels_to_ascii_chars(image, ascii_chars=ASCII_CHARS, range_width=25):
    pixels_in_image = list(image.getdata())
    pixels_to_chars = [ascii_chars[int(pixel_value / range_width)] for pixel_value in pixels_in_image]
    return "".join(pixels_to_chars)

# Image to ASCII art
def convert_image_to_ascii(image, new_width, ascii_chars=ASCII_CHARS):
    image = scale_image(image, new_width)
    image = convert_to_grayscale(image)
    pixels_to_chars = map_pixels_to_ascii_chars(image, ascii_chars)
    len_pixels_to_chars = len(pixels_to_chars)
    ascii_image = [pixels_to_chars[index: index + new_width] for index in range(0, len_pixels_to_chars, new_width)]
    return "\n".join(ascii_image)

# Edge Detection
def apply_edge_detection(image):
    img_array = np.array(image)
    edges = cv2.Canny(img_array, 100, 200)
    return Image.fromarray(edges)

def main():
    st.set_page_config(page_title="ASCII Art Generator", layout="wide")
    st.title("🎨 ASCII Art Generator")
    st.sidebar.header("Controls")
    uploaded_image = st.sidebar.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
    draw_image = st.sidebar.checkbox("Draw your own image")

    if draw_image:
        # Create two columns for drawing tools
        col1, col2 = st.columns(2)

        with col1:
            drawing_mode = st.selectbox("Drawing tool:", ("freedraw", "line", "rect", "circle", "transform"))
            stroke_width = st.slider("Stroke width: ", 1, 25, 3)
        with col2:
            stroke_color = st.color_picker("Stroke color:")
            bg_color = st.color_picker("Background color: ", "#eee")

        bg_image = st.file_uploader("Background image:", type=["png", "jpg"])

        # Canvas
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
        # Image preprocessing
        apply_edge = st.sidebar.checkbox("Apply Edge Detection")
        if apply_edge:
            image = apply_edge_detection(image)

        # ASCII Art settings
        new_width = st.sidebar.slider("Adjust ASCII art width", min_value=50, max_value=300, value=100)
        ascii_chars = st.sidebar.text_input("Custom ASCII characters (optional)", value="".join(ASCII_CHARS))
        ascii_chars = list(ascii_chars) if ascii_chars else ASCII_CHARS

        # Generate ASCII Art
        if st.sidebar.button("Generate ASCII Art"):
            st.write("Generating ASCII art...")

            ascii_art = convert_image_to_ascii(image, new_width, ascii_chars)

            # Display original image and ASCII art in two rows
            st.subheader("Original Image")
            st.image(image, caption='Original Image', use_column_width=True)

            st.subheader("ASCII Art")
            st.text(ascii_art)

            # Download options
            st.markdown("### Download Options")
            st.download_button(
                label="Download ASCII Art as Text",
                data=ascii_art,
                file_name="ascii_art.txt",
                mime="text/plain",
            )

    # Fun facts
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Fun Fact about ASCII Art")
    fun_facts = [
        "ASCII art began in the early days of computers when graphical interfaces weren’t available, using characters to create images.",
        "Artists use a set of 128 ASCII characters to form images, making creativity essential due to these constraints.",
        "ASCII art is not just for visual pleasure; it has been used in early computer games and even for data compression!",
        "ASCII art inspired modern emoticons and eventually evolved into emojis and kaomoji.",
    ]
    st.sidebar.write(np.random.choice(fun_facts))


if __name__ == "__main__":
    main()