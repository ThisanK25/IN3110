"""Command-line (script) interface to instapy"""
from __future__ import annotations

import argparse
import sys

import in3110_instapy
import numpy as np
from PIL import Image

from . import io


def run_filter(
    file: str,
    out_file: str = None,
    implementation: str = "python",
    filter: str = "color2gray",
    scale: int = 1,
) -> None:
    """Run the selected filter"""
    # load the image from a file
    image = Image.open(file)
    if scale != 1:
        # Resize image, if needed
        image = image.resize((int(scale*image.size[0]), int(scale*image.size[1])))

    # Apply the filter
    image_arr = np.asarray(image)   # Convert image to array first
    filter_function = in3110_instapy.get_filter(implementation=implementation, filter=filter)
    filtered = filter_function(image_arr)
    if out_file:
        # save the file
        io.write_image(filtered, out_file)
    else:
        # not asked to save, display it instead
        io.display(filtered)


def main(argv=None):
    """Parse the command-line and call run_filter with the arguments"""
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser()

    # filename is positional and required
    parser.add_argument("file", type=str, help="The filename to apply filter to")

    # Add required arguments
    parser.add_argument("-o", "--out", type=str, help="The output filename")
    parser.add_argument("-g", "--gray", help="Select gray filter", action="store_true")
    parser.add_argument("-se", "--sepia", help="Select sepia filter", action="store_true")
    parser.add_argument("-sc", "--scale", type=float, help="Scale factor to resize image")
    parser.add_argument("-i", "--implementation", metavar={"python", "numpy", "numba"}, type=str, help="The implementation")

    # parse arguments and call run_filter
    args = parser.parse_args()

    # Default settings
    implementation = "python"
    filter = "color2gray"
    scale = 1

    # Set values based on command line inputs
    if args.sepia:
        filter = "color2sepia"
    if args.gray and args.sepia:    # If both gray and sepia are called, terminate
        print("You cannot run two filters at once.")
        sys.exit()
    if args.implementation == "numpy":
        implementation = "numpy"
    elif args.implementation == "numba":
        implementation = "numba"
    elif args.implementation != "python" and args.implementation != None:   # Terminates when an invalid input is set
        print("Implementation has to be of the following: {'python', 'numpy', 'numba'}")
        sys.exit()
    if args.scale != None:
        scale = args.scale
    
    run_filter(args.file, args.out, implementation=implementation, filter=filter, scale=scale)