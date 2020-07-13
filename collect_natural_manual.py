from argparse import ArgumentParser
from natural import chexpeditor_client


def parse_script_args():
    """Parse command line arguments.

    Returns:
        args (Namespace): Parsed command line arguments

    """
    parser = ArgumentParser()

    parser.add_argument('--csv_path', type=str,
                        required=True,
                        help='Path to data CSV')

    parser.add_argument('--data_dir', type=str,
                        required=True,
                        help='The directory in which CheXphoto is located')

    parser.add_argument('--delay', type=int, default=0,
                        help='Interval in between images (in ms)')

    parser.add_argument('--row_start', type=int, default=0,
                        help='Image # of CSV to display. 0 is first image')

    parser.add_argument('--row_end', type=int,
                        help='Image # of CSV to display (non-inclusive)')

    parser.add_argument('--screen_height', type=int, required=True,
                        help='Height of target screen (in px)')

    parser.add_argument('--screen_width', type=int, required=True,
                        help='Width of target screen (in px)')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_script_args()
    chexpeditor_client.run(args.csv_path, args.data_dir, args.row_start, args.row_end, args.screen_width, args.screen_height, args.delay, connection=None)
