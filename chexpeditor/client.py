"""Implement the CheXpeditor client, which can operate in manual and auto modes.

This file is not meant to be called directly. For that, use the top-level scripts
collection_natural_manual.py and collect_natural_auto.py. Rather, this file provides
the underlying common functionality between the two modes.

"""
from argparse import ArgumentParser
from pathlib import Path

import cv2

from chexpeditor.util import load_data, display_img, path_to_filename, send_message

# General constants
WINDOW_NAME = "CheXpeditor Client"
ESC_CODE = 27

# Constants specific to auto mode
MSG_DELAY_MS = 100
CLIENT_TIMEOUT_S = 10
SERVER_OK = "OK"


def get_base_parser():
    """Get a parser for args common to manual and auto modes."""
    parser = ArgumentParser()

    parser.add_argument("--csv_path", type=str, required=True, help="Path to data CSV")

    parser.add_argument(
        "--data_dir",
        type=str,
        required=True,
        help="The directory in which CheXphoto is located",
    )

    parser.add_argument(
        "--row_start",
        type=int,
        default=0,
        help="Row index of the first image to load (inclusive). 0 is first image",
    )

    parser.add_argument(
        "--row_end",
        type=int,
        help="Row index of the last entry to load (exclusive). Omit to load all entries until end.",
    )

    parser.add_argument(
        "--screen_height", type=int, required=True, help="Height (in px) of the screen",
    )

    parser.add_argument(
        "--screen_width", type=int, required=True, help="Width (in px) of the screen"
    )

    return parser


def run_manual(img_paths, screen_width, screen_height, delay):
    """Run the CheXpeditor client in manual mode.

    Execution can be aborted at any time by pressing the escape key.

    Args:
        img_paths ([Path]): list of resolved image paths
        screen_width (int): width (in px) of the screen
        screen_height (int): height (in px) of the screen
        delay (int): how long in milliseconds the client should wait before advancing
            to the next image. If set to 0, the client will wait for a keypress before
            proceeding.

    """
    assert delay >= 0, "Delay cannot be negative!"
    for i, img_path in enumerate(img_paths):
        display_img(WINDOW_NAME, img_path, screen_width, screen_height, i=i)
        if cv2.waitKey(delay) == ESC_CODE:
            break


def run_auto(img_paths, orig_paths, screen_width, screen_height, seq, connection):
    """Run the CheXpeditor client in auto mode.

    Execution can be aborted at any time by pressing the escape key.

    Args:
        img_paths ([Path]): list of resolved image paths
        orig_paths ([Path]): list of the raw image paths in the CSV. Used for
            creating the raw image filename that will be later reassociated
            to labels in the original CSV.
        screen_width (int): width (in px) of the screen
        screen_height (int): height (in px) of the screen
        seq (int): sequence number for synchronization with server
        connection ((str, int)): see documentation in <run>

    """
    ip, port = connection
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
            if response.startswith(SERVER_OK + "|"):
                _, out_filename = response.split("|")
                print(f"[{seq + i}]: Wrote photo {out_filename}")
                error = False
                break
            elif response == "TIMEOUT":
                print("TIMEOUT. Trying again.")
                error = False
            else:
                if error:
                    print(f"Stopping transfer loop due to server error: {response}")
                    return
                else:
                    error = True
                    print("Mismatch, but will try with next photo.")
                    break


def run(
    csv_path,
    data_dir,
    row_start,
    row_end,
    screen_width,
    screen_height,
    delay=None,
    connection=None,
):
    """Run the CheXpeditor client - not intended to be invoked directly.

    Args:
        csv_path (Path): path to the CSV file, in CheXphoto format
        data_dir (Path): the location of the dataset. Concatenating this
            directory name with a path in the CSV should produce a valid
            relative path!
        row_start (int): row index of the first entry to load (inclusive)
        row_end (int): row index of the last entry to load (exclusive). If None,
            all entries until the end will be loaded.
        screen_width (int): width (in px) of the screen
        screen_height (int): height (in px) of the screen
        delay (int): [MANUAL ONLY] how long in milliseconds the client should wait
            before advancing to the next image. If set to 0, the client will wait for
            a keypress before proceeding.
        connection ((str, int)): [AUTO ONLY] tuple of ip, port.
            ip (str): the IP address of the server (must be on same network)
            port (int): port at which server is listening

    """
    data_dir = Path(data_dir).expanduser()
    if row_end is not None:
        assert (
            row_end > row_start
        ), f"Starting row {row_start} must be strictly less than ending row {row_end}!"
    assert screen_width > 0 and screen_height > 0, "Screen dimensions must be positive!"

    # Load and filter image paths to display
    img_paths, orig_paths = load_data(Path(csv_path), data_dir, row_start, row_end)

    # Spawn the display window
    cv2.namedWindow(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Run the CheXpeditor client in the chosen mode
    if connection is not None:
        run_auto(
            img_paths, orig_paths, screen_width, screen_height, row_start, connection
        )
    else:
        run_manual(img_paths, screen_width, screen_height, delay)
