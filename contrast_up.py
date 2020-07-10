"""Implement contrast on a set of images."""
import numpy as np
from PIL import ImageEnhance


def contrast_up_mapping(level, src_img):
    """Perform contrast adjustment.

    Args:
        level (int): level of perturbation
        src_img (Image): PIL Image to perturb

    Returns:
        (Image): the Image perturbed by the contrast

    """
    if level == 1:
        factor = 0.5
    else:
        factor = level
    noisy_factor = 1 + factor * 0.2 + np.random.uniform(-0.01, 0.01)
    return ImageEnhance.Contrast(src_img).enhance(noisy_factor)
