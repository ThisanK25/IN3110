"""pure Python implementation of image filters"""
from __future__ import annotations

import numpy as np


def python_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """

    gray_image = np.empty_like(image)
    # iterate through the pixels, and apply the grayscale transform
    for i in range(gray_image.shape[0]):
        for j in range(gray_image.shape[1]):
            gray_image[i][j] = 0.21*image[i][j][0] + 0.72*image[i][j][1] + 0.07*image[i][j][2]
    return gray_image


def python_color2sepia(image: np.array) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
    sepia_image = np.empty_like(image)
    # Iterate through the pixels
    # applying the sepia matrix

    sepia_matrix = [
        [ 0.393, 0.769, 0.189],
        [ 0.349, 0.686, 0.168],
        [ 0.272, 0.534, 0.131],
    ]

    # Iterate through the image-array and sepia_matrix rows to set sepia values
    for i in range(sepia_image.shape[0]):
        for j in range(sepia_image.shape[1]):
            for k in range(sepia_image.shape[2]):
                # Implement matrix-vector multiplication manually, set color value to 255 if higher than 255
                sepia_image[i][j][k] = min(sepia_matrix[k][0]*image[i][j][0] + sepia_matrix[k][1]*image[i][j][1] + \
                                       sepia_matrix[k][2]*image[i][j][2], 255)

    # Return image
    # don't forget to make sure it's the right type!
    return sepia_image.astype("uint8")
