# Usage Instructions for ASCII Art Generator

## Installation Instructions
To run this project, you need to have Python installed on your machine.  
Install the required libraries by running the following command in your terminal or command prompt:

```bash
pip install streamlit Pillow numpy
```

## Command-Line Usage Instructions
To generate ASCII art from the command line, navigate to the directory where your script is located and run:

```bash
python main.py <image_file_path> [--width <width>] [--color] [--invert] [--blur] [--edge]
```

**Examples:**
1. To specify the width of the ASCII art (for example, 120 characters wide):
   ```bash
   python main.py example/ztm-logo.png --width 120
   ```

2. To generate colored ASCII art (output will be saved as HTML):
   ```bash
   python main.py example/ztm-logo.png --color
   ```
   
3. To invert the colors:
   ```bash
   python community-version.py example/ztm-logo.png --invert
   ```
   
4. To apply a blur effect:
   ```bash
   python community-version.py example/ztm-logo.png --blur
   ```

5. To apply edge detection:
   ```bash
   python community-version.py example/ztm-logo.png --edge
   ```


## Streamlit App Usage Instructions
To run the Streamlit web application, use the following command in your terminal:

```bash
streamlit run community-version.py
```

This will start a local web server. You can open your browser to the URL shown in the terminal (usually `http://localhost:8501`) to access the app.

Once the app is running, you can upload an image and customize settings from the sidebar to generate ASCII art.
