# ASCII Art Generator - Features

## Streamlit Web Application

1. **Image Input Options**
   - Upload images (JPG, PNG, JPEG)
   - Draw custom images using an interactive canvas

2. **Drawing Tools** (for custom image creation)
   - Freehand drawing
   - Line tool
   - Rectangle tool
   - Circle tool
   - Transform tool
   - Adjustable stroke width and color
   - Customizable background color
   - Option to use a background image

3. **Image Preprocessing**
   - Edge detection option
   - Normal Image option

4. **ASCII Art Generation**
   - Adjustable ASCII art width
   - Custom ASCII character input option

5. **Output Display**
   - Display of original image and ASCII art
   - Text-based ASCII art output

6. **Download Options**
   - Download ASCII art as a text file

7. **User Interface**
   - Streamlit-based responsive web interface
   - Sidebar for controls and settings

8. **Additional Features**
   - Random ASCII art fun facts displayed in the sidebar

## Command-Line Tool

To use the command-line tool with the provided image, you would run the following command in your terminal:
```bash
python main.py <image_path>
```
This will generate the ASCII art and print it to the console. If you want to save the output to a file, you can add an output file path:
```bash
python main.py <image_path> [output_path]
```

## Using the Streamlit App
To use the Streamlit app, first run the app with:
```bash
streamlit run main.py
```

## Shared Features

1. **Image Processing**
   - Image scaling while maintaining aspect ratio
   - Grayscale conversion

2. **ASCII Conversion**
   - Pixel to ASCII character mapping
   - Customizable ASCII character set

3. **Flexibility**
   - Can be run as a web app or command-line tool from the same codebase

## Technical Features

1. **Python-based Implementation**
   - Utilizes popular libraries like Pillow, NumPy, and OpenCV

2. **Modular Design**
   - Separate modules for Streamlit app, command-line tool, and core functionality

3. **Extensibility**
   - Easy to add new features or modify existing ones

4. **Cross-platform Compatibility**
   - Works on Windows, macOS, and Linux

This ASCII Art Generator combines the power of a user-friendly web interface with the flexibility of a command-line tool, providing a versatile solution for creating ASCII art from images or custom drawings.