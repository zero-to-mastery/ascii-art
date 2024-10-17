import io, numpy as np
from typing import List
from PIL import Image, ImageDraw

def __get_image_from_bytes(byte_contents: bytes) -> Image:
    """_summary_
    Args:
        byte_contents (bytes): Input image bytes.
    Returns:
        Image: Output image.
    """
    return Image.open(io.BytesIO(byte_contents)).convert('RGBA')

def get_mosaic_image(contents: bytes, block_size:int=10) -> Image:
    """_summary_
    Args:
        contents (bytes): Input image bytes.
        block_size (int, optional): Sidelength of a mosaic block. Defaults to 10.
    Returns:
        Image: Output image.
    """ 
    image = __get_image_from_bytes(contents)

    img = np.array(image)
    
    #get height and width of image
    height, width, _ = img.shape

    #create an empty image
    result = Image.new('RGBA', (width, height), (0, 0, 0, 0)) 
    draw = ImageDraw.Draw(result)

    #split image "blocks"
    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            #get a block
            block = img[y:y+block_size, x:x+block_size]

            #get block color alpha channel
            alpha_channel = block[:, :, 3]

            #calculate the average of alpha value: avg_alpha
            avg_alpha = np.mean(alpha_channel)

            if avg_alpha < 50:
                continue  #nearly transparent

            #calculate the avg_color of this block(only RGB channels)
            avg_color = np.mean(block[:, :, :3], axis=(0, 1)).astype(int)
            color = tuple(avg_color) + (255,)  #set alpha to 255

            #draw the block
            draw.rectangle([x, y, x+block_size, y+block_size], fill=color)
            
    return result

