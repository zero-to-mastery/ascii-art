import argparse
import base64
import io
import os
import platform
import random
import sys
from typing import List

import imageio.v3 as iio
import numpy as np
import streamlit as st
from PIL import (Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont,
                 ImageOps, ImageSequence)

# ASCII patterns and color themes
ASCII_PATTERNS = {
    "basic": ["@", "#", "S", "%", "?", "*", "+", "-", "/", ";", ":", ",", "."],
    "complex": ["▓", "▒", "░", "█", "▄", "▀", "▌", "▐", "▆", "▇", "▅", "▃", "▂"],
    "emoji": ["😁", "😎", "🤔", "😱", "🤩", "😏", "😴", "😬", "😵", "😃"],
    "numeric": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
}

COLOR_THEMES = {
    "indigo": [(75, 0, 130), (255, 20, 147), (0, 255, 255)],
    "neon": [(57, 255, 20), (255, 20, 147), (0, 255, 255)],
    "pastel": [(255, 179, 186), (255, 223, 186), (186, 255, 201), (186, 225, 255)],
    "grayscale": [(i, i, i) for i in range(0, 255, 25)],
    "cherry_blossom": [(255, 204, 229), (255, 102, 178), (255, 0, 127), (204, 0, 102)],
    "northern_lights": [(0, 255, 255), (0, 204, 153), (153, 0, 204), (255, 0, 255)],
}


def get_terminal_size():
    """Returns the width and height of the terminal in characters."""
    return os.get_terminal_size().columns, os.get_terminal_size().lines


def resize_image_for_terminal(image: Image.Image, pattern: str) -> Image.Image:
    """Resizes the image based on terminal size while maintaining aspect ratio."""
    terminal_width, _ = get_terminal_size()
    aspect_ratio = get_aspect_ratio(pattern)
    new_width = min(terminal_width, image.width)
    new_height = int(aspect_ratio * image.height / image.width * new_width)
    return image.resize((new_width, new_height))


def apply_image_filters(
    image: Image.Image, brightness: float, contrast: float, blur: bool, sharpen: bool
) -> Image.Image:
    """Applies brightness, contrast, blur, and sharpen filters to the image."""
    if brightness != 1.0:
        image = ImageEnhance.Brightness(image).enhance(brightness)
    if contrast != 1.0:
        image = ImageEnhance.Contrast(image).enhance(contrast)
    if blur:
        image = image.filter(ImageFilter.BLUR)
    if sharpen:
        image = image.filter(ImageFilter.SHARPEN)
    return image


def create_contours(image: Image.Image) -> Image.Image:
    """Creates contours for the image."""
    return image.filter(ImageFilter.FIND_EDGES)


def flip_image(
    image: Image.Image, flip_horizontal: bool, flip_vertical: bool
) -> Image.Image:
    """Flips the image horizontally and/or vertically."""
    if flip_horizontal:
        image = ImageOps.mirror(image)
    if flip_vertical:
        image = ImageOps.flip(image)
    return image


def get_aspect_ratio(pattern: str) -> float:
    """Dynamically adjusts aspect ratio based on ASCII pattern."""
    if pattern == "basic":
        return 0.55
    elif pattern == "complex":
        return 0.65
    elif pattern == "emoji":
        return 1.0
    return 0.55


def resize_image(image: Image.Image, width: int, pattern: str) -> Image.Image:
    """Resizes the image based on the aspect ratio of the selected pattern."""
    aspect_ratio = get_aspect_ratio(pattern)
    new_height = int(aspect_ratio * image.height / image.width * width)
    return image.resize((width, new_height))


# resizes the image based on the original image's aspect ratios
def preserve_resize_image(image: Image.Image, width: int) -> Image.Image:
    original_aspect_ratio = image.height / image.width
    new_height = int(width * original_aspect_ratio)
    return image.resize((width, new_height))


def map_pixels_to_ascii_with_colors(image: Image.Image, pattern: list):
    """Maps pixels to ASCII characters and captures colors."""
    grayscale_image = image.convert("L")
    grayscale_pixels = np.array(grayscale_image)
    ascii_chars = np.vectorize(
        lambda pixel: pattern[min(pixel // (256 // len(pattern)), len(pattern) - 1)]
    )(grayscale_pixels)
    ascii_image = "\n".join(["".join(row) for row in ascii_chars])
    return ascii_image, np.array(
        image
    )  # Return both ASCII characters and color information


def create_colorized_ascii_html(image: Image.Image, pattern: list, theme: str) -> str:
    """Creates colorized ASCII art in HTML format."""
    image = resize_image(image, 80, "basic")
    pixels = np.array(image)
    ascii_image_html = "<div style='font-family: monospace; white-space: pre;'>"
    color_palette = COLOR_THEMES.get(theme, COLOR_THEMES["grayscale"])

    for row in pixels:
        for pixel in row:
            ascii_char = pattern[int(np.mean(pixel) / 255 * (len(pattern) - 1))]
            color = random.choice(color_palette)
            ascii_image_html += f"<span style='color:rgb({color[0]},{color[1]},{color[2]})'>{ascii_char}</span>"
        ascii_image_html += "<br>"

    ascii_image_html += "</div>"
    return ascii_image_html


def process_gif_frames_to_ascii_with_colors(
    gif_image: Image.Image, pattern: list, width, pattern_type: str
):
    """Processes GIF frames and converts them to colorized ASCII art."""
    frames = []
    colors = []

    for frame in gif_image:
        resized_frame = resize_image(frame.convert("RGB"), width, pattern_type)
        ascii_frame, frame_colors = map_pixels_to_ascii_with_colors(
            resized_frame, pattern
        )
        frames.append(ascii_frame)
        colors.append(frame_colors)

    return frames, colors


def convert_ascii_to_new_image_with_colors(
    frame: str, pattern_type: str, colors: np.array, colorize=None
):
    """Converts ASCII frame to a colorized image."""
    image = Image.new("RGB", (800, 600), color="white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    max_char_width, max_char_height = calculate_char_size(font, pattern_type)

    y_offset = 0
    for i, line in enumerate(frame.splitlines()):
        x_offset = 0
        for j, char in enumerate(line):
            if colorize:
                pixel_color = tuple(int(c) for c in colors[i, j])
                draw.text((x_offset, y_offset), char, fill=pixel_color, font=font)
            else:
                draw.text((x_offset, y_offset), char, fill="black", font=font)
            x_offset += max_char_width
        y_offset += max_char_height

    return image


def calculate_char_size(font, pattern_type: str):
    """Calculates the maximum character size based on the font."""
    ascii_chars = ASCII_PATTERNS[pattern_type]
    max_char_width = max(font.getbbox(char)[2] for char in ascii_chars)
    max_char_height = max(font.getbbox(char)[3] for char in ascii_chars)
    return max_char_width, max_char_height


def save_new_images_to_gif(images: list, duration: int):
    """Saves ASCII images back into a GIF."""
    gif_output = io.BytesIO()
    images[0].save(
        gif_output,
        format="GIF",
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0,
    )
    gif_output.seek(0)
    return gif_output


# Function to map pixels to ASCII characters
def map_pixels_to_ascii(image: Image.Image, pattern: list) -> str:
    grayscale_image = image.convert("L")
    pixels = np.array(grayscale_image)
    ascii_chars = np.vectorize(
        lambda pixel: pattern[min(pixel // (256 // len(pattern)), len(pattern) - 1)]
    )(pixels)
    ascii_image = "\n".join(["".join(row) for row in ascii_chars])
    return ascii_image


def create_colored_ascii_art_image(
    ascii_text: str, font: ImageFont.ImageFont, color_theme
) -> Image.Image:
    # Split the ASCII text into lines
    lines = ascii_text.splitlines()

    # Calculate the width and height of the image based on the font size
    max_line_length = max(len(line) for line in lines)
    char_width = int(font.getlength("A"))
    char_height = int(font.getlength("A"))
    image_width = char_width * max_line_length + 20  # Add some padding
    image_height = char_height * len(lines) + 20  # Add some padding

    # Create a new image with a white background
    image = Image.new("RGB", (image_width, image_height), color="white")

    # Initialize the drawing context
    draw = ImageDraw.Draw(image)
    colors = COLOR_THEMES[color_theme]

    # Start drawing text line by line, keeping alignment
    y_position = 10  # Start drawing at 10 pixels from the top
    for line in lines:
        x_position = 10  # Start drawing each line at 10 pixels from the left
        for char in line:
            # Generate a random color
            # Draw the character with the random color
            random_color = random.choice(colors)
            draw.text((x_position, y_position), char, fill=random_color, font=font)
            x_position += char_width  # Move to the next character position
        y_position += char_height  # Move to the next line

    return image


# function to get default monospace font from system
def get_monospace_font():
    # Determine the font path based on the operating system
    os_name = platform.system()
    if os_name == "Windows":
        font_path = "C:\\Windows\\Fonts\\cour.ttf"  # Courier New font
    elif os_name == "Darwin":  # macOS
        font_path = "/System/Library/Fonts/Menlo.ttc"  # Menlo font
    else:  # Assume Linux
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"  # DejaVu Sans Mono font
    # Load the font with a specified size
    font_size = 12
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        # Fallback to default font if the specified font is not found
        print(
            "Could not load the specified monospaced font. Falling back to default font."
        )
        font = ImageFont.load_default()
    return font


def create_gif(image_paths: List, output, animation_speed):
    images = []
    for i in image_paths:
        images.append(iio.imread(i))
    iio.imwrite(output, images, duration=animation_speed, loop=0)


def delete_temp_files(image_paths: List):
    for i in image_paths:
        os.remove(i)


def gif_loader(output):
    file_ = open(f"{output}", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()
    return data_url


def run_streamlit_app():
    """Runs the Streamlit application for generating ASCII art."""
    st.title("🌟 Customizable ASCII Art Generator")
    pattern_type, custom_set, colorize, color_theme, width, animate, animation_speed = (
        get_sidebar_options()
    )

    uploaded_file = st.file_uploader(
        "Upload an image (JPEG/PNG/GIF)", type=["jpg", "jpeg", "png", "gif"]
    )
    if uploaded_file:
        image = Image.open(uploaded_file)
        ascii_pattern = (
            validate_custom_set(custom_set)
            if custom_set
            else ASCII_PATTERNS[pattern_type]
        )

        if image.format == "GIF":
            process_gif(image, ascii_pattern, colorize, color_theme, width)
        else:
            process_image(
                image,
                ascii_pattern,
                colorize,
                color_theme,
                width,
                animate,
                animation_speed,
            )


def get_sidebar_options():
    """Gets options from the sidebar."""
    st.sidebar.title("Settings")
    pattern_type = st.sidebar.selectbox(
        "Choose ASCII Pattern", options=ASCII_PATTERNS.keys()
    )
    custom_set = st.sidebar.text_input("Custom ASCII Set (Optional)", max_chars=50)
    colorize = st.sidebar.checkbox("Enable Colorized ASCII Art")
    color_theme = st.sidebar.selectbox(
        "Choose Color Theme", options=list(COLOR_THEMES.keys())
    )
    if colorize:
        animate = st.sidebar.checkbox("Animate Ascii-Art")
        animation_speed = st.sidebar.slider("Animation Speed in ms", 100, 800, step=100)
    else:
        animate, animation_speed = 0, 100

    width = st.sidebar.slider("Set ASCII Art Width", 50, 150, 100)
    return (
        pattern_type,
        custom_set,
        colorize,
        color_theme,
        width,
        animate,
        animation_speed,
    )


def process_gif(image, ascii_pattern, colorize, color_theme, width):
    """Processes a GIF image."""
    durations = image.info["duration"]
    frames = []
    for frame in ImageSequence.Iterator(image):
        frame = frame.convert("RGB")
        frame = apply_image_filters(
            frame, 1.0, 1.0, False, False
        )  # No filters for simplicity
        frames.append(frame)

    git_output = save_new_images_to_gif(frames, durations)
    st.image(git_output, caption="Processed Gif", use_column_width=True)

    if colorize:
        ascii_html = create_colorized_ascii_html(image, ascii_pattern, color_theme)
        st.markdown(ascii_html, unsafe_allow_html=True)
    else:
        ascii_art, _ = map_pixels_to_ascii_with_colors(image, ascii_pattern)
        st.text(ascii_art)


def process_image(
    image, ascii_pattern, colorize, color_theme, width, animate, animation_speed
):
    """Processes a regular image."""
    image = apply_image_filters(
        image, 1.0, 1.0, False, False
    )  # No filters for simplicity
    st.image(image, caption="Processed Image", use_column_width=True)

    if colorize and animate:
        image_resized = preserve_resize_image(image, width)
    else:
        image_resized = resize_image(image, width, ascii_pattern)
    if colorize:
        if animate:
            ascii_text = map_pixels_to_ascii(image_resized, ascii_pattern)
            font = get_monospace_font()
            image_paths = []
            for i in range(5):
                image = create_colored_ascii_art_image(ascii_text, font, color_theme)
                path = f"image{i}.png"
                image.save(path)
                image_paths.append(path)
            if "temp" not in os.listdir():
                os.makedirs("temp")

            output_path = "temp/animated.gif"
            create_gif(image_paths, output_path, animation_speed)
            delete_temp_files(image_paths)
            st.subheader("Animated ASCII Art Preview:")
            st.markdown(
                f'<img src="data:image/gif;base64,{gif_loader(output_path)}" alt="output gif">',
                unsafe_allow_html=True,
            )

        else:

            ascii_html = create_colorized_ascii_html(
                image_resized, ascii_pattern, color_theme
            )
            st.markdown(ascii_html, unsafe_allow_html=True)
    else:
        ascii_art, _ = map_pixels_to_ascii_with_colors(image_resized, ascii_pattern)
        st.text(ascii_art)


def run_cli(
    input_image: str,
    output: str,
    pattern_type: str,
    brightness: float,
    contrast: float,
    blur: bool,
    sharpen: bool,
    colorize: bool,
    theme: str,
    apply_contours: bool,
    custom_set: str,
    width: int,
):
    """Runs the CLI function for generating ASCII art."""
    image = Image.open(input_image)
    image = apply_image_filters(image, brightness, contrast, blur, sharpen)
    image_resized = resize_image(image, width, pattern_type)
    ascii_pattern = (
        validate_custom_set(custom_set) if custom_set else ASCII_PATTERNS[pattern_type]
    )

    if colorize:
        ascii_html = create_colorized_ascii_html(image_resized, ascii_pattern, theme)
        with open(output, "w", encoding="utf-8") as file:
            file.write(ascii_html)
    else:
        ascii_art, _ = map_pixels_to_ascii_with_colors(image_resized, ascii_pattern)
        with open(output, "w", encoding="utf-8") as file:
            file.write(ascii_art)

    print(f"ASCII art saved to {output}")
    if not colorize:
        with open(output, "r", encoding="utf-8") as f:
            print(f.read())


def validate_custom_set(custom_set: str):
    """Validates the custom ASCII character set."""
    if not custom_set or len(custom_set) < 2:
        raise ValueError("Custom ASCII set must contain at least two characters.")
    if len(set(custom_set)) != len(custom_set):
        raise ValueError("Custom ASCII set must not contain duplicate characters.")
    return list(custom_set)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(
            description="Generate ASCII art from an image."
        )
        parser.add_argument("input_image", help="Path to the input image file.")
        parser.add_argument(
            "-o", "--output", default="output.txt", help="Output file name."
        )
        parser.add_argument(
            "-p",
            "--pattern",
            choices=ASCII_PATTERNS.keys(),
            default="basic",
            help="ASCII pattern.",
        )
        parser.add_argument(
            "-w", "--width", type=int, default=100, help="Width of ASCII art."
        )
        parser.add_argument(
            "-b", "--brightness", type=float, default=1.0, help="Brightness factor."
        )
        parser.add_argument(
            "-c", "--contrast", type=float, default=1.0, help="Contrast factor."
        )
        parser.add_argument("--blur", action="store_true", help="Apply blur effect.")
        parser.add_argument(
            "--sharpen", action="store_true", help="Apply sharpen effect."
        )
        parser.add_argument(
            "--colorize", action="store_true", help="Enable colorized ASCII art."
        )
        parser.add_argument(
            "-t",
            "--theme",
            choices=COLOR_THEMES.keys(),
            default="grayscale",
            help="Color theme.",
        )
        parser.add_argument(
            "--contours", action="store_true", help="Apply contour effect to the image."
        )
        parser.add_argument(
            "--custom-set", type=str, help="Custom ASCII character set to use"
        )

        args = parser.parse_args()
        ascii_pattern = (
            validate_custom_set(args.custom_set)
            if args.custom_set
            else ASCII_PATTERNS[args.pattern]
        )
        run_cli(
            args.input_image,
            args.output,
            args.pattern,
            args.brightness,
            args.contrast,
            args.blur,
            args.sharpen,
            args.colorize,
            args.theme,
            args.contours,
            args.custom_set,
            args.width,
        )
    else:
        run_streamlit_app()
