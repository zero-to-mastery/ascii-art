# ASCII Art Generator

Welcome to the **ASCII Art Generator**! This tool converts images into beautiful ASCII art, available via both a command-line interface and a web interface powered by **Streamlit**. 

---

## Web Interface (Streamlit)

### Running the Web Interface
To start the web interface, run:
```bash
streamlit run community-version.py
```
This will open the ASCII Art Generator web app in your browser, where you can upload an image or draw your own, and customize the ASCII output.

### Features Available in the Web Interface:
1. **Upload or Draw Image**: Upload an image or use the drawing canvas to create custom artwork.
2. **Customization Options**:
   - **Width**: Set the ASCII art width in characters.
   - **Brightness and Contrast**: Adjust brightness and contrast for desired effects.
   - **Edge Detection**: Enhance outlines for sharper ASCII representations.
3. **Preview & Download**: View and download generated ASCII art as a `.txt` file.
4. **Fun Facts Sidebar**: Learn fun facts about ASCII art.

---

## Command-Line Interface (CLI)

### Running the CLI
To use the ASCII Art Generator from the command line:
```bash
python community-version.py <input_image> --output <output_file>
```
### CLI Options
| Option                              | Description                                                                    | Default              |
|-------------------------------------|--------------------------------------------------------------------------------|----------------------|
| `<input_image>`                     | Path to the input image file (JPEG or PNG).                                    | Required             |
| `--output <output_file>`            | Output file path (`.txt` for grayscale ASCII or `.html` for colorized).        | N/A                  |
| `--pattern {basic, complex, emoji}` | Select ASCII pattern.                                                          | `basic`              |
| `--width <int>`                     | Width of ASCII art in characters.                                              | `100`                |
| `--brightness <float>`              | Adjust brightness (0.5 - 2.0).                                                 | `1.0`                |
| `--contrast <float>`                | Adjust contrast (0.5 - 2.0).                                                   | `1.0`                |
| `--blur`                            | Apply a blur filter.                                                           | Disabled             |
| `--sharpen`                         | Apply a sharpen filter.                                                        | Disabled             |
| `--colorize`                        | Enable colorized ASCII art.                                                    | Disabled (grayscale) |
| `--theme {neon, pastel, grayscale}` | Color theme for colorized ASCII art; requires `--colorize`.                    | `grayscale`          |

---

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ascii-art
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

