import sys

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy.spatial import Delaunay


# Load and preprocess the image
def load_image(image_path, resize_factor=1):
    img = Image.open(image_path)
    img = img.resize((int(img.width * resize_factor), int(img.height * resize_factor)))
    return np.array(img)


# Generate random points over the image
def generate_points(image, num_points=500):
    height, width, _ = image.shape
    # Random points across the image dimensions
    points = np.vstack((np.random.randint(0, width, num_points), np.random.randint(0, height, num_points))).T
    # Add corners to ensure triangulation covers the entire image
    points = np.vstack([points, [[0, 0], [0, height], [width, 0], [width, height]]])
    return points


# Create Delaunay triangulation from points
def create_delaunay_triangulation(points):
    return Delaunay(points)


# Draw triangles on the image using the Delaunay triangulation
def draw_geometric_art(image, points, triangulation, output_path=None):
    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.imshow(image)

    for triangle in triangulation.simplices:
        vertices = points[triangle]
        # Get the color of the center of the triangle
        center = np.mean(vertices, axis=0).astype(int)
        color = image[center[1], center[0], :] / 255

        # Draw the triangle with the calculated color
        triangle_shape = plt.Polygon(vertices, color=color)
        ax.add_patch(triangle_shape)

    ax.set_axis_off()
    if output_path:
        plt.savefig(output_path, bbox_inches="tight", pad_inches=0, facecolor=(0.5, 0.5, 0.5, 0.0))
    else:
        plt.show()


# Main function to convert image to geometric art
def create_geometric_art(image_path, output_path=None, num_points=500, resize_factor=1):
    # Load image and generate points
    image = load_image(image_path, resize_factor)
    points = generate_points(image, num_points)

    # Create triangulation and draw art
    triangulation = create_delaunay_triangulation(points)
    draw_geometric_art(image, points, triangulation, output_path)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 geometric-art.py <input_image> [output_image] [num_points]")
        sys.exit(1)

    image_file_path = sys.argv[1]
    output_file_path = sys.argv[2] if len(sys.argv) > 2 else None
    num_points = int(sys.argv[3]) if len(sys.argv) > 3 else 500

    create_geometric_art(image_file_path, output_file_path, num_points)

# Example usage:
# python3 geometric-art.py example/ztm-logo.png
# python3 geometric-art.py example/ztm-logo.png geometric-art.png
# python3 geometric-art.py example/ztm-logo.png geometric-art.png 1000
