from PIL import Image, ImageOps
import sys
import os

image_folder = sys.argv[1]

ASCII_CHARS = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", "."]


for images in os.listdir(image_folder):
    images = Image.open(f'{image_folder}{images}')

    images.thumbnail((100, 100))
    imgs = ImageOps.grayscale(images)

    def pixel_to_ascii(image):
        pixels = Image.Image.getdata(image)
        ascii_string = ""
        for pixel in pixels:
            ascii_string += ASCII_CHARS[pixel//25]
        return ascii_string

    # converting greyscale images to ascii strings
    ascii_str = pixel_to_ascii(imgs)

    width = imgs.width
    ascii_str_len = len(ascii_str)

    ascii_image_art = ""

    for indexes in range(0, ascii_str_len, width):
        ascii_image_art += ascii_str[indexes: indexes+width] + "\n"

    print(ascii_image_art)

    # below 👇 is an optional code if you want to store the last ascii_art into a text file

    # with open("ascii_art.txt", "w") as file:
    #    file.write(ascii_image_art)
