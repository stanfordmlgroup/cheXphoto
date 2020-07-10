"""Implement a synthetic glare effect."""

import numpy as np
from PIL import Image
from scipy.stats import multivariate_normal


# TODO: explore other possible covariance matrices
# TODO: another type of boundary which is a line
def glare_matte_mapping(level, src_img):
    """Perform the glare matte mapping.

    Args:
        level (int): level of perturbation
        src_img (Image): PIL Image to perturb
    Returns:
        (Image): the Image perturbed by the glare mapping

    """
    width, height = src_img.size
    cov = (level*50) ** 2
    return glare_matte(src_img, [([np.random.uniform(0, width),
                                   np.random.uniform(0, height)],
                                  [[cov, 0], [0, cov]], level*100)], level)


def glare_matte(img, mask_params, level):
    """Simulate a glare effect.

    Generate semi-transparent white masks where opacity is determined by a
    2-dimensional Gaussian. Masks are directly alpha-composited onto the
    image.

    Args:
        img (Image): PIL image on which to apply the glare effect
        mask_params (list): list of (mean, cov, max_val), which control
            various aspects of mask appearance.
            mean (np.ndarray): (x, y) point about which Gaussian is centered
            cov (np.ndarray): 2x2 matrix controlling spread of Gaussian
            max_val (float): value to normalize values to before clamping
        level (int): level of perturbation

    """
    img = img.convert('RGBA')
    for mean, cov, max_val in mask_params:
        mask = generate_glare_mask(img.size, mean, cov, max_val, level)
        img.alpha_composite(mask)
    img = img.convert('RGB')
    return img


def generate_glare_mask(mask_size, mean, cov, max_val, level):
    """Generate a glare mask from a 2-dimensional Gaussian.

    Args:
        mask_size (tuple): (width, height) of the mask to generate
        mean (np.ndarray): (x, y) point about which Gaussian is centered
        cov (np.ndarray): 2x2 matrix controlling spread of Gaussian
        max_val (float): value to normalize values to before clamping
        level (int): level of perturbation

    Returns:
        (Image): RGBA base mask of size mask_size

    """
    width, height = mask_size
    mask = np.zeros((height, width, 4), dtype=float)
    # Set mask to be all white
    mask[:, :, :3] = 255
    # Spatially compute normal PDF values
    normal = multivariate_normal(mean=mean, cov=cov)
    x_vals, y_vals = np.meshgrid(np.arange(width), np.arange(height))
    vals = np.stack([x_vals, y_vals], axis=-1)
    alpha = normal.pdf(vals)
    # Set alpha channel to renormalized and clamped PDF values
    mask[:, :, 3] = np.fmin(150 + 20*level, alpha * max_val / np.max(alpha))
    # Convert np.ndarray to PIL Image for further processing
    return Image.fromarray(np.uint8(mask))
