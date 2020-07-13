from natural.chexpeditor_client import get_base_parser, run


def add_manual_args(parser):
    parser.add_argument('--delay', type=int, default=0,
                        help='Interval in between images (in ms)')


if __name__ == '__main__':
    parser = get_base_parser()
    add_manual_args(parser)
    args = parser.parse_args()
    run(args.csv_path, args.data_dir, args.row_start, args.row_end, args.screen_width, args.screen_height, delay=args.delay, connection=None)
