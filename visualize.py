"""Visualize all perturbations and levels for a given image."""

import numpy as np

from PIL import Image
from argparse import ArgumentParser
from pathlib import Path

from constants import LEVELS, PERTURBATIONS


FIG_SIZE = (12, 8)


def visualize(img, perturbations, levels, show):
    """Visualize all specified perturbations and levels for a given image.

    Args:
        img (Image): PIL image for which to plot perturbations
        perturbations (dict): maps name (str) -> mapping function (function)
        levels (list): list of each level (int) to plot
        show (bool): whether to show the final figure

    Returns:
        (None)

    """
    # Workaround to allow code to run without display attached
    import matplotlib
    if not show:
        matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    out_dir = Path('output')
    out_dir.mkdir(exist_ok=True, parents=True)

    # Don't visualize identity
    if 'identity' in perturbations:
        perturbations = perturbations.copy()
        del perturbations['identity']
    fig, ax = plt.subplots(nrows=len(levels),
                           ncols=len(perturbations),
                           gridspec_kw={'wspace': 0, 'hspace': 0},
                           figsize=FIG_SIZE)
    names = sorted(list(perturbations.keys()))
    for iname, name in enumerate(names):
        print('Generating visuals for "%s"...' % name)
        mapping_fn = perturbations[name]
        for ilevel, level in enumerate(levels):
            perturbed_img = mapping_fn(level, img)
            perturbed_img_name = '%s_%d.png' % (name, level)
            perturbed_img.save(out_dir / perturbed_img_name)
            ax[ilevel, iname].imshow(perturbed_img)
            # Remove tick marks
            ax[ilevel, iname].set_yticklabels([])
            ax[ilevel, iname].set_xticklabels([])
            ax[ilevel, iname].tick_params(axis='both',
                                          which='both',
                                          length=0)
            # Plot vertical and horizontal titles
            if not iname:
                ax[ilevel, iname].set_ylabel('Level %d' % level,
                                             rotation=90,
                                             size='large')
            if not ilevel:
                ax[ilevel, iname].set_title(name)
    if show:
        plt.show()
    plt.savefig(out_dir / 'visualization.png')


def parse_script_args():
    """Parse command line arguments.

    Returns:
        args (Namespace): Parsed command line arguments

    """
    parser = ArgumentParser()

    parser.add_argument('--img_path', type=str,
                        default='test_images/xray.jpg',
                        help='Path to image to visualize')

    parser.add_argument('--no_show', action='store_true',
                        help='Whether to not show the final figure.')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_script_args()
    np.random.seed(0)
    src_img = Image.open(args.img_path)
    visualize(src_img, PERTURBATIONS, LEVELS, not args.no_show)
