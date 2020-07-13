"""Generate perturbed dataset.

Usage:
    python synthesize.py --perturbation identity

"""

from argparse import ArgumentParser
from pathlib import Path
from PIL import Image
from tqdm import tqdm
import pandas as pd
import numpy as np
import concurrent.futures

from transforms.constants import LEVELS, PERTURBATIONS


COL_PATH = 'Path'


def parse_script_args():
    """Parse command line arguments.

    Returns:
        args (Namespace): Parsed command line arguments

    """
    parser = ArgumentParser()

    parser.add_argument('--src_csv', type=str,
                        default='/deep/group/chexperturbed/data/' +
                                'CheXpert/dev10K.csv',
                        help='Absolute path to source data csv')

    parser.add_argument('--dst_dir', type=str,
                        default='/deep/group/aihc-bootcamp-spring2020/break/chexperturbed/data/' +
                                'synthetic/CheXpert-10K-digital',
                        help='Destination directory for synthesized data')

    parser.add_argument('--perturbation', type=str,
                        choices=tuple(PERTURBATIONS.keys()),
                        help='Kind of perturbation to apply')
    
    parser.add_argument('--perturbation2', type=str,
                        default="identity",
                        choices=tuple(PERTURBATIONS.keys()),
                        help='Kind of perturbation to apply')

    parser.add_argument('--perturbation3', type=str,
                        default="identity",
                        choices=tuple(PERTURBATIONS.keys()),
                        help='Kind of perturbation to apply')

    parser.add_argument('--level', type=int,
                        choices=tuple(LEVELS),
                        default=1, help='Severity of perturbation')

    parser.add_argument('--split', type=str,
                        choices=('train', 'valid', 'test'),
                        default='train', help='Type of splitting of dataset')

    args = parser.parse_args()
    return args


def get_dst_img_path(src_path, split, perturbed_dir):
    """Transform the src_path into the dst_path.

    Given the path to the original image in the csv,
    derive the path to the corresponding perturbed image

    Args:
        src_path (str): path to original image
        split (str): type of split (train/valid/test)
        perturbed_dir (Path): root of perturbed dataset

    Returns:
        (Path): path to the corresponding perturbed image

    """
    splits = src_path.split('/')
    assert(split in splits)
    index = splits.index(split)
    return perturbed_dir / '/'.join(splits[index:])


def apply_perturbation(perturbation, level, src_img):
    """Apply the specified perturbation to src_img.

    Args:
        perturbation (str): name of perturbation to be applied
        level (int): degree of perturbation (from 1 to 4)
        src_img (Image): the image to perturb

    Returns:
        (Image): the perturbed image

    """
    if perturbation in PERTURBATIONS:
        return PERTURBATIONS[perturbation](level, src_img)
    raise NotImplementedError()

def process_perturbation(path, args, perturbed_dir):
    # TODO: remove the absolute path
    src_img = Image.open(Path('/deep/group/CheXpert/') / path)
    dst_img = apply_perturbation(args.perturbation, args.level, src_img)
    dst_img = apply_perturbation(args.perturbation2, args.level, dst_img)
    dst_img = apply_perturbation(args.perturbation3, args.level, dst_img)
    # write stuff to disk
    dst_path = get_dst_img_path(path, args.split, perturbed_dir)
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    dst_img.save(dst_path)

def generate_data(args):
    """Generate perturbed dataset.

    Args:
        args (Namespace): Parsed command line arguments

    Returns:
        None

    """
    # manages optional additional perturbations
    if (args.perturbation2!="identity"):
        if (args.perturbation3!="identity"):
            perturbed_dir = Path(args.dst_dir) / args.perturbation / args.perturbation2/ args.perturbation3 / f'level_{args.level}'
        else:
            perturbed_dir = Path(args.dst_dir) / args.perturbation / args.perturbation2 / f'level_{args.level}'
    else:
        perturbed_dir = Path(args.dst_dir) / args.perturbation / f'level_{args.level}'
    
    
    perturbed_dir.mkdir(parents=True, exist_ok=True)

    src_df = pd.read_csv(args.src_csv)
    paths = list(src_df[COL_PATH])

    # generate the image using parallel processing
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = [executor.submit(process_perturbation, path, args, perturbed_dir) for path in paths]

        for f in tqdm(concurrent.futures.as_completed(results), total=len(paths)):
            pass
        
    src_df[COL_PATH] = src_df[COL_PATH].apply(get_dst_img_path,
                                              args=(args.split, perturbed_dir))
    src_df.to_csv(perturbed_dir / f'{args.split}.csv', index=False)


if __name__ == '__main__':
    np.random.seed(0)
    args = parse_script_args()
    generate_data(args)
