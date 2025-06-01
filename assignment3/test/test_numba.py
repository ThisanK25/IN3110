import numpy.testing as nt
import numpy as np  # For type checking
from in3110_instapy.numba_filters import numba_color2gray, numba_color2sepia


def test_color2gray(image, reference_gray):
    # run color2gray
    gray_image = numba_color2gray(image)
    # check that the result has the right shape, type
    if not isinstance(gray_image, np.ndarray):
        raise TypeError(f"Expected type {np.ndarray}, but got {type(gray_image)}")
    
    if len(gray_image.shape) != 3:
        raise ValueError(f"Expected a 3-dimensional array, but got a {len(gray_image.shape)}-dimensional array")
    
    if not np.issubdtype(gray_image.dtype, np.uint8):   # Check types of values in array
        raise TypeError(f"Expected type {np.uint8}, but got {type(gray_image.dtype)}")
                
    if gray_image.shape[2] != 3: # There are only 3 RGB values per pixel
        raise ValueError("Array doesn't have shape (image.height, image.width, 3)")
    
    # Check that all values in the array are close in value to the reference array
    nt.assert_allclose(gray_image, reference_gray, err_msg="Margin of error is too great for some values")


def test_color2sepia(image, reference_sepia):
    # run color2sepia
    sepia_image = numba_color2sepia(image)
    # check that the result has the right shape, type
    if not isinstance(sepia_image, np.ndarray):
        raise TypeError(f"Expected type {np.ndarray}, but got {type(sepia_image)}")
    
    if len(sepia_image.shape) != 3:
        raise ValueError(f"Expected a 3-dimensional array, but got a {len(sepia_image.shape)}-dimensional array")
    
    if not np.issubdtype(sepia_image.dtype, np.uint8):   # Check types of values in array
        raise TypeError(f"Expected type {np.uint8}, but got {type(sepia_image.dtype)}")
                
    if sepia_image.shape[2] != 3: # There are only 3 RGB values per pixel
        raise ValueError("Array doesn't have shape (image.height, image.width, 3)")
    
    # Check that all values in the array are close in value to the reference array
    nt.assert_allclose(sepia_image, reference_sepia, err_msg="Margin of error is too great for some values")
