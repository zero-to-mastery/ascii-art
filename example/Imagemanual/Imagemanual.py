from PIL import Image

# Step 1: Open the image file using Pillow's Image.open() method
image = Image.open('your_image.jpg')

# Step 2: Get the dimensions of the image (width x height)
image_width, image_height = image.size

# Step 3: Display some information about the image
print(f"Image Format: {image.format}")
print(f"Image Mode: {image.mode}")
print(f"Image Size (Width x Height): {image_width} x {image_height}")

# Step 4: Show the original image (optional)
image.show()

# Step 5: Convert the image to grayscale
grayscale_image = image.convert('L')

# Step 6: Show the grayscale image (optional)
grayscale_image.show()

# Step 7: Save the grayscale image
grayscale_image.save('grayscale_image.jpg')

# Step 8: Close the image files when done to free up system resources
image.close()
grayscale_image.close()

print("Image processing completed. Grayscale image saved as 'grayscale_image.jpg'.")
