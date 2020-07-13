"""Build a dataset out of a flat directory of CheXpeditor outputs from auto mode.

This should be run after copying the CheXpeditor photos to a locally accessible path.

The following example assumes that the CheXphoto-v1.0 folder is located in a
directory called data/:
    python compile_csv_from_chexpeditor.py
        --src_csv_path data/CheXphoto-v1.0/valid/valid.csv
        --src_row_start 0
        --src_row_end 3
        --chexpeditor_export_dir local/path/to/chexpeditor/outputs/
        --dst_data_dir output/
        --dst_dataset_name MorePhotos
        --dst_csv_path output/MorePhotos_labels.csv

Note that the --dst_dataset_name is prepended to the original image path in the source
CSV. For example, if an image had the following path in the source dataset:
    CheXphoto-v1.0/valid/synthetic/digital/patient64542/study1/view1_frontal.png
Then specifying --dst_dataset_name MorePhotos would prepend to the path, giving:
    MorePhotos/CheXphoto-v1.0/valid/synthetic/digital/patient64542/study1/view1_frontal.png
This ensures that images from the original dataset are not mixed with the new one, and
also serves as a rudimentary form of revision history.

For more detailed information about the available args, please run:
    python compile_csv_from_chexpeditor.py --help

"""
from argparse import ArgumentParser
from pathlib import Path, PurePosixPath
from shutil import copy

import pandas as pd
from tqdm import tqdm

from chexpeditor.util import filename_to_path

COL_PATH = "Path"


def parse_script_args():
    """Parse command line arguments.

    Returns:
        args (Namespace): Parsed command line arguments

    """
    parser = ArgumentParser()

    parser.add_argument(
        "--src_csv_path",
        type=str,
        required=True,
        help="Path to original source CSV (--csv_path in collect_natural_auto.py)",
    )

    parser.add_argument(
        "--src_row_start",
        type=int,
        required=True,
        help="Starting row of source data range (inclusive)",
    )

    parser.add_argument(
        "--src_row_end",
        type=int,
        required=True,
        help="Ending row of source data range (exclusive)",
    )

    parser.add_argument(
        "--chexpeditor_export_dir",
        type=str,
        required=True,
        help="Local directory containing CheXpeditor outputs",
    )

    parser.add_argument(
        "--dst_data_dir",
        type=str,
        required=True,
        help="Where the output images should be saved, preserving the original directory structure",
    )

    parser.add_argument(
        "--dst_dataset_name",
        type=str,
        required=True,
        help="Name for generated dataset, which will be prepended to paths in destination CSV",
    )

    parser.add_argument(
        "--dst_csv_path",
        type=str,
        required=True,
        help="Save location for the CSV of the transformed dataset",
    )

    parser.add_argument(
        "--copy", type=bool, default=True, help="Specify False to only generate a CSV"
    )

    args = parser.parse_args()

    assert (
        args.src_row_end > args.src_row_start
    ), f"Starting row {args.src_row_start} must be strictly less than ending row {args.src_row_end}!"
    args.chexpeditor_export_dir = Path(args.chexpeditor_export_dir)
    args.src_csv_path = Path(args.src_csv_path)
    args.dst_data_dir = Path(args.dst_data_dir)
    args.dst_csv_path = Path(args.dst_csv_path)

    return args


if __name__ == "__main__":
    args = parse_script_args()

    # Create data directory
    args.dst_data_dir.mkdir(exist_ok=True, parents=True)

    # Parse filenames and copy to directories
    names = []
    for src_file_path in tqdm(list(args.chexpeditor_export_dir.iterdir())):
        name = src_file_path.name
        seq, parsed_path = filename_to_path(name)
        names.append((seq, parsed_path))
        dst_file_path = args.dst_data_dir / args.dst_dataset_name / parsed_path
        dst_file_path.parent.mkdir(exist_ok=True, parents=True)
        if args.copy:
            copy(src_file_path, dst_file_path)

    # Sort names by sequence number
    names.sort(key=lambda x: x[0])
    names = [name[1] for name in names]

    # Check for consistency and correspondence
    df = pd.read_csv(args.src_csv_path)
    df = df.iloc[args.src_row_start : args.src_row_end]
    src_paths = list(df[COL_PATH])
    dst_paths = []
    assert len(src_paths) == len(names)
    for src_path, name in zip(src_paths, names):
        assert str(Path(src_path)) == str(Path(name))
        dst_paths.append(str(PurePosixPath(args.dst_dataset_name) / src_path))

    # Update the path column and create the new CSV
    df[COL_PATH] = dst_paths
    df.to_csv(args.dst_csv_path, index=False)
