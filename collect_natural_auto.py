from natural.chexpeditor_client import get_base_parser, run


def add_auto_args(parser):
    parser.add_argument('--ip', type=str, required=True,
                        help='IP address for CheXpeditor server')

    parser.add_argument('--port', type=int, default=4445,
                        help='Port for CheXpeditor server')

    parser.add_argument('--seq', type=int, default=0,
                        help='Starting sequence no. for synchronization')


if __name__ == '__main__':
    parser = get_base_parser()
    add_auto_args(parser)
    args = parser.parse_args()
    connection = (args.ip, args.port, args.seq)
    run(args.csv_path, args.data_dir, args.row_start, args.row_end, args.screen_width, args.screen_height, delay=None, connection=connection)
