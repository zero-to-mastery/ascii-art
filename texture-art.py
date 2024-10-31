import argparse
import io
import os
import random

import matplotlib.pyplot as plt
from PIL import Image


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


def get_random_texture_path(folder_path: str) -> str:
    """_summary_

    Args:
        folder_path (str): The folder where to find images(only jpg)

    Returns:
        str: Full path of a selected image
    """
    # get all .jpg files in the folder
    jpg_files = [f for f in os.listdir(folder_path) if f.endswith(".jpg")]

    if not jpg_files:
        return None

    # randomly select a .jpg file
    file = random.choice(jpg_files)

    # return full path
    return os.path.join(folder_path, file)


def apply_texture_with_fit_cover(input_image: Image, texture_image: Image, alpha_threshold=128) -> Image:
    """_summary_

    Args:
        input_image (Image): Input image
        texture_image (Image): Texture image
        alpha_threshold (int, optional): The alpha value threshold (0-255).
                               Only areas with an alpha value higher than this threshold
                               will receive the texture. Default is 128.
                               - 0 means fully transparent areas are affected.
                               - 255 means only fully opaque areas are affected
                               - Defaults to 128.

    Returns:
        Image: Output image.
    """
    # get width and height of the input and texture images
    input_width, input_height = input_image.size
    texture_width, texture_height = texture_image.size

    # calculate the scaling factor to ensure the texture covers the input image (object-fit: cover effect)
    scale = max(input_width / texture_width, input_height / texture_height)
    new_texture_size = (int(texture_width * scale), int(texture_height * scale))

    # resize the texture image, maintaining the aspect ratio to cover the input image
    texture_img_resized = texture_image.resize(new_texture_size, Image.Resampling.LANCZOS)

    # calculate the area to crop from the texture to center it
    crop_x = (new_texture_size[0] - input_width) // 2
    crop_y = (new_texture_size[1] - input_height) // 2
    texture_img_cropped = texture_img_resized.crop((crop_x, crop_y, crop_x + input_width, crop_y + input_height))

    # extract the alpha channel from the input image
    input_alpha = input_image.split()[3]

    # create an empty image
    result_img = Image.new("RGBA", (input_width, input_height), (0, 0, 0, 0))

    # iterate over each pixel, applying the texture based on the alpha channel
    for y in range(input_height):
        for x in range(input_width):
            # get current pixel's alpha value
            alpha_value = input_alpha.getpixel((x, y))

            # apply the texture if the alpha value exceeds the threshold
            if alpha_value > alpha_threshold:
                # use the pixel from the texture image
                texture_pixel = texture_img_cropped.getpixel((x, y))
                result_img.putpixel((x, y), texture_pixel)
            else:
                # retain the original transparency or make it fully transparent
                result_img.putpixel((x, y), (0, 0, 0, 0))
    return result_img


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apply a texture image to an input image.")

    parser.add_argument("--input_image", "-i", type=str, help="Path to the input image.")
    parser.add_argument("--texture_image", "-t", type=str, help="Path to the texture image.", default=None)
    parser.add_argument("--output", "-o", type=str, help="Path to save the output image. (default value: None, and it will 'Show')", default=None)
    # parser.add_argument("--alpha_threshold", "-a", type=int, help="The alpha value threshold (0-255)", default=128)

    args = parser.parse_args()

    # check 'input_image' argument
    if not args.input_image:
        import sys

        print("No input file provided!")
        sys.exit(1)

    original_img = get_image_from_path(args.input_image)

    # check 'texture_image' argument
    # if texture_image is None, select a random texture from somewhere
    if args.texture_image is None:
        random_texture_path = get_random_texture_path("texture-art-source")
        texture_img = get_image_from_path(random_texture_path)
    else:
        texture_img = get_image_from_path(args.texture_image)

    result_img = apply_texture_with_fit_cover(original_img, texture_img)

    if args.output:
        result_img.save(args.output, "PNG")
    else:
        plt.imshow(result_img)
        plt.axis("off")
        plt.show()

# Example:
# 1. python3 texture-art.py -i example/ztm-logo.png
# 2. python3 texture-art.py -i example/ztm-logo.png -t your/own/texture/path
# 3. python3 texture-art.py -i example/ztm-logo.png -o texture-art.png
