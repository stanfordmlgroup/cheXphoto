import cv2

from argparse import ArgumentParser
from pathlib import Path

from natural.util import load_data, display_img, path_to_filename, send_message

WINDOW_NAME = 'CheXpeditor Client'
ESC_CODE = 27

# Constants specific to auto mode
MSG_DELAY_MS = 100
CLIENT_TIMEOUT_S = 10
SERVER_OK = 'OK'


def get_base_parser():
    parser = ArgumentParser()

    parser.add_argument('--csv_path', type=str,
                        required=True,
                        help='Path to data CSV')

    parser.add_argument('--data_dir', type=str,
                        required=True,
                        help='The directory in which CheXphoto is located')

    parser.add_argument('--row_start', type=int, default=0,
                        help='Image # of CSV to display. 0 is first image')

    parser.add_argument('--row_end', type=int,
                        help='Image # of CSV to display (non-inclusive)')

    parser.add_argument('--screen_height', type=int, required=True,
                        help='Height of target screen (in px)')

    parser.add_argument('--screen_width', type=int, required=True,
                        help='Width of target screen (in px)')

    return parser


def run_manual(img_paths, screen_width, screen_height, delay):
    assert delay >= 0, "Delay cannot be negative!"
    for i, img_path in enumerate(img_paths):
        display_img(WINDOW_NAME, img_path, screen_width, screen_height, i=i)
        if cv2.waitKey(delay) == ESC_CODE:
            break


def run_auto(img_paths, orig_paths, screen_width, screen_height, connection):
    ip, port, seq = connection
    assert seq >= 0, "Sequence number should be nonnegative!"
    assert len(img_paths) == len(orig_paths)
    error = False
    for i, (img_path, orig_path) in enumerate(zip(img_paths, orig_paths)):
        display_img(WINDOW_NAME, img_path, screen_width, screen_height, i=seq + i)
        if cv2.waitKey(MSG_DELAY_MS) == ESC_CODE:
            break
        filename = path_to_filename(seq + i, orig_path)
        while True:
            response = send_message(ip, port, seq + i, filename, CLIENT_TIMEOUT_S)
            if response.startswith(SERVER_OK + '|'):
                _, out_filename = response.split('|')
                print(f"[{seq + i}]: Wrote photo {out_filename}")
                error = False
                break
            elif response == 'TIMEOUT':
                print('TIMEOUT. Trying again.')
                error = False
            else:
                if error:
                    print(f"Stopping transfer loop due to server error: {response}")
                    return
                else:
                    error = True
                    print("Mismatch, but will try with next photo.")
                    break


def run(csv_path, data_dir, row_start, row_end, screen_width, screen_height, delay=None, connection=None):
    data_dir = Path(data_dir).expanduser()
    if row_end is not None:
        assert row_end > row_start, f"Starting row {row_start} must be strictly less than ending row {row_end}!"
    assert screen_width > 0 and screen_height > 0, "Screen dimensions must be positive!"
    # Load image paths to display
    img_paths, orig_paths = load_data(csv_path, data_dir, row_start, row_end)

    # Spawn the display window
    cv2.namedWindow(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(WINDOW_NAME,
                          cv2.WND_PROP_FULLSCREEN,
                          cv2.WINDOW_FULLSCREEN)

    # If a connection was passed in, run in auto mode. Else, run in manual mode.
    if connection is not None:
        run_auto(img_paths, orig_paths, screen_width, screen_height, connection)
    else:
        run_manual(img_paths, screen_width, screen_height, delay)
