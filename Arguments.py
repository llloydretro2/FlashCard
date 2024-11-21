import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Parameters for server')
    parser.add_argument(
        '--share',
        action='store_true',
        default=False,
        help='Whether launch server to share, add -s to share link')
    parser.add_argument('--card_path',
                        type=str,
                        default='Cards',
                        help='The path of the flashcards')

    return parser.parse_args()
