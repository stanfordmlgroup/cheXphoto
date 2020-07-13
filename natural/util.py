import numpy as np
from PIL import Image
from pathlib import Path
import pandas as pd
import cv2
import random
from socket import AF_INET, SOCK_DGRAM, socket, timeout

MAX_NONCE = 100
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
    orig_paths = list(map(Path, df[COL_PATH]))
    img_paths = list(map(lambda path: data_dir / path, orig_paths))
    # Select images based on given range
    if row_end is None:
        img_paths = img_paths[row_start:]
    else:
        img_paths = img_paths[row_start: row_end]
    # Check that all images in range exist
    for img_path in img_paths:
        assert img_path.exists(), f"Could not locate image {str(img_path)}!"
    return img_paths, orig_paths


def display_img(window_name, img_path, screen_width, screen_height, i):
    print(f'[{i}]: Showing image {str(img_path)}...')
    # Need to convert back to str for compatibility with Win-SSHFS
    img = Image.open(str(img_path)).convert('RGB')
    img = add_background(img, screen_width, screen_height)
    img = np.array(img)[..., ::-1]
    cv2.imshow(window_name, img)


def path_to_filename(seq, img_path):
    # Nonce is needed since Android caches photos with same filename
    nonce = random.randint(0, MAX_NONCE)
    return '__'.join([str(seq), str(nonce)] + list(img_path.parts))


def send_message(ip, port, seq, msg, timeout_s):
    """Send a message to the CheXpeditor server.

    Args:
        ip (str): server IP address
        port (int): server port
        seq (int): message sequence number
        msg (str): message data

    Returns:
        (str): the decoded server response

    """
    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket.settimeout(timeout_s)
    client_socket.sendto((str(seq) + '|' + msg).encode(), (ip, port))
    try:
        data, ip = client_socket.recvfrom(1024)
        return data.decode('utf-8')
    except timeout:
        return 'TIMEOUT'
