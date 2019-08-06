from matplotlib import pyplot as pl

import pandas as pd
import numpy as np
import argparse

import os

parser = argparse.ArgumentParser(
                                 description='Arguments for ICO analysis'
                                 )

parser.add_argument(
                    '-n',
                    action='store',
                    type=str,
                    help='the file with fraction data'
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

# Grab the run number
df['number'] = df['run'].apply(lambda x: int(x.split('/')[-1].split('_')[-1]))
df['group'] = df['run'].apply(lambda x: x.split('/')[1])
df = df.sort_values(by='number')  # Order by run number

groupcols = ['group', 'temperature']
groups = df.groupby(groupcols)

# Create folder for plots
plotpath = os.path.join(args.p, 'fraction_vs_count')
if not os.path.exists(plotpath):
    os.makedirs(plotpath)

for group, data in groups:

    # Running mean
    frac_mean = []
    frac_std = []
    frac_sem = []
    frac_count = []
    for i in range(2, data.shape[0]+1):
        fracs = data['fraction'].values[:i]
        mean = np.mean(fracs)
        std = np.std(fracs, ddof=1)
        count = len(fracs)
        sem = std/(count**0.5)

        frac_mean.append(mean)
        frac_std.append(std)
        frac_sem.append(sem)
        frac_count.append(count)

    fig, ax = pl.subplots()

    groupstr = str(group)
    ax.errorbar(
                frac_count,
                frac_mean,
                frac_std,
                marker='.',
                linestyle='none',
                ecolor='r',
                label='STDEV: '+groupstr
                )

    ax.errorbar(
                frac_count,
                frac_mean,
                frac_sem,
                marker='.',
                linestyle='none',
                ecolor='y',
                label='SEM: '+groupstr
                )

    ax.legend()
    ax.grid()

    ylabel = r'Fraction of VP $(n_{'+str(args.e)+r'}\geq'+str(args.f)+r')$'
    ax.set_xlabel('Number of Runs')
    ax.set_ylabel(ylabel)
    ax.set_xticks(frac_count)

    fig.tight_layout()

    savename = list(map(lambda x: str(x), list(group)))
    savename = '_'.join(savename)
    savename = os.path.join(plotpath, savename)
    savename += '.png'

    fig.savefig(savename)
    pl.close('all')
