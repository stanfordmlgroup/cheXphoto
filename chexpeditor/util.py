"""Implement utility functions used in chexpeditor_client.py."""
import random
from pathlib import Path
from socket import AF_INET, SOCK_DGRAM, socket, timeout

import cv2
import numpy as np
import pandas as pd
from PIL import Image

MAX_NONCE = 100
COL_PATH = "Path"


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
    background = Image.new("RGB", (out_width, out_height), (0, 0, 0))

    # Fit original image within screen while preserving aspect ratio
    img_width, img_height = img.size
    scale_factor = min(float(out_height) / img_height, float(out_width) / img_width)
    new_height = int(scale_factor * img_height)
    new_width = int(scale_factor * img_width)
    img = img.resize((new_width, new_height), Image.ANTIALIAS)

    # Paste original image on black background
    paste_x = (out_width - new_width) // 2
    paste_y = (out_height - new_height) // 2
    background.paste(img, (paste_x, paste_y))
    return background


def load_data(csv_path, data_dir, row_start, row_end):
    """Load a specified range of image filenames from a CSV.

    Args:
        csv_path (Path): path to the CSV file, in CheXphoto format
        data_dir (Path): the location of the dataset. Concatenating this
            directory name with a path in the CSV should produce a valid
            relative path!
        row_start (int): row index of the first entry to load (inclusive)
        row_end (int): row index of the last entry to load (exclusive). If None,
            all entries until the end will be loaded.

    Returns:
        img_paths ([Path]): list of resolved image paths
        orig_paths ([Path]): list of the raw image paths in the CSV. Used for
            creating the raw image filename that will be later reassociated
            to labels in the original CSV.

    """
    assert Path(csv_path).exists()
    # Load image paths from CSV and resolve relative to data_dir
    df = pd.read_csv(csv_path)

    # Select images based on given range
    orig_paths = list(map(Path, df[COL_PATH]))
    if row_end is None:
        orig_paths = orig_paths[row_start:]
    else:
        orig_paths = orig_paths[row_start:row_end]
    img_paths = list(map(lambda path: data_dir / path, orig_paths))

    # Check that all images in range exist
    for img_path in img_paths:
        assert img_path.exists(), f"Could not locate image {str(img_path)}!"
    return img_paths, orig_paths


def display_img(window_name, img_path, screen_width, screen_height, i):
    """Display an image on the screen, overlaid on a black background.

    Args:
        window_name (str): name of OpenCV window
        img_path (Path): local path to image to load and display
        screen_width (int): width (in px) of the screen
        screen_height (int): height (in px) of the screen
        i (int): the index of the image

    """
    print(f"[{i}]: Showing image {str(img_path)}...")
    img = Image.open(str(img_path)).convert("RGB")
    img = add_background(img, screen_width, screen_height)
    img = np.array(img)[..., ::-1]
    cv2.imshow(window_name, img)


def path_to_filename(seq, orig_path):
    """Convert an image path to a CheXpeditor format filename.

    Args:
        seq (int): the sequence number of the file
        orig_path (Path): the original image path listed in the CSV

    Returns:
        (str): a CheXpeditor format filename, under which the file will be
            saved on the Android device

    """
    # Nonce is needed since Android caches photos with same filename
    nonce = random.randint(0, MAX_NONCE)
    return "__".join([str(seq), str(nonce)] + list(orig_path.parts))


def filename_to_path(name):
    """Parse a CheXpeditor filename and convert it to a Path.

    Args:
        name (str): A CheXpeditor filename

    Returns:
        seq (int): The associated sequence number
        path (Path): The actual path encoded in the filename

    """
    # Parse the name and discard the nonce and original split name
    name_parts = name.split("__")
    seq = int(name_parts[0])
    path = Path(*name_parts[2:])  # name_parts[1] is the nonce, which we skip
    return seq, path


def send_message(ip, port, seq, msg, timeout_s):
    """Send a message to the CheXpeditor server.

    Args:
        ip (str): server IP address
        port (int): server port
        seq (int): message sequence number
        msg (str): message data
        timeout_s (int): how long the client should wait for the server
            response before declaring timeout

    Returns:
        (str): the decoded server response

    """
    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket.settimeout(timeout_s)
    client_socket.sendto((str(seq) + "|" + msg).encode(), (ip, port))
    try:
        data, ip = client_socket.recvfrom(1024)
        return data.decode("utf-8")
    except timeout:
        return "TIMEOUT"
