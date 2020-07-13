"""Implement 3-D tilt perturbation on a set of images."""
import numpy as np
from PIL import Image


def find_coeffs(pa, pb):
    """Calculate parameters for PIL perspective transform.

    Source:
        https://stackoverflow.com/questions/14177744/

    Args:
        pa (list): list of 4 (x, y) points to map to pb
        pb (list): list of 4 (x, y) points to be mapped from pa

    Returns:
        (np.ndarray): parameters for PIL perspective transform
    """
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = np.matrix(matrix, dtype=np.float)
    B = np.array(pb).reshape(8)

    res = np.dot(np.linalg.inv(A.T * A) * A.T, B)
    return np.array(res).reshape(8)


def tilt_mapping(level, src_img):
    """Perform a 3-D tilt transformation.

    Args:
        level (int): level of perturbation
        src_img (Image): PIL Image to perturb

    Returns:
        (Image): the Image perturbed by the tilt

    """
    width, height = src_img.size
    degree = level * 0.05
    coeffs = find_coeffs(
        [(width * np.random.uniform(0, degree),
          height * np.random.uniform(0, degree)),
         (width * np.random.uniform(1 - degree, 1),
          height * np.random.uniform(0, degree)),
         (width * np.random.uniform(1 - degree, 1),
          height * np.random.uniform(1 - degree, 1)),
         (width * np.random.uniform(0, degree),
          height * np.random.uniform(1 - degree, 1))],
        [(0, 0), (width, 0), (width, height), (0, height)])

    img = src_img.transform((width, height),
                            Image.PERSPECTIVE,
                            coeffs,
                            Image.BICUBIC)
    return img
