# -*- coding: utf-8 -*-


"""monoshape main

This program takes an image that has well differentiated light and dark
tones and extracts its monochromatic shape in the desired color with a 
transparent background.

This is the main Python file.
"""

import sys
from typing import Tuple, List

import filetype
from PIL import Image, ImageOps, PngImagePlugin

__author__ = 'Borja González Seoane'
__copyright__ = 'Copyright 2019, Borja González Seoane'
__credits__ = 'Borja González Seoane'
__license__ = 'LICENSE'
__version__ = '0.1dev0'
__maintainer__ = 'Borja González Seoane'
__email__ = 'dev@glezseoane.com'
__status__ = 'Development'


# =============================================
# =               Order handling              =
# =============================================
# noinspection PyShadowingNames
def handle_arguments(argv: List) -> Tuple:
    """Handles the arguments.

    Handles the arguments when the program is run and exports it into a
    enumeration of it.

    :param argv: Vector with the ordered input arguments
    :type argv: List
    :return: Interpreted argument vector
    :rtype: Tuple
    """
    # Assert composition integrity
    if not (len(argv) >= 2 or len(argv) <= 7):
        raise IOError("Bad command composition! Please, read the manual.")

    # The path is always the first argument
    path = argv[1]

    if '-bb' in argv or '--black_background' in argv:
        black_background = True
    else:
        black_background = False

    if '-ws' in argv or '--white_shape' in argv:
        white_shape = True
    else:
        white_shape = False

    if '-rgb' in argv:
        rgb_shape = True
        index = argv.index('-rgb')
        red = int(argv[index + 1])
        green = int(argv[index + 2])
        blue = int(argv[index + 3])
    else:
        rgb_shape = False
        red = green = blue = None

    return path, black_background, white_shape, rgb_shape, red, \
        green, blue


# =============================================
# =                  Process                  =
# =============================================
# noinspection PyShadowingNames
def extract_shape(path: str,
                  black_background: bool = False,
                  white_shape: bool = False,
                  rgb_shape: bool = False,
                  red: int = None,
                  green: int = None,
                  blue: int = None) -> PngImagePlugin.PngImageFile:
    """Extracts a shape from an image.

    Processes an input image (as path) to extract its associated shape.
    Per omission, the shape is drawn black, but using the white_shape
    flag can be drawn white and using the rgb_shape and its associated
    values can be drawn on every desired color.

    :param path: Path to the original image
    :type path: str
    :param black_background: Flag to consider an inverse image with a black
        background in the image processing
    :type black_background: bool
    :param white_shape: Flag to use a white shape
    :type white_shape: bool
    :param rgb_shape: Flag to use a custom RGB color to the
        output shape
    :type rgb_shape: bool
    :param red: Using an RGB input, the red value
    :type red: int
    :param green: Using an RGB input, the green value
    :type green: int
    :param blue: Using an RGB input, the blue value
    :type blue: int
    :return: The shape as a PIL image object
    :rtype: PngImagePlugin.PngImageFile
    """
    thresh = 200  # Image white threshold

    # Check arguments integrity
    if path is None:
        raise ValueError("Bad argument composition! The path is mandatory.")
    if not (black_background ^ white_shape ^ rgb_shape)\
            and (black_background or white_shape or rgb_shape):
        raise ValueError("Bad argument composition! Only a flag can be set "
                         "to True.")
    if rgb_shape and not (red is not None
                          and green is not None
                          and blue is not None):
        raise ValueError("Bad argument composition! Using RGB mode is "
                         "mandatory specify the color values.")

    # Check file PNG typing
    try:
        if not filetype.guess(path).mime == 'image/png':
            raise IOError("The input file must be a PNG image!")
    except FileNotFoundError:
        raise FileNotFoundError

    img = Image.open(path)

    # Invert the image color if the flag is passed
    if black_background:
        img = img.convert('RGB')
        img = ImageOps.invert(img)

    img = img.convert('RGBA')
    img_decomposition = img.getdata()
    format_data = []
    for pixel in img_decomposition:
        if pixel[0] >= thresh and pixel[1] >= thresh and pixel[2] >= thresh \
                or pixel[3] == 0:  # If the pixel is white or yet transparent
            format_data.append((0, 0, 0, 0))  # Assert it transparent
        else:
            if white_shape:
                format_data.append((255, 255, 255, 255))  # Make it white
            elif rgb_shape:
                format_data.append((red, green, blue, 255))  # Make it rgb
            else:
                format_data.append((0, 0, 0, 255))  # Make it black
    img.putdata(format_data)

    return img


# =============================================
# =                    MAIN                   =
# =============================================
if __name__ == "__main__":
    path, black_background, white_shape, rgb_shape, red, \
        green, blue = handle_arguments(sys.argv)

    shape = extract_shape(path, black_background, white_shape,
                          rgb_shape, red, green, blue)
    # Save into a different file
    shape.save(path.replace('.png', '_trace.png'))
