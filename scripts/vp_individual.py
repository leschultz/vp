from analysis_functions import vp_iterator
import argparse
import os

parser = argparse.ArgumentParser(
                                 description='Arguments for ICO analysis'
                                 )

parser.add_argument(
                    '-i',
                    action='store',
                    type=str,
                    help='the generic name of the input file'
                    )

parser.add_argument(
                    '-n',
                    action='store',
                    type=str,
                    help='the generic name of trajectory file'
                    )

parser.add_argument(
                    '-t',
                    action='store',
                    type=str,
                    help='the generic name of thermodynamic file'
                    )

parser.add_argument(
                    '-d',
                    action='store',
                    type=str,
                    help='location of data'
                    )

parser.add_argument(
                    '-p',
                    action='store',
                    type=str,
                    help='parent directory name'
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
                    '-o',
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
                 args.i,
                 args.n,
                 args.t,
                 args.d,
                 args.p,
                 edges=args.e,
                 faces=args.f,
                 threshold=args.o
                 )

# Create a folder for analysis data
datadir = os.path.join(*args.s.split('/')[:-1])
if not os.path.exists(datadir):
    os.makedirs(datadir)

df.to_csv(args.s, index=False)
