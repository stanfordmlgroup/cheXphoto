import cv2

from pathlib import Path

from natural.util import load_data, display_img

WINDOW_NAME = 'CheXpeditor Client'
ESC_CODE = 27


def run_manual(img_paths, screen_width, screen_height, delay):
    total = len(img_paths)
    for i, img_path in enumerate(img_paths):
        display_img(WINDOW_NAME, img_path, screen_width, screen_height, i=i, total=total)
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
