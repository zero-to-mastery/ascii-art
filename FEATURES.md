# ASCII Art Generator Project - FEATURES.md

## Introduction
This project converts images into ASCII art using Python. It uses the `Pillow` library to process images and map their pixel values to ASCII characters. The code has been enhanced with comments to make it more understandable, and instructions for creating a virtual environment and generating a `requirements.txt` file have been included.

---

## Features

### 1. **Convert Image to ASCII Art**
   - The project resizes the input image, converts it to grayscale, and maps each pixel to an ASCII character based on its brightness.
   - The resulting ASCII art is printed to the console in the form of characters that visually represent the original image.

### 2. **Comments for Better Understanding**
   - Detailed comments have been added to the code to explain each function and its purpose, making it easier to understand for future developers or collaborators.

### 3. **Virtual Environment Setup**
   - The project uses a virtual environment (`venv`) to manage dependencies. This ensures a clean and isolated environment for package installation.

### 4. **`requirements.txt` File**
   - The required dependencies for the project are captured in the `requirements.txt` file, making it easier for others to install the necessary packages.

### 5. **`.gitignore` File**
   - A `.gitignore` file has been added to the project to ensure that unnecessary or sensitive files are not included in version control.
   - This includes the virtual environment files, cache, and other temporary files.

---

## How to Run the Project (Step-by-Step Guide)

### 1. Clone the Repository
   First, clone the project from GitHub or download it to your local machine.

   ```bash
   git clone https://github.com/your-username/ascii-art-generator
   cd ascii-art-generator
   ```

### 2. Create a Virtual Environment
Create a virtual environment to manage the project's dependencies in an isolated space.

    ```bash
    python -m venv venv
    ```
### 3. Activate the Virtual Environment
#### On Windows:
    ```bash
    venv\Scripts\activate
    ```
#### On macOS/Linux:
    ```bash
    source venv/bin/activate
    ```
You should see (venv) in your terminal, indicating that the environment is active.

### 4. Install Dependencies
Install the required dependencies (such as Pillow) using the requirements.txt file:

    ```bash
    pip install -r requirements.txt
    ```
### 5. Run the Project
After installing the dependencies, you can run the script to convert an image into ASCII art. Pass the path to the image file as a command-line argument:

    ```bash
    python ascii_art.py /path/to/your/image.jpg
    ```
The output will be printed directly to the console in the form of ASCII art.

### 6. Deactivate the Virtual Environment (Optional)
Once you're done working in the project, you can deactivate the virtual environment by running:

    ```bash
    deactivate
    ```
## Modifications Made to the Original Code
### Comments Added:

Detailed comments were added to explain the purpose of each function and how the code works.
This makes the code more readable and easier to follow for developers who are new to the project.
Created requirements.txt:

The project dependencies were captured in the requirements.txt file using the following command:

    ```bash
    pip freeze > requirements.txt
    ```
This ensures that anyone running the project can install the exact same versions of the required packages.
Added .gitignore File:

The .gitignore file prevents committing unnecessary files to version control, such as:
    -  Virtual environment files
    -  Byte-compiled Python files
    -  OS-specific files (e.g., .DS_Store)