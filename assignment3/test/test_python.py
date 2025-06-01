from in3110_instapy.python_filters import python_color2gray, python_color2sepia

import numpy as np  # For type checks

def test_color2gray(image):
    # run color2gray
    gray_image = python_color2gray(image)
    # check that the result has the right shape, type
    if not isinstance(gray_image, np.ndarray):
        raise TypeError(f"Expected type {np.ndarray}, but got {type(gray_image)}")
    
    if len(gray_image.shape) != 3:
        raise ValueError(f"Expected a 3-dimensional array, but got a {len(gray_image.shape)}-dimensional array")
    
    if not np.issubdtype(gray_image.dtype, np.uint8):   # Check types of values in array
        raise TypeError(f"Expected type {np.uint8}, but got {type(gray_image.dtype)}")
                
    if gray_image.shape[2] != 3: # There are only 3 RGB values per pixel
        raise ValueError("Array doesn't have shape (image.height, image.width, 3)")
    
    # assert uniform r,g,b values
    for i in range(gray_image.shape[0]):
        for j in range(gray_image.shape[1]):
            assert gray_image[i][j][0] == gray_image[i][j][1] == gray_image[i][j][2], "RGB values of at least one pixel are non-uniform" 


def test_color2sepia(image):
    # run color2sepia
    sepia_image = python_color2sepia(image)
    # check that the result has the right shape, type
    if not isinstance(sepia_image, np.ndarray):
        raise TypeError(f"Expected type {np.ndarray}, but got {type(sepia_image)}")
    
    if len(sepia_image.shape) != 3:
        raise ValueError(f"Expected a 3-dimensional array, but got a {len(sepia_image.shape)}-dimensional array")
    
    if not np.issubdtype(sepia_image.dtype, np.uint8):   # Check types of values in array
        raise TypeError(f"Expected type {np.uint8}, but got {type(sepia_image.dtype)}")
                
    if sepia_image.shape[2] != 3: # There are only 3 RGB values per pixel
        raise ValueError("Array doesn't have shape (image.height, image.width, 3)")
    
    # verify some individual pixel samples
    # according to the sepia matrix

    sepia_matrix = [
        [ 0.393, 0.769, 0.189],
        [ 0.349, 0.686, 0.168],
        [ 0.272, 0.534, 0.131],
    ]

    # Check that the first and last pixels per dimension are correct within a margin of error
    for i in (0, -1):
        for j in (0, -1):
            for k in range(3):
                assert np.isclose(sepia_image[i][j][k], min(int(sepia_matrix[k][0]*image[i][j][0] + \
                                                        sepia_matrix[k][1]*image[i][j][1] + \
                                                        sepia_matrix[k][2]*image[i][j][2]), 255), atol=1), \
                                                        "Margin of error between values is too great"
    