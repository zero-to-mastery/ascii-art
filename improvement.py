def save_ascii_art_to_jpg(image_ascii, image):
    if not image:
        raise Exception('Image object is invalid')
    if len(image_ascii) <= 0:
        raise Exception('ASCII art string is of invalid length')
    
    # Dimensions of the original image
    original_image_width, original_image_height = image.size
    characters_count_in_width = len(image_ascii.split()[0])
    characters_count_in_height = len(image_ascii.split())

    # Dimensions of the output image
    output_image_width = 6*characters_count_in_width
    output_image_height = 15*characters_count_in_height

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    try:
        # Create a blank image of black background
        image = Image.new("RGB", (output_image_width, output_image_height), BLACK)
        draw = ImageDraw.Draw(image)

        # Draw the text on the blank image from top left corner with font color of white
        draw.text((0, 0), image_ascii, fill=WHITE)

        # Resize the output image as per the original image's dimensions
        resized_image = image.resize((original_image_width, original_image_height))
        resized_image.save('output.jpg')
        print('ASCII art image saved to output.jpg')
    except Exception as exception:
        raise exception