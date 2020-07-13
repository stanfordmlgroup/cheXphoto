import numpy as np
from PIL import Image

def add_background(img, out_width, out_height):
    """Paste image onto a black background with the same size as screen.

    Args:
        img (Image): PIL image to paste on background
        out_width (int): width (in px) of output image
        out_height (int): height (in px) of output image

    Returns:
        background (Image): the output image with a black background

    """
    # Create black background with same size as screen
    background = Image.new('RGB', (out_width, out_height), (0, 0, 0))

    # Fit original image within screen while preserving aspect ratio
    img_width, img_height = img.size
    scale_factor = min(float(out_height) / img_height,
                       float(out_width) / img_width)
    new_height = int(scale_factor * img_height)
    new_width = int(scale_factor * img_width)
    img = img.resize((new_width, new_height), Image.ANTIALIAS)

    # Paste original image on black background
    paste_x = (out_width - new_width) // 2
    paste_y = (out_height - new_height) // 2
    background.paste(img, (paste_x, paste_y))
    return background
