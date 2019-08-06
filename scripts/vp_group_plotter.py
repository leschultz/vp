from matplotlib import pyplot as pl

import pandas as pd
import argparse

import os

parser = argparse.ArgumentParser(
                                 description='Arguments for ICO analysis'
                                 )

parser.add_argument(
                    '-n',
                    action='store',
                    type=str,
                    help='the file with grouped fraction data'
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
                    '-p',
                    action='store',
                    type=str,
                    help='the path to save plots'
                    )

args = parser.parse_args()

df = pd.read_csv(args.n)

groupcols = ['run', 'temperature']
groups = df.groupby(groupcols)

# Create folder for plots
plotpath = os.path.join(args.p, 'fraction_vs_atoms')
if not os.path.exists(plotpath):
    os.makedirs(plotpath)

for group, data in groups:

    fig, ax = pl.subplots()

    groupstr = str(group)
    ax.errorbar(
                data['atoms'],
                data['fraction_mean'],
                data['fraction_std'],
                marker='.',
                linestyle='none',
                ecolor='r',
                label='STDEV: '+groupstr
                )

    ax.errorbar(
                data['atoms'],
                data['fraction_mean'],
                data['fraction_sem'],
                marker='.',
                linestyle='none',
                ecolor='y',
                label='SEM: '+groupstr
                )

    ax.legend()
    ax.grid()

    ylabel = r'Fraction of VP $(n_{'+str(args.e)+r'}\geq'+str(args.f)+r')$'
    ax.set_xlabel('Number of Atoms')
    ax.set_ylabel(ylabel)

    fig.tight_layout()

    savename = list(map(lambda x: str(x), list(group)))
    savename = '_'.join(savename)
    savename = os.path.join(plotpath, savename)
    savename += '.png'

    fig.savefig(savename)
    pl.close('all')
