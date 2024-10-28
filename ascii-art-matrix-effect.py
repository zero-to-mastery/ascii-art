import cv2
import numpy as np
from PIL import Image
from typing import List

ASCII_CHARS: List[str] = ['#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']


def scale_image(image: Image.Image, new_width: int = 100) -> Image.Image:
    (original_width, original_height) = image.size
    aspect_ratio: float = original_height / float(original_width)
    new_height: int = int(aspect_ratio * new_width)
    new_image: Image.Image = image.resize((new_width, new_height))
    return new_image


def convert_to_grayscale(image: Image.Image) -> Image.Image:
    return image.convert('L')


def map_pixels_to_ascii_chars(image: Image.Image, range_width: int = 25) -> str:
    pixels_in_image: List[int] = list(image.getdata())
    pixels_to_chars: List[int] = [ASCII_CHARS[int(pixel_value / range_width)] for pixel_value in pixels_in_image]
    return "".join(pixels_to_chars)


def convert_image_to_ascii(image: Image.Image, new_width: int = 100) -> str:
    image = scale_image(image, new_width)
    image = convert_to_grayscale(image)
    pixels_to_chars: str = map_pixels_to_ascii_chars(image)
    len_pixels_to_chars: int = len(pixels_to_chars)
    image_ascii: List[str] = [pixels_to_chars[index:index + new_width] for index in range(0, len_pixels_to_chars, new_width)]
    return "\n".join(image_ascii)


def generate_matrix_effect(image_ascii: str, frame_count: int) -> List[str]:
    lines = image_ascii.split('\n')
    height = len(lines)
    width = max(len(line) for line in lines)  # Ensure all lines have the same width
    frames = []
    flow_count = width

    column_states = [-1] * width  # -1 means no flow
    column_lengths = [0] * width

    # Skip the first second (assuming 30 FPS, skip the first 30 frames)
    skip_frames = 30

    for t in range(frame_count):
        new_frame = []
        for y in range(height):
            new_line = ""
            for x in range(width):
                if x >= len(lines[y]):
                    new_line += ' '  # Pad shorter lines with spaces
                elif column_states[x] == -1:
                    new_line += lines[y][x]
                elif column_states[x] < y:
                    new_line += lines[y][x]
                elif column_states[x] - column_lengths[x] <= y:
                    if column_states[x] == y:
                        new_line += " "
                    else:
                        new_line += chr(np.random.choice(list(range(33, 127))))  # Random ASCII characters excluding space
                else:
                    new_line += lines[y][x]
            new_frame.append(new_line)
        frames.append("\n".join(new_frame))
        column_states = [state + 2 if state != -1 else state for state in column_states]  # Move the flow down faster
        # Reset the flow if it reaches the bottom and generate new flows
        for i in range(width):
            if column_states[i] >= height + column_lengths[i]:
                column_states[i] = -1
        # Randomly select columns to start new flows if the number of active flows is less than flow_count
        if t >= skip_frames:
            active_flows = sum(1 for state in column_states if state != -1)
            if active_flows < flow_count and np.random.rand() < 0.8:  # Gradually generate new flows
                i = np.random.randint(0, width)
                if column_states[i] == -1:
                    column_states[i] = 0
                    column_lengths[i] = np.random.randint(int(0.2 * height), int(1.2 * height))  # Random length between 20-120% of height
    return frames


def create_video_from_frames(frames: List[str], output_path: str):
    height = len(frames[0].split('\n'))
    width = len(frames[0].split('\n')[0])
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    frame_rate = 30
    video = cv2.VideoWriter(output_path, fourcc, frame_rate, (width * 10, height * 10))

    for frame in frames:
        img = np.zeros((height * 10, width * 10, 3), dtype=np.uint8)
        for y, line in enumerate(frame.split('\n')):
            for x, char in enumerate(line):
                if char == ' ':  # Head of the flow
                    color = (200, 255, 200)  # Lighter color for the first character of the flow
                    char = chr(np.random.choice(list(range(33, 127))))  # Random ASCII characters excluding space
                else:
                    color = (0, 255, 0)
                cv2.putText(img, char, (x * 10, y * 10 + 10), cv2.FONT_HERSHEY_PLAIN, 1, color, 1)
        video.write(img)

    video.release()


if __name__ == '__main__':
    import sys
    image_file_path: str = sys.argv[1]
    frame_count: int = int(sys.argv[2]) if len(sys.argv) > 2 else 500
    new_width = 100

    image = Image.open(image_file_path)
    image_ascii = convert_image_to_ascii(image, new_width)
    frames = generate_matrix_effect(image_ascii, frame_count)
    create_video_from_frames(frames, "ascii-art-matrix-effect.mp4")
"""
Feature: 
    Generate a MP4 video with matrix effect from ascii-art of an image file.

Args:
    image_file_path: str - Path to the image file.
    frame_count: int - Number of frames to generate (optional, default: 500).

Usage:
    python3 ascii-art-matrix-effect.py <image_file_path> <frame_count>

Example:
    python3 ascii-art-matrix-effect.py example/ztm-logo.png
    python3 ascii-art-matrix-effect.py example/ztm-logo.png 1000

Output file:
    ascii-art-matrix-effect.mp4
"""
