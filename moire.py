"""Implement a synthetic Moire effect."""

import numpy as np
from PIL import Image


def moire_mapping(level, src_img):
    """Perform the Moire mapping.

    Args:
        level (int): level of perturbation
        src_img (Image): PIL Image to perturb

    Returns:
        (Image): the Image perturbed by the Moire mapping

    """
    if level == 1:
        gap = 20
        opacity = 0.05
    elif level == 2:
        gap = 4.5
        opacity = 0.15
    elif level == 3:
        gap = 2.5
        opacity = 0.35
    else:
        gap = 1
        opacity = 0.5

    return moire(src_img, upsample_factor=2,
                 thickness=1,
                 gap=gap,
                 opacity=opacity,
                 darkness=1.0,
                 mask_params=[(90, 0.5, (np.random.uniform(0, 100),
                                         np.random.uniform(0, 100))),
                              (90 + np.random.normal(0, 1), 0.5,
                               (np.random.uniform(0, 100),
                                np.random.uniform(0, 100)))])


def moire(img, upsample_factor, thickness, gap, opacity, darkness,
          mask_params):
    """Simulate a Moire effect.

    Generate semi-transparent masks consisting of parallel lines, which are
    then warped, rotated, cropped, and alpha-composited onto the original
    image. Original image is upsampled before applying masks and downsampled
    to original size afterwards, to induce additional artifacts.

    Args:
        img (Image): PIL Image on which to apply the Moire effect
        upsample_factor (float): upsampling factor in [1, +inf)
        thickness (int): width of mask lines in pixels
        gap (int): gap between adjacent mask lines in pixels
        opacity (float): opacity of mask lines in [0, 1]
        darkness (float): darkness of mask lines in [0, 1]
        mask_params (list): list of (angle, spread, offset), which control
            various aspects of mask appearance.
            angle (float): counterclockwise rotation of mask (in degrees)
            spread (float): How much to warp lines to converge in [0, 1]
            offset ((int, int)): (x, y) offset of mask in pixels

    Returns:
        (Image): the Image perturbed by the Moire effect

    """
    # Add alpha channel to image
    img = img.convert('RGBA')
    # Upsample the image according to upsample_factor
    upsample_size = (img.width * upsample_factor, img.height * upsample_factor)
    img_resize = img.resize(upsample_size, Image.ANTIALIAS)
    # Make mask large enough so it can still contain the image when rotated
    mask_dim = max(img_resize.size) * 2
    # Create a mask with the specified parameters
    base_mask = generate_base_mask((mask_dim, mask_dim), thickness,
                                   gap, opacity, darkness)
    # Apply transformations on the base mask, and use alpha compositing to
    # paste them onto the image
    for angle, spread, offset in mask_params:
        mask = transform_mask(base_mask, img_resize.size, angle, spread,
                              offset)
        img_resize.alpha_composite(mask, (0, 0))
    # Downsample back to the original image size
    img = img_resize.resize(img.size, Image.ANTIALIAS)
    # Remove alpha channel for JPEG export
    img = img.convert('RGB')
    return img


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


def transform_mask(mask, out_size, angle, spread, offset):
    """Apply a transformation to a mask to enhance realism.

    Args:
        mask (Image): RGBA mask image
        out_size (tuple): (width, height) of the output mask
        angle (float): counterclockwise rotation of mask (in degrees)
        spread (float): How much to warp lines to converge in [0, 1]
        offset ((int, int)): (x, y) offset of mask in pixels

    Returns:
        (Image): transformed mask of size out_size

    """
    # Warp mask with PIL perspective transform to induce spread
    coeffs = find_coeffs([(0, 0), (mask.width, 0),
                          (mask.width, mask.height), (0, mask.height)],
                         [(0, mask.height * (0.5 - spread / 2)),
                          (mask.width, 0), (mask.width, mask.height),
                          (0, mask.height * (0.5 + spread / 2))])
    mask = mask.transform(mask.size, Image.PERSPECTIVE, data=coeffs)
    # Rotate mask
    mask = mask.rotate(angle)
    # Offset mask and crop to desired output size
    left = (mask.width - out_size[0]) // 2
    upper = (mask.height - out_size[1]) // 2
    mask = mask.crop((left + offset[0],
                      upper + offset[1],
                      left + offset[0] + out_size[0],
                      upper + offset[1] + out_size[1]))
    return mask


def generate_base_mask(mask_size, thickness, gap, opacity, darkness):
    """Generate a base mask that can be later transformed.

    The base mask consists of semi-transparent horizontal parallel lines
    separated by fully transparent gaps.

    Args:
        mask_size (tuple): (width, height) of the mask to generate
        thickness (int): width of mask lines in pixels
        gap (int): gap between adjacent mask lines in pixels
        opacity (float): opacity of mask lines in [0, 1]
        darkness (float): darkness of mask lines in [0, 1]

    Returns:
        (Image): RGBA base mask of size mask_size

    """
    width, height = mask_size
    mask = np.zeros((height, width, 4), dtype=np.uint8)
    # Compute the dark (semi-transparent) and light (transparent) rows
    remainders = np.remainder(np.arange(height), thickness + gap)
    dark_rows = np.nonzero(remainders < thickness)
    light_rows = np.nonzero(remainders >= thickness)
    # Set the opacity of the dark rows
    mask[dark_rows, :, 3] = int(opacity * 255)
    # Set the color of the dark rows
    mask[dark_rows, :, :3] = int((1 - darkness) * 255)
    # Convert np.ndarray to PIL Image for further processing
    return Image.fromarray(np.uint8(mask))
