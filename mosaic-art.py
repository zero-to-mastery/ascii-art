import argparse
import io

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw


def get_image_from_bytes(byte_contents: bytes) -> Image:
    """_summary_

    Args:
        byte_contents (bytes): Input image bytes.

    Returns:
        Image: Output image.
    """
    return Image.open(io.BytesIO(byte_contents)).convert("RGBA")


def get_image_from_path(image_path: str) -> Image:
    """_summary_

    Args:
        image_path (str): Input image path.

    Returns:
        Image: Output image.
    """
    return Image.open(image_path).convert("RGBA")


def get_mosaic_image(input_image: Image, block_size: int = 5) -> Image:
    """_summary_

    Args:
        input_image (Image): Input image.
        block_size (int, optional): Sidelength of a mosaic block. Defaults to 5.

    Returns:
        Image: Output image.
    """
    # read image in RGBA
    img = np.array(input_image)

    # get height and width of image
    height, width, _ = img.shape

    # create an empty image
    result_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))  # 初始化為完全透明
    draw = ImageDraw.Draw(result_img)

    # split image "blocks"
    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            # get a block
            block = img[y : y + block_size, x : x + block_size]

            # get block color alpha channel
            alpha_channel = block[:, :, 3]

            # calculate the average of alpha value: avg_alpha
            avg_alpha = np.mean(alpha_channel)

            if avg_alpha < 50:
                continue  # nearly transparent

            # calculate the avg_color of this block(only RGB channels)
            avg_color = np.mean(block[:, :, :3], axis=(0, 1)).astype(int)
            color = tuple(avg_color) + (255,)  # set alpha to 255

            # draw the block
            draw.rectangle([x, y, x + block_size, y + block_size], fill=color)

    return result_img


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a mosaic image from an input image.")

    parser.add_argument("--input", "-i", type=str, help="Path to the input image.")
    parser.add_argument("--output", "-o", type=str, help="Path to save the output mosaic image. (default value: None, and it will 'Show')", default=None)
    parser.add_argument("--block_size", "-b", type=int, help="Block size for the mosaic effect. (default value: 5)", default=5)

    args = parser.parse_args()

    # check 'input' argument
    if not args.input:
        import sys

        print("No input file provided!")
        sys.exit(1)

    original_img = get_image_from_path(args.input)
    result_img = get_mosaic_image(original_img, args.block_size)

    if args.output:
        result_img.save(args.output, "PNG")
    else:
        plt.imshow(result_img)
        plt.axis("off")
        plt.show()

# Example:
# 1. python3 mosaic-art.py -i example/ztm-logo.png
# 2. python3 mosaic-art.py -i example/ztm-logo.png -b 20
# 3. python3 mosaic-art.py -i example/ztm-logo.png -b 15 -o mosaic-art.png
