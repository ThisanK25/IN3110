# `in3110_instapy`

## Description

This package allows you to run any image you would like into either gray or sepia filters,
and saves or displays the filtered image, and scale the image if possible. You can use
different implementations to get faster results.

The grayscale filter and python implementation are the default settings.

## Installation

This package can be installed using pip:

```
python3 -m pip install in3110_instapy
```

## Usage

To run this package, write down

```
python3 -m in3110_instapy (+ arguments to fill in)
```

in the command line. Arguments are listed below.

### Arguments:

- Required:
    - file: The image you wish to apply a filter on

- Options:
    - -h: A menu with a short summary of each argument
    - -o OUT: A file path you wish to save the filtered image to, rather than display
    - -g: Grayscale filter
    - -se: Sepia filter
    - -sc SCALE: Scaling factor, if you wish to resize the image
    - -i {'python', 'numpy', 'numba'}: The implementation of the filter: python, numpy or numba 