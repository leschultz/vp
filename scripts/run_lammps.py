'''
Use the installed version of lammps to run multiple simulations.
'''

from functions import finder

import subprocess
import sys
import os

runpath = sys.argv[1]  # The path for all runs to be executed
program = sys.argv[2]  # The lammps binary
runname = sys.argv[3]  # The standard lammps input file name

# Count all mathching paths
runs = finder(runname, runpath)
count = len(runs)

countnew = 1
for path in runs:

    print('Running ('+str(countnew)+'/'+str(count)+'): '+path)

    subprocess.run(
                   program.split(' ')+['-in', runname],
                   cwd=path,
                   stdout=open(os.devnull, 'wb')
                   )

    countnew += 1
