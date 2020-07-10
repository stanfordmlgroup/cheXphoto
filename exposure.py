"""Implement exposure correction on a set of images."""
import numpy as np
from PIL import Image
from skimage import exposure


def exposure_mapping(level, src_img):
    """Perform contrast adjustment.

    Args:
        level (int): level of perturbation
        src_img (Image): PIL Image to perturb

    Returns:
        (Image): the Image perturbed by the exposure shift

    """
    image = np.asarray(src_img)
    # min 0.5, max 2
    # ) = I ** gama after scaling 0 to 1
    #expose = exposure.adjust_gamma(image, gamma=(level/5.0)*1.5 + 0.5, gain=1)

    #expose = exposure.adjust_log(image, gain=1.1)

    expose = exposure.adjust_sigmoid(image, cutoff= 0.5, gain=5)

    #expose = exposure.equalize_hist(image)
    return Image.fromarray(expose, "RGB")

