# ASCII Art Generator - Usage Guide

Welcome to the **ASCII Art Generator**! This tool allows you to convert images into beautiful ASCII art. You can use the provided web interface powered by **Streamlit** or generate ASCII art directly from the command line with a variety of customization options.

---

## Web Interface (Streamlit)

You can interact with the ASCII Art Generator using an easy-to-use web interface. This is ideal for those who want to quickly generate ASCII art without using the command line.

### Running the Web Interface

To start the web interface, run the following command:

```bash
streamlit run community-version.py
```

Once executed, this will open the ASCII Art Generator web app in your browser, where you can upload an image and customize the output.

### Features Available in the Web Interface:

- **Choose ASCII Pattern**: Select from `basic`, `complex`, or `emoji` patterns.
- **Image Filters**: Adjust the image's brightness, contrast, blur, or sharpen before converting.
- **Color Themes**: Choose color themes like `neon`, `pastel`, or `grayscale` for colorized ASCII art.
- **Download Options**: Download the generated ASCII art as a text file or an HTML file for colorized output.

## Command Line Interface (CLI)

For more flexibility and automation, you can use the command line interface (CLI) to generate ASCII art.

### Running the CLI

To run the tool from the command line, use the following syntax:

```bash
python community-version.py <input_image> --output <output_file> [OPTIONS]
```

### Required Arguments:

1. **`<input_image>`**: The path to the input image file (JPEG or PNG).
2. **`--output <output_file>`**: The name of the output file (either `.txt` for grayscale ASCII or `.html` for colorized ASCII).

---

## Options and Arguments

Here is a list of all available options and their descriptions:

| Option                | Description                                                                                  | Default            |
|-----------------------|----------------------------------------------------------------------------------------------|--------------------|
| `--output`            | Specifies the output file path. (Required)                                                   | N/A                |
| `--pattern {basic, complex, emoji}` | Selects the ASCII pattern to use.                                                | `basic`            |
| `--width <int>`       | Sets the width of the ASCII art in characters.                                                | `100`              |
| `--brightness <float>`| Adjusts the brightness of the image (range: 0.5 - 2.0).                                       | `1.0`              |
| `--contrast <float>`  | Adjusts the contrast of the image (range: 0.5 - 2.0).                                         | `1.0`              |
| `--blur`              | Applies a blur filter to the image.                                                           | Disabled           |
| `--sharpen`           | Applies a sharpen filter to the image.                                                        | Disabled           |
| `--colorize`          | Enables colorized ASCII art output.                                                           | Disabled (grayscale)|
| `--theme {neon, pastel, grayscale}` | Specifies the color theme for colorized ASCII art. This requires `--colorize`.    | `grayscale`        |

---

## Examples

Here are some examples of how to use the tool:

### Example 1: Generate Grayscale ASCII Art

```bash
python community-version.py example/ztm-logo.png --output ascii_art.txt
```

This will create a grayscale ASCII art version of the image and save it as `ascii_art.txt`.

### Example 2: Generate Colorized ASCII Art with Neon Theme

```bash
python community-version.py example/ztm-logo.png --output ascii_art.html --colorize --theme neon
```

This will generate a colorized ASCII art using the "neon" theme and save it as `ascii_art.html`.

### Example 3: Use Emoji Pattern with Custom Brightness and Contrast

```bash
python community-version.py example/ztm-logo.png --output ascii_art.html --pattern emoji --brightness 1.5 --contrast 1.8 --colorize --theme pastel
```

This command uses the emoji pattern, adjusts brightness and contrast, and outputs a pastel color-themed ASCII art in HTML format.

---

## Requirements

Ensure you have the following requirements installed:

- Python 3.x
- Pillow (`pip install pillow`)
- Numpy (`pip install numpy`)
- Streamlit (`pip install streamlit`)

You can install all dependencies using the `requirements.txt` file (if provided):

```bash
pip install -r requirements.txt
```

---

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd ascii-art
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/macOS
   venv\Scripts\activate     # For Windows
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

