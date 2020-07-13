"""Implement motion blur on a set of images."""
import numpy as np
import cv2
from PIL import Image


def motion_mapping(level, src_img):
    """Perform the motion blur effect.

    Args:
        level (int): level of perturbation,
        src_img (Image): PIL Image to perturb

    Returns:
        (Image): the Image perturbed by the blur

    """
    pil_img = src_img.convert('RGB')
    open_cv = np.array(pil_img)
    img = open_cv[:, :, ::-1].copy()
    if level == 1:
        size = 2
    elif level == 2:
        size = 10
    elif level == 3:
        size = 25
    elif level == 4:
        size = 45

    # generating the kernel
    kernel_motion_blur = np.zeros((size, size))
    kernel_motion_blur[int((size-1)/2), :] = np.ones(size)
    kernel_motion_blur = kernel_motion_blur / size

    # applying the kernel to the input image
    output = cv2.filter2D(img, -1, kernel_motion_blur)
    output = cv2.cvtColor(output.astype(np.uint8), cv2.COLOR_BGR2RGB)

    return Image.fromarray(output)
