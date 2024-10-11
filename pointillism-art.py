import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from skimage import color, filters


# Load and resize image
def load_image(image_path, size=(400, 400)):
    img = Image.open(image_path).resize(size)  # Resize for faster processing
    img = img.convert("RGB")  # Ensure it's RGB format
    return np.array(img)


# Generate random points across the image
def generate_random_points(image, num_points):
    height, width, _ = image.shape
    points = np.random.rand(num_points, 2)
    points[:, 0] *= width  # Scale x-coordinates
    points[:, 1] *= height  # Scale y-coordinates
    return points


# Sample color from the image at each point with random perturbation and subtle sepia tone
def sample_colors(image, points):
    height, width, _ = image.shape
    colors = []
    for point in points:
        x, y = int(point[0]), int(point[1])
        x = min(x, width - 1)  # Ensure index within bounds
        y = min(y, height - 1)
        color = image[y, x]  # Note that the y-axis comes first in image indexing

        # Add random perturbation to the color
        perturbation = np.random.randint(-20, 21, size=3)  # Random values between -20 and 20
        perturbed_color = np.clip(color + perturbation, 0, 255)  # Ensure values are within [0, 255]

        # Apply subtle sepia tone effect
        tr = int(0.393 * perturbed_color[0] + 0.769 * perturbed_color[1] + 0.189 * perturbed_color[2])
        tg = int(0.349 * perturbed_color[0] + 0.686 * perturbed_color[1] + 0.168 * perturbed_color[2])
        tb = int(0.272 * perturbed_color[0] + 0.534 * perturbed_color[1] + 0.131 * perturbed_color[2])

        sepia_color = np.clip([tr, tg, tb], 0, 255)

        # Blend the original perturbed color with the sepia color
        blend_ratio = 0.5  # Adjust this value to control the intensity of the sepia effect
        blended_color = np.clip((1 - blend_ratio) * perturbed_color + blend_ratio * sepia_color, 0, 255)

        colors.append(blended_color)
    return np.array(colors)


# Detect edges in the image using Sobel filter
def detect_edges(image):
    grayscale_image = color.rgb2gray(image)
    edges = filters.sobel(grayscale_image)
    return edges


# Compute point sizes based on edge proximity
def compute_point_sizes(points, edges, min_size=1, max_size=50):
    height, width = edges.shape
    point_sizes = []
    edge_values = []  # List to collect edge values

    for point in points:
        x, y = int(point[0]), int(point[1])
        x = min(x, width - 1)  # Ensure index within bounds
        y = min(y, height - 1)

        # Higher edge value means the point is near an edge (smaller point size)
        edge_value = edges[y, x]
        edge_values.append(edge_value)  # Collect edge value

    # Normalize edge values
    min_edge_value = min(edge_values)
    max_edge_value = max(edge_values)
    if max_edge_value != min_edge_value:
        normalized_edge_values = [(ev - min_edge_value) / (max_edge_value - min_edge_value) for ev in edge_values]
    else:
        normalized_edge_values = [0 for _ in edge_values]  # All values are the same

    for i, _ in enumerate(points):
        normalized_edge_value = normalized_edge_values[i]

        # Linearly interpolate between min and max size based on normalized edge value
        point_size = min_size + (1 - normalized_edge_value) * (max_size - min_size)
        point_sizes.append(point_size)

    return np.array(point_sizes)


# Plot the pointillism image with edge-aware point sizes
def create_pointillism_art(image_path, output_path=None, num_points=50000, min_size=1, max_size=50):
    # Load image
    img = load_image(image_path)

    # Generate random points
    points = generate_random_points(img, num_points)

    # Sample colors from the image based on points
    colors = sample_colors(img, points)

    # Detect edges in the image
    edges = detect_edges(img)

    # Compute point sizes based on proximity to edges
    point_sizes = compute_point_sizes(points, edges, min_size, max_size)

    # Plot the points with sampled colors and dynamic sizes
    plt.figure(figsize=(8, 8))
    plt.scatter(points[:, 0], points[:, 1], c=colors / 255, s=point_sizes, edgecolor="none")
    plt.gca().invert_yaxis()  # Match the image's coordinate system
    plt.axis("off")  # Hide axis

    if output_path:
        # Save the plot as an image file
        plt.savefig(output_path, bbox_inches="tight", pad_inches=0, facecolor=(0.5, 0.5, 0.5, 0.0))
        plt.close()
    else:
        # Show the plot
        plt.show()


if __name__ == "__main__":
    import sys

    image_file_path: str = sys.argv[1]
    print(image_file_path)

    if len(sys.argv) == 2:
        create_pointillism_art(image_file_path)
    elif len(sys.argv) == 3:
        output_file_path = sys.argv[2]
        create_pointillism_art(image_file_path, output_file_path)
        print("Pointillism image file path: ", output_file_path)

# Example usage:
# python3 pointillism-art.py example/ztm-logo.png
# python3 pointillism-art.py example/ztm-logo.png pointillism-art.png
