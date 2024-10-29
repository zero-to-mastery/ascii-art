import gradio as gr
from PIL import Image
import numpy as np
import torch
from transformers import CLIPProcessor, CLIPModel
import os

# Load the CLIP model and processor
try:
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch16")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch16")
    print("Model loaded successfully!")
except Exception as e:
    print("Error loading the model:", e)

# Function to convert image to ASCII art
def image_to_ascii(image, width=100):
    image = image.resize((width, int((width / image.width) * image.height)))
    image = image.convert("L")  # Convert to grayscale
    
    ascii_chars = "@%#*+=-:. "
    pixels = np.array(image)
    ascii_str = ""
    for row in pixels:
        for pixel in row:
            ascii_str += ascii_chars[pixel // 32]
        ascii_str += "\n"  # New line for each row of pixels
    return ascii_str

# Main function: Classifies the image and generates ASCII art
def classify_image(image):
    try:
        # Preparing the image for the model
        inputs = processor(images=image, return_tensors="pt")

        # List of classes that the model can predict
        classes = [
            "dog", "cat", "car", "flower", "tree", "building", "person", "bicycle",
            "airplane", "train", "boat", "mountain", "beach", "forest", "lake", 
            "city", "sunset", "bird", "fish", "food", "pizza", "burger", "pasta", 
            "cake", "coffee", "phone", "laptop", "book", "pen", "chair", "table", 
            "shoe", "bag", "hat", "watch", "ball", "trophy", "guitar", "piano",
            "sunglasses", "camera", "tree", "cloud", "rainbow", "fire", "waterfall",
            "cup", "bottle", "bridge", "street", "bus", "truck", "motorcycle", 
            "clock", "keyboard", "monitor", "bed", "sofa", "microwave", "refrigerator", 
            "washing machine", "oven", "TV", "skyscraper", "snow", "desert", "cactus",
            "rose", "sunflower", "butterfly", "spider", "frog", "shark", "whale",
            "owl", "squirrel", "rabbit", "fox", "horse", "sheep", "cow", "chicken",
            "pig", "duck", "goat", "monkey", "lion", "tiger", "elephant", "bear"
        ]

        # Preparing the classes for the model
        text_inputs = processor(text=classes, return_tensors="pt", padding=True)

        # Use the model to predict the class
        with torch.no_grad():
            outputs = model(**inputs, input_ids=text_inputs["input_ids"])

        logits_per_image = outputs.logits_per_image  # Logits for the image
        probs = logits_per_image.softmax(dim=1)  # Convert to probabilities

        # Find the class with the highest probability
        predicted_class_idx = probs.argmax().item()
        predicted_class = classes[predicted_class_idx]

    except Exception as e:
        print("Error during classification:", e)
        predicted_class = "Unrecognized"  # If unable to classify, use a default message

    # Generate the ASCII art
    ascii_art = image_to_ascii(image)

    # Save the ASCII art to a file
    output_path = "ascii_art.txt"
    with open(output_path, "w") as file:
        file.write(f"Detected class: {predicted_class}\n\n")
        file.write(ascii_art)

    # Return the result
    return f"Detected class: {predicted_class}\n\nASCII art saved in: {output_path}\n\nASCII art:\n{ascii_art}"

# Create the Gradio interface
iface = gr.Interface(
    fn=classify_image,
    inputs=gr.Image(type="pil"),
    outputs="text",
    title="Image Classification with ASCII Art",
    description="Detects the class of an image, generates an ASCII representation, and saves it in the current directory."
)

iface.launch()
