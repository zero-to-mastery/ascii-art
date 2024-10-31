import argparse
import io
import os
import random

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageOps


def get_image_from_bytes(byte_contents: bytes) -> Image:
    """_summary_

    Args:
        byte_contents (bytes): Input image bytes.

    Returns:
        Image: Output image.
    """
    return Image.open(io.BytesIO(byte_contents)).convert('RGBA')

def get_image_from_path(image_path: str) -> Image:
    """_summary_

    Args:
        image_path (str): Input image path.

    Returns:
        Image: Output image.
    """
    return Image.open(image_path).convert('RGBA')


def get_invert_colors_image(input_image: Image) -> Image:
    """_summary_
    
    Args:
        input_image (Image): Input image.

    Returns:
        Image: Output image.
    """

    # Apply invert effect
    inverted_img = ImageOps.invert(input_image.convert("RGB"))  # Invert RGB channels
    inverted_img = Image.merge("RGBA", (*inverted_img.split()[:3], input_image.split()[3]))  # Restore the alpha channel

    return inverted_img

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a color-inverted image from an input image.")
    parser.add_argument("--input", "-i", type=str, help="Path to the input image.")
    parser.add_argument("--output", "-o", type=str, help="Path to save the output color-inverted image. (default value: None, and it will 'Show')", default=None)

    args = parser.parse_args()
    
    # check 'input' argument
    if not args.input:
        import sys
        print("No input file provided!")
        sys.exit(1)
        
    original_img = get_image_from_path(args.input)
    inverted_img = get_invert_colors_image(original_img)
        
    if args.output:
        inverted_img.save(args.output, 'PNG')
    else:
        plt.imshow(inverted_img)
        plt.axis('off')
        plt.show()  
        
# Example:
# 1. python3 invert-color-art.py -i example/ztm-logo.png
# 3. python3 invert-color-art.py -i example/ztm-logo.png -o inverted-color-art.png   