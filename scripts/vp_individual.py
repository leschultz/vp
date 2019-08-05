from functions import vp_iterator
import argparse

parser = argparse.ArgumentParser(
                                 description='Arguments for ICO analysis'
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
                    help='location of data'
                    )

parser.add_argument(
                    '-e',
                    action='store',
                    type=int,
                    help='number of edges to consider'
                    )

parser.add_argument(
                    '-f',
                    action='store',
                    type=int,
                    help='minimum number of faces for considered edge index'
                    )

parser.add_argument(
                    '-t',
                    action='store',
                    type=float,
                    help='the minimum length for a Voronoi polyhedra edge'
                    )

parser.add_argument(
                    '-s',
                    action='store',
                    type=str,
                    help='the file to save fraction data'
                    )

args = parser.parse_args()

df = vp_iterator(
                 args.n,
                 args.d,
                 edges=args.e,
                 faces=args.f,
                 threshold=args.t
                 )

df.to_csv(args.s, index=False)
