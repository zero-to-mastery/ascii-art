import typer
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
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


def create_contours(image):
    return image.filter(ImageFilter.FIND_EDGES)


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