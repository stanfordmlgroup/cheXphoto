"""Implement blur on a set of images."""
from PIL import ImageFilter


def blur_mapping(level, src_img):
    """Perform the blur effect.

    Args:
        level (int): level of perturbation
        src_img (Image): PIL Image to perturb

    Returns:
        (Image): the Image perturbed by the blur

    """
    if level == 1:
        radius = 1.5
    elif level == 2:
        radius = 3
    elif level == 3:
        radius = 6
    else:
        radius = 10
    return src_img.filter(ImageFilter.GaussianBlur(radius=radius))
