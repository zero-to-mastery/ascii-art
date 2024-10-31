import typer
from PIL import Image, ImageEnhance, ImageFilter, ImageOps, ImageDraw, ImageFont
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import numpy as np
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
import colorsys
import random

app = typer.Typer()
console = Console()

ASCII_PATTERNS = {
    'basic': ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.'],
    'complex': ['▓', '▒', '░', '█', '▄', '▀', '▌', '▐', '▆', '▇', '▅', '▃', '▂'],
    'emoji': ['😁', '😎', '🤔', '😱', '🤩', '😏', '😴', '😬', '😵', '😃'],
    'numeric': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
}

COLOR_THEMES = {
    'neon': [(57, 255, 20), (255, 20, 147), (0, 255, 255)],
    'pastel': [(255, 179, 186), (255, 223, 186), (186, 255, 201), (186, 225, 255)],
    'grayscale': [(i, i, i) for i in range(0, 255, 25)],
}


def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)
    return image.resize((new_width, new_height))


def apply_image_filters(image, brightness, contrast, blur, sharpen):
    if brightness != 1.0:
        image = ImageEnhance.Brightness(image).enhance(brightness)
    if contrast != 1.0:
        image = ImageEnhance.Contrast(image).enhance(contrast)
    if blur:
        image = image.filter(ImageFilter.BLUR)
    if sharpen:
        image = image.filter(ImageFilter.SHARPEN)
    return image

def text_to_image(text, canvas_width, canvas_height):
    image = Image.new('RGB', (canvas_width, canvas_height), color='white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    text_width, text_height = draw.textsize(text, font=font)
    position = ((canvas_width - text_width) / 2,
                (canvas_height - text_height) / 2)
    draw.text(position, text, fill='black', font=font)
    return image

# Function to flip image
def flip_image(image: Image.Image, flip_horizontal: bool, flip_vertical: bool) -> Image.Image:
    if flip_horizontal:
        image = ImageOps.mirror(image)  # Flip horizontally
    if flip_vertical:
        image = ImageOps.flip(image)  # Flip vertically
    return image

def create_ascii_art(image, pattern, colorize=False, theme='grayscale'):
    ascii_chars = ASCII_PATTERNS[pattern]
    ascii_art = []
    pixels = np.array(image)

    for y in range(image.height):
        line = []
        for x in range(image.width):
            pixel = pixels[y, x]
            char_index = int(np.mean(pixel) / 255 * (len(ascii_chars) - 1))
            char = ascii_chars[char_index]
            if colorize:
                color = random.choice(COLOR_THEMES[theme])
                line.append(f"[color rgb({color[0]},{color[1]},{color[2]})]" + char + "[/color]")
            else:
                line.append(char)
        ascii_art.append("".join(line))

    return "\n".join(ascii_art)

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

def create_contours(image):
    return image.filter(ImageFilter.FIND_EDGES)

# Streamlit app for the ASCII art generator
def run_streamlit_app():
    st.title("🌟 Customizable ASCII Art Generator")
    page = st.sidebar.selectbox('ASCII Art', ['Image', 'Live'])
    if page == "Image":
        # Sidebar for options and settings
        st.sidebar.title("Settings")
        pattern_type = st.sidebar.selectbox("Choose ASCII Pattern", options=[
                                            'basic', 'complex', 'emoji'])
        colorize = st.sidebar.checkbox("Enable Colorized ASCII Art")
        color_theme = st.sidebar.selectbox(
            "Choose Color Theme", options=list(COLOR_THEMES.keys()))
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
        uploaded_file = st.file_uploader(
            "Upload an image (JPEG/PNG)", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            image = Image.open(uploaded_file)
            # Apply filters to the image
            image = apply_image_filters(
                image, brightness, contrast, apply_blur, apply_sharpen)
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
                ascii_html = create_colorized_ascii_html(
                    image_resized, ascii_pattern, color_theme)
                st.markdown(ascii_html, unsafe_allow_html=True)
            else:
                st.subheader("Grayscale ASCII Art Preview:")
                ascii_art = map_pixels_to_ascii(image_resized, ascii_pattern)
                st.text(ascii_art)
            # Download options
            if colorize:
                st.download_button("Download ASCII Art as HTML", ascii_html,
                                   file_name="ascii_art.html", mime="text/html")
            else:
                st.download_button("Download ASCII Art as Text", ascii_art,
                                   file_name="ascii_art.txt", mime="text/plain")
        # Instructions for the user
        st.markdown("""
            - 🎨 Use the **Settings** panel to customize your ASCII art with patterns, colors, and image filters.
            - 📤 Upload an image in JPEG or PNG format to start generating your ASCII art.
            - 💾 Download your creation as a **text file** or **HTML** for colorized output.
        """)
    elif page == "Live":
        st.markdown("""
            **Note**: 
                Click the **`START`** button and allow the camera permissions.
        """)
        webrtc_ctx = webrtc_streamer(
            key="video-sendonly",
            mode=WebRtcMode.SENDONLY,
            media_stream_constraints={"video": True},
        )
        image_place = st.empty()
        while True:
            if webrtc_ctx.video_receiver:
                try:
                    video_frame = webrtc_ctx.video_receiver.get_frame(
                        timeout=1)
                except Exception as e:
                    print(e)
                    break
                img_rgb = video_frame.to_ndarray(format="rgb24")
                image = Image.fromarray(img_rgb)
                image_resized = resize_image(image, 100, "basic")
                ascii_art = map_pixels_to_ascii(
                    image_resized, ASCII_PATTERNS["basic"])
                image_place.text(ascii_art)


@app.command()
def generate(
        image_path: str = typer.Argument(..., help="Path to the input image"),
        width: int = typer.Option(100, help="Width of the ASCII art"),
        pattern: str = typer.Option("basic", help="ASCII pattern to use"),
        colorize: bool = typer.Option(False, help="Generate colorized ASCII art"),
        theme: str = typer.Option("grayscale", help="Color theme for colorized output"),
        brightness: float = typer.Option(1.0, help="Brightness adjustment"),
        contrast: float = typer.Option(1.0, help="Contrast adjustment"),
        blur: bool = typer.Option(False, help="Apply blur effect"),
        sharpen: bool = typer.Option(False, help="Apply sharpen effect"),
        contours: bool = typer.Option(False, help="Apply contour effect"),
        invert: bool = typer.Option(False, help="Invert the image"),
        output: str = typer.Option(None, help="Output file path")
):
    """Generate ASCII art from an image with various customization options."""

    with Progress() as progress:
        task = progress.add_task("[green]Processing image...", total=100)

        # Load and process the image
        image = Image.open(image_path)
        progress.update(task, advance=20)

        image = resize_image(image, width)
        progress.update(task, advance=20)

        image = apply_image_filters(image, brightness, contrast, blur, sharpen)
        progress.update(task, advance=20)

        if contours:
            image = create_contours(image)

        if invert:
            image = ImageOps.invert(image.convert('RGB'))
        progress.update(task, advance=20)

        ascii_art = create_ascii_art(image, pattern, colorize, theme)
        progress.update(task, advance=20)

    # Display or save the result
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(ascii_art)
        console.print(f"ASCII art saved to {output}")
    else:
        console.print(Panel(ascii_art, title="ASCII Art", expand=False))


if __name__ == "__main__":
    app()