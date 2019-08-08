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

# Create folders for plots
meanpath = os.path.join(
                        args.p,
                        'fraction_vs_count_e'+str(args.e)+'_geq_f'+str(args.f)
                        )

if not os.path.exists(meanpath):
    os.makedirs(meanpath)

stdpath = os.path.join(
                       args.p,
                       'std_vs_count_e'+str(args.e)+'_geq_f'+str(args.f)
                       )

if not os.path.exists(stdpath):
    os.makedirs(stdpath)

sempath = os.path.join(
                       args.p,
                       'sem_vs_count_e'+str(args.e)+'_geq_f'+str(args.f)
                       )

if not os.path.exists(sempath):
    os.makedirs(sempath)

for group, data in groups:

    # Running mean
    frac_mean = []
    frac_std = []
    frac_std_percent = []
    frac_sem = []
    frac_sem_percent = []
    frac_count = []
    for i in range(2, data.shape[0]+1):
        fracs = data['fraction'].values[:i]

        count = len(fracs)  # Number of values
        mean = np.mean(fracs)  # Mean of values

        std = np.std(fracs, ddof=1)  # Standard deviation
        std_percent = std/mean*100.0  # STD percent error

        sem = std/(count**0.5)  # Standard error in the mean
        sem_percent = sem/mean*100.0  # SEM percent error

        frac_mean.append(mean)
        frac_std.append(std)
        frac_std_percent.append(std_percent)
        frac_sem.append(sem)
        frac_sem_percent.append(sem_percent)
        frac_count.append(count)

    # If the number of runs is less than two skip
    if not frac_mean:
        continue

    # Plot mean vs the number of runs
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

    fig.tight_layout()

    savename = list(map(lambda x: str(x), list(group)))
    savename = '_'.join(savename)
    savename = os.path.join(meanpath, savename)
    savename += '.png'

    fig.savefig(savename)
    pl.close('all')

    # General y label
    ygeneral = ' of VP $(n_{'+str(args.e)+r'}\geq'+str(args.f)+r')$'

    # Plot std vs the number of runs
    fig, ax1 = pl.subplots()

    ax1.plot(
             frac_count,
             frac_std,
             marker='.',
             linestyle='none',
             label='STDEV: '+groupstr
             )

    ax1.legend()
    ax1.grid()

    ax1.set_xlabel('Number of Runs')

    ylabel = r'STDEV'+ygeneral
    ax1.set_ylabel(ylabel)

    ax2 = ax1.twinx()
    ax2.set_ylabel(r'$\%$ '+ylabel)
    ax2.set_ylim(min(frac_std_percent), max(frac_std_percent))

    fig.tight_layout()

    savename = list(map(lambda x: str(x), list(group)))
    savename = '_'.join(savename)
    savename = os.path.join(stdpath, savename)
    savename += '.png'

    fig.savefig(savename)
    pl.close('all')

    # Plot sem vs the number of runs
    fig, ax1 = pl.subplots()

    ax1.plot(
             frac_count,
             frac_sem,
             marker='.',
             linestyle='none',
             label='SEM: '+groupstr
             )

    ax1.legend()
    ax1.grid()

    ax1.set_xlabel('Number of Runs')

    ylabel = r'SEM'+ygeneral

    ax1.set_ylabel(ylabel)

    ax2 = ax1.twinx()
    ax2.set_ylabel(r'$\%$ '+ylabel)
    ax2.set_ylim(min(frac_sem_percent), max(frac_sem_percent))

    fig.tight_layout()

    savename = list(map(lambda x: str(x), list(group)))
    savename = '_'.join(savename)
    savename = os.path.join(sempath, savename)
    savename += '.png'

    fig.savefig(savename)
    pl.close('all')
