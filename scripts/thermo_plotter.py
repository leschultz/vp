'''
Plot all thermodynamic variables as a function of time for equillibration and
data gathering portions.
'''

from matplotlib import pyplot as pl
from vp_run_functions import *
from functions import finder
from scipy import stats

import pandas as pd
import numpy as np

import sys
import os

runsdir = sys.argv[1]  # The path to the run set
runin = sys.argv[2]  # The name for the input file
sigma = float(sys.argv[3])  # The confidence interval for statistical tests

# Count all mathching paths
runs = finder('system.txt', runsdir)
count = str(len(runs))

newcount = 1
for path in runs:

    print('Run ('+str(newcount)+'/'+str(count)+'): '+path)

    param = input_parse(os.path.join(path, runin))

    # The units used for the simulation
    units_metal = units('metal')

    # Gather thermodynamic data
    cols, df = system_parse(os.path.join(path, 'system.txt'))
    df = pd.DataFrame(df, columns=cols)
    df['Time'] = df['TimeStep']*param['timestep']  # Time in [ps]

    # Create folder for plots thermodynamic data
    plotdir = os.path.join(*[path, 'plots', 'thermodynamic'])
    if not os.path.exists(plotdir):
        os.makedirs(plotdir)

    # Create a folder for analysis data
    datadir = os.path.join(*[path, 'data', 'thermodynamic'])
    if not os.path.exists(datadir):
        os.makedirs(datadir)

    # Start plotting thermodynamic data vs time
    x = df['Time'].values
    for col in df.columns:

        # Skip time values
        if ('TimeStep' == col) or ('Time' == col):
            continue

        y = df[col].values

        fig, ax = pl.subplots()

        ax.plot(x, y, marker='.', linestyle='none')

        ax.grid()

        ax.set_ylabel(col+' ['+units_metal[col]+']')
        ax.set_xlabel('Time [ps]')

        fig.tight_layout()
        pl.savefig(os.path.join(plotdir, col))
        pl.close('all')

    # Divide data by steps and get settled volume
    prev = 0  # All steps should start at 0
    vols = []
    for step in np.cumsum(param['holdsteps']):
        d = df[(df['TimeStep'] >= prev) & (df['TimeStep'] <= step)]
        vol = d['Volume'].values
        vols.append(np.mean(vol[abs(vol-np.mean(vol)) < sigma*np.std(vol)]))

        prev = step  # To devine the beggining of the next step

    holdtemps = param['temperatures']

    # Mean volumes for settled data
    dfvol = pd.DataFrame({'Temperature': holdtemps, 'Volume': vols})
    dfvol.to_csv(os.path.join(datadir, 'mean_volumes'), index=False)

    fit = stats.linregress(holdtemps, vols)
    m, b, r = fit[:3]

    tempfit = np.linspace(min(holdtemps), max(holdtemps))
    volfit = tempfit*m+b

    fig, ax = pl.subplots()

    ax.plot(holdtemps, vols, marker='.', linestyle='none', label='data')
    ax.plot(tempfit, volfit, label='Linear fit (r='+str(r)+')')

    ax.grid()
    ax.legend()

    ax.set_ylabel(r'Volume ['+units_metal['Volume']+']')
    ax.set_xlabel(r'Temperature ['+units_metal['Temperature']+']')

    fig.tight_layout()
    pl.savefig(os.path.join(plotdir, 'volume_temperature_fit'))
    pl.close('all')

    newcount += 1
