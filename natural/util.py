import numpy as np
from PIL import Image
from pathlib import Path
import pandas as pd
import cv2

COL_PATH = 'Path'


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


def load_data(csv_path, data_dir, row_start, row_end):
    assert Path(csv_path).exists()
    # Load image paths from CSV and resolve relative to data_dir
    df = pd.read_csv(csv_path)
    img_paths = list(map(lambda path: data_dir / path, df[COL_PATH]))
    # Select images based on given range
    if row_end is None:
        img_paths = img_paths[row_start:]
    else:
        img_paths = img_paths[row_start: row_end]
    # Check that all images in range exist
    for img_path in img_paths:
        assert img_path.exists(), f"Could not locate image {str(img_path)}!"
    return img_paths


def display_img(window_name, img_path, screen_width, screen_height, i=None, total=None):
    progress = f'[{i + 1}/{total}] ' if i is not None and total is not None else ''
    print(f'{progress}Showing image {str(img_path)}...')
    # Need to convert back to str for compatibility with Win-SSHFS
    img = Image.open(str(img_path)).convert('RGB')
    img = add_background(img, screen_width, screen_height)
    img = np.array(img)[..., ::-1]
    cv2.imshow(window_name, img)
