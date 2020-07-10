"""Implement rotation perturbation on a set of images."""
import numpy as np
from PIL import Image
import cv2
import random

def rotation_mapping(level, src_img):
    """Perform a black background rotation transformation.
    Args:
        level (int): level of perturbation
        src_img (Image): PIL Image to perturb

    Returns:
        (Image): the Image perturbed by the rotation

    """
    pil_img = src_img.convert('RGB')
    open_cv = np.array(pil_img)
    img = open_cv[:, :, ::-1].copy()
    width, height = src_img.size
    rot = 5 * level # min 15, max 60
    if bool(random.getrandbits(1)): rot *= -1
    border_buffer = 0

    matrix = cv2.getRotationMatrix2D((width//2, height//2), rot, 1.0)
    cos, sin = np.abs(matrix[0, 0]), np.abs(matrix[0, 1])

    nW = int((height * sin) + (width * cos)) + border_buffer
    nH = int((height * cos) + (width * sin)) + border_buffer

    matrix[0, 2] += (nW / 2) - (width//2)
    matrix[1, 2] += (nH / 2) - (height//2)

    output = cv2.warpAffine(img, matrix, (nW, nH))

    return Image.fromarray(output)
