from functions import copier
import argparse

parser = argparse.ArgumentParser(description='Arguments for copying data')

parser.add_argument(
                    '-s',
                    action='store',
                    type=str,
                    help='parent directory containing original data'
                    )

parser.add_argument(
                    '-n',
                    action='store',
                    type=str,
                    help='name of generic file to copy'
                    )

parser.add_argument(
                    '-d',
                    action='store',
                    type=str,
                    help='destination of copied files'
                    )

args = parser.parse_args()

copier(args.s, args.n, args.d)
