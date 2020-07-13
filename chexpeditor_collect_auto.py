"""Run automatic collection of naturally perturbed images using CheXpeditor.

Before running this, please read the repo README to set up the server component on
your Android device.

The following example assumes that the CheXphoto-v1.0 folder is located in a
directory called data/:
    python chexpeditor_collect_auto.py
        --csv_path data/CheXphoto-v1.0/valid/valid.csv
        --data_dir data/
        --row_start 3  # must match starting row in CheXpeditor app
        --row_end 10
        --screen_width 1920
        --screen_height 1080
        --ip 10.0.2.127  # dummy IP, use one shown in CheXpeditor app

For more detailed information about the available args, please run:
    python chexpeditor_collect_auto.py --help

"""
from chexpeditor.client import get_base_parser, run


def add_auto_args(parser):
    parser.add_argument(
        "--ip", type=str, required=True, help="IP address for CheXpeditor server"
    )

    parser.add_argument(
        "--port", type=int, default=4445, help="Port for CheXpeditor server"
    )


if __name__ == "__main__":
    parser = get_base_parser()
    add_auto_args(parser)
    args = parser.parse_args()
    connection = (args.ip, args.port)
    run(
        args.csv_path,
        args.data_dir,
        args.row_start,
        args.row_end,
        args.screen_width,
        args.screen_height,
        delay=None,
        connection=connection,
    )
