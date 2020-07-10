"""Implement the identity mapping, which is a no-op."""


def identity_mapping(level, src_img):
    """Perform the identity mapping.

    Args:
        level (int): level of perturbation, N/A here
        src_img (Image): PIL Image to perturb

    Returns:
        (Image): the Image perturbed by the identity mapping

    """
    return src_img
