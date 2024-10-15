# Features

## Installation

Before using the ASCII Art Generator, ensure you have the following dependencies installed in your Python environment:

### Required Python Libraries

1. **Pillow**: For image processing and manipulation.
2. **Numpy**: For efficient numerical operations.
3. **OpenCV**: For edge detection.
4. **Streamlit**: To create the web-based interface.
5. **Streamlit Drawable Canvas**: For drawing functionality in the web app.

### Installation Command

To install all the required libraries, run the following command:

```bash
pip install Pillow numpy opencv-python streamlit streamlit-drawable-canvas
```

If you are using a virtual environment, make sure to activate it before running the above command.

---

## ASCII Art Generator

The **ASCII Art Generator** is a Python-based project that converts images into text-based ASCII art. It includes both a command-line interface and a Streamlit-based web interface for generating and downloading ASCII art. The project supports various image manipulation features and customization options.

### Key Features

### 1. **Command-Line Interface (CLI)**
   - Convert any image file (JPEG, PNG) to ASCII art via the command line.
   - Example usage:
     ```bash
     python community-version.py <image_path> [output_path]
     ```
   - **Parameters**:
     - `image_path`: The path to the input image file.
     - `output_path` *(optional)*: The file path where the generated ASCII art will be saved as text. If not provided, the ASCII art will be printed to the console.

### 2. **Streamlit Web App**
   - Interactive web interface built with **Streamlit**.
   - **Upload or Draw** your own image on a canvas and convert it into ASCII art.
   - Adjustable parameters for **image width** and **custom ASCII characters**.
   - Preview the original image and the generated ASCII art side by side.
   - **Edge Detection** feature to apply an edge-detection filter before converting to ASCII art.
   - **Download** generated ASCII art as a `.txt` file.

### 3. **Customizable ASCII Characters**
   - Users can provide custom ASCII characters to generate the art.
   - By default, the following characters are used: `@`, `#`, `S`, `%`, `?`, `*`, `+`, `;`, `:`, `,`, `.`.

### 4. **Edge Detection**
   - Apply edge detection on the uploaded image using **OpenCV** before converting it to ASCII art.
   - Enhances the outlines of the image for sharper ASCII art representations.

### 5. **Image Processing**
   - The image is **scaled** while preserving its aspect ratio before being converted to ASCII art.
   - Converts the image to **grayscale** for effective mapping to ASCII characters.

### 6. **Drawing Canvas**
   - Integrated drawing feature where users can:
     - **Freely draw**, or create shapes such as lines, rectangles, and circles.
     - Customize **stroke color** and **background color**.
   - Converts the drawn image into ASCII art directly from the canvas.

### 7. **Fun Facts Sidebar**
   - The web app includes fun facts about ASCII art, providing an educational component to the user interface.

### 8. **Cross-Platform Compatibility**
   - Works on Windows, Mac, and Linux systems with the appropriate Python environment.
   - Easily installed using `pip` for all dependencies.

### Example
**CLI Example**:
```bash
python community-version.py example/ztm-logo.png
```

**Streamlit App**:
```bash
streamlit run community-version.py
```
