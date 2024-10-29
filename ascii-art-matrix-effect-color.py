from typing import List, Tuple

import cv2
import numpy as np
from PIL import Image

ASCII_CHARS: List[str] = [".", ":", ">", "&", "%", "#", "N", "M", "W", "R", "B"]


def scale_image(image: Image.Image, new_width: int = 100) -> Image.Image:
    (original_width, original_height) = image.size
    aspect_ratio: float = original_height / float(original_width)
    new_height: int = int(aspect_ratio * new_width)
    new_image: Image.Image = image.resize((new_width, new_height))
    return new_image


def convert_to_grayscale(image: Image.Image) -> Image.Image:
    return image.convert("L")


def map_pixels_to_ascii_chars(image: Image.Image, range_width: int = 25) -> str:
    pixels_in_image: List[int] = list(image.getdata())
    pixels_to_chars: List[int] = [ASCII_CHARS[int(pixel_value / range_width)] for pixel_value in pixels_in_image]
    return "".join(pixels_to_chars)


def convert_image_to_ascii(image: Image.Image, new_width: int = 100) -> Tuple[str, List[Tuple[int, int, int, int]]]:
    image = scale_image(image, new_width)
    grayscale_image = convert_to_grayscale(image)
    pixels_to_chars: str = map_pixels_to_ascii_chars(grayscale_image)
    len_pixels_to_chars: int = len(pixels_to_chars)
    image_ascii: List[str] = [pixels_to_chars[index : index + new_width] for index in range(0, len_pixels_to_chars, new_width)]
    color_data: List[Tuple[int, int, int, int]] = list(image.convert("RGBA").getdata())
    return "\n".join(image_ascii), color_data


def get_char_for_position(x, y, lines, column_states, column_lengths):
    if x >= len(lines[y]):
        return " "  # Pad shorter lines with spaces
    if column_states[x] == -1 or column_states[x] < y:
        return lines[y][x]
    if column_states[x] - column_lengths[x] <= y:
        if column_states[x] == y:
            return " "
        else:
            return chr(np.random.choice(list(range(33, 127))))  # Random ASCII characters excluding space
    return lines[y][x]


def generate_new_frame(lines, column_states, column_lengths, height, width):
    new_frame = []
    for y in range(height):
        new_line = "".join(get_char_for_position(x, y, lines, column_states, column_lengths) for x in range(width))
        new_frame.append(new_line)
    return new_frame


def update_column_states(column_states, column_lengths, columns_covered, height, width):
    # Move the flow down faster
    column_states = [state + 2 if state != -1 else state for state in column_states]
    # Reset the flow if it reaches the bottom and mark columns as covered
    for i in range(width):
        if column_states[i] >= height + column_lengths[i]:
            column_states[i] = -1
            columns_covered[i] = True  # Mark this column as covered
    return column_states, columns_covered


def start_new_flows(column_states, column_lengths, columns_covered, height, width, t, skip_frames):
    if t >= skip_frames:
        active_flows = sum(1 for state in column_states if state != -1)
        if active_flows < width:
            # Ensure all columns are eventually covered
            uncovered_columns = [i for i, covered in enumerate(columns_covered) if not covered]
            if uncovered_columns:
                i = np.random.choice(uncovered_columns)
            else:
                i = np.random.randint(0, width)
            if column_states[i] == -1:
                column_states[i] = 0
                column_lengths[i] = np.random.randint(int(0.2 * height), int(1.2 * height))  # Random length between 20-120% of height
    return column_states, column_lengths


def generate_matrix_effect(image_ascii: str) -> List[str]:
    lines = image_ascii.split("\n")
    height = len(lines)
    width = max(len(line) for line in lines)  # Ensure all lines have the same width
    frames = []

    column_states = [-1] * width  # -1 means no flow
    column_lengths = [0] * width
    columns_covered = [False] * width  # Track which columns have been covered by the flow

    # Skip the first second (assuming 30 FPS, skip the first 30 frames)
    skip_frames = 30
    t = 0

    while not all(columns_covered):
        new_frame = generate_new_frame(lines, column_states, column_lengths, height, width)
        frames.append("\n".join(new_frame))
        column_states, columns_covered = update_column_states(column_states, column_lengths, columns_covered, height, width)
        column_states, column_lengths = start_new_flows(column_states, column_lengths, columns_covered, height, width, t, skip_frames)
        t += 1

    # Add 1 second of additional frames after all columns are covered
    additional_frames = 30
    frames.extend([frames[-1]] * additional_frames)

    return frames


def create_video_from_frames(frames: List[str], color_data: List[Tuple[int, int, int, int]], width: int, output_path: str):
    height = len(frames[0].split("\n"))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    frame_rate = 30
    video = cv2.VideoWriter(output_path, fourcc, frame_rate, (width * 10, height * 10))

    # Track which characters have been part of the flow
    flow_passed = [[False] * width for _ in range(height)]

    for frame in frames:
        img = np.zeros((height * 10, width * 10, 3), dtype=np.uint8)
        for y, line in enumerate(frame.split("\n")):
            for x, char in enumerate(line):
                color = color_data[y * width + x] if y * width + x < len(color_data) else (0, 255, 0, 255)
                if color[3] == 0:  # Handle transparency
                    color = (50, 50, 50, 255)  # Convert transparent pixels to dark gray

                if char in ASCII_CHARS:
                    color = (color[2], color[1], color[0])  # Convert RGBA to BGR
                elif char == " ":  # Head of the flow
                    char = chr(np.random.choice(list(range(33, 127))))  # Random ASCII characters excluding space
                    color = (200, 255, 200)  # Lighter color for the first character of the flow
                else:
                    color = (0, 255, 0)  # Green color for the flow
                    flow_passed[y][x] = True  # Mark this character as part of the flow

                # If the flow has passed, turn the character green
                if flow_passed[y][x]:
                    color = (0, 255, 0)

                cv2.putText(img, char, (x * 10, y * 10 + 10), cv2.FONT_HERSHEY_PLAIN, 1, color, 1)
        video.write(img)

    video.release()


if __name__ == "__main__":
    import sys

    image_file_path: str = sys.argv[1]
    new_width = 100

    image = Image.open(image_file_path)
    image_ascii, color_data = convert_image_to_ascii(image, new_width)
    frames = generate_matrix_effect(image_ascii)
    create_video_from_frames(frames, color_data, new_width, "ascii-art-matrix-effect-color.mp4")
"""
Feature:
    Generate a MP4 video with matrix effect from ascii-art of an image file.
    Gradually turning the coloured characters green as the "flow" passes through them.

Usage:
    python3 ascii-art-matrix-effect-color.py <image_file_path>

Args:
    image_file_path: str - Path to the image file.

Example:
    python3 ascii-art-matrix-effect-color.py example/ztm-logo.png

Output file:
    ascii-art-matrix-effect-color.mp4
"""
