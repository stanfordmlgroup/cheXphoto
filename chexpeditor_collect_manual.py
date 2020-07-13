"""Run manual collection of naturally perturbed images using CheXpeditor.

The following example assumes that the CheXphoto-v1.0 folder is located in a
directory called data/:
    python chexpeditor_collect_manual.py
        --csv_path data/CheXphoto-v1.0/valid/valid.csv
        --data_dir data/
        --row_start 3
        --row_end 10
        --screen_width 1920
        --screen_height 1080
        --delay 1000  # in milliseconds

For more detailed information about the available args, please run:
    python chexpeditor_collect_manual.py --help

"""

from chexpeditor.client import get_base_parser, run


def add_manual_args(parser):
    parser.add_argument(
        "--delay",
        type=int,
        default=0,
        help="Interval in between images (in ms). Omit to require a keypress to advance.",
    )


if __name__ == "__main__":
    parser = get_base_parser()
    add_manual_args(parser)
    args = parser.parse_args()
    run(
        args.csv_path,
        args.data_dir,
        args.row_start,
        args.row_end,
        args.screen_width,
        args.screen_height,
        delay=args.delay,
        connection=None,
    )
