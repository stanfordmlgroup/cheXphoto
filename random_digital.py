"""Randomly increase or reduce brightness and contrast on a set of images."""
import numpy as np
from brightness_up import brightness_up_mapping
from brightness_down import brightness_down_mapping
from contrast_up import contrast_up_mapping
from contrast_down import contrast_down_mapping
import random

def random_digital_mapping(level, src_img):
    """Perform the successive digital effects.

    Args:
        level (int): level of perturbation
        src_img (Image): PIL Image to perturb

    Returns:
        (Image): the Image perturbed by the two transformations

    """
    contrast_img = contrast_up_mapping(level, src_img) if bool(random.getrandbits(1)) else contrast_down_mapping(level, src_img)
    img = brightness_up_mapping(level, contrast_img) if bool(random.getrandbits(1)) else brightness_down_mapping(level, contrast_img)
    return img
