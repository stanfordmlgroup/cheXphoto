import cv2
import numpy as np
import pandas as pd

from pathlib import Path
from PIL import Image

from natural.util import add_background

WINDOW_NAME = 'CheXpeditor Client'
COL_PATH = 'Path'
ESC_CODE = 27


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


def display_img(img_path, screen_width, screen_height, i=None, total=None):
    progress = f'[{i + 1}/{total}] ' if i is not None and total is not None else ''
    print(f'{progress}Showing image {str(img_path)}...')
    # Need to convert back to str for compatibility with Win-SSHFS
    img = Image.open(str(img_path)).convert('RGB')
    img = add_background(img, screen_width, screen_height)
    img = np.array(img)[..., ::-1]
    cv2.imshow(WINDOW_NAME, img)


def run_manual(img_paths, screen_width, screen_height, delay):
    total = len(img_paths)
    for i, img_path in enumerate(img_paths):
        display_img(img_path, screen_width, screen_height, i=i, total=total)
        if cv2.waitKey(delay) == ESC_CODE:
            break


def run(csv_path, data_dir, row_start, row_end, screen_width, screen_height, delay=0, connection=None):
    data_dir = Path(data_dir).expanduser()
    if row_end is not None:
        assert row_end > row_start, f"Starting row {row_start} must be strictly less than ending row {row_end}!"
    assert screen_width > 0 and screen_height > 0, "Screen dimensions must be positive!"
    assert delay >= 0, "Delay cannot be negative!"
    # Load image paths to display
    img_paths = load_data(csv_path, data_dir, row_start, row_end)

    # Spawn the display window
    cv2.namedWindow(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(WINDOW_NAME,
                          cv2.WND_PROP_FULLSCREEN,
                          cv2.WINDOW_FULLSCREEN)

    # If a connection was passed in, run in automatic mode. Else, run in manual mode.
    if connection is not None:
        raise NotImplementedError('Not available!')
    else:
        run_manual(img_paths, screen_width, screen_height, delay)
