import streamlit as st
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import numpy as np
import random

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
                        sharpen: bool, contours: bool) -> Image.Image:
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

    # Apply contour detection if selected
    if contours:
        image = image.filter(ImageFilter.FIND_EDGES)

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
    apply_contours = st.sidebar.checkbox("Apply Contour Detection")  # New checkbox for contours

    # Upload image
    uploaded_file = st.file_uploader("Upload an image (JPEG/PNG)", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file)

        # Apply filters to the image, including contour detection
        image = apply_image_filters(image, brightness, contrast, apply_blur, apply_sharpen, apply_contours)

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


if __name__ == "__main__":
    run_streamlit_app()
