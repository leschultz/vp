from ast import literal_eval

import numpy as np
import sys
import os

from vp_run_functions import run_creator

save = sys.argv[1]  # The location and name for the set of runs
runs = int(sys.argv[2])  # The number of runs to generate
template = sys.argv[3]  # Template file path
elements = sys.argv[4]  # Elements
traj = sys.argv[5]  # Initial trajectories
potential = sys.argv[6]  # The potential used
potential_type = sys.argv[7]  # The type of potential
timestep = sys.argv[8]  # The timestep
dump_rate = sys.argv[9]  # The rate to dump data
ensemble = sys.argv[10]  # The ensemble for the holds
vols = sys.argv[11]  # The volume for nvt holds (write None for npt)
holds = sys.argv[12]  # temperature and holds as tuples

# Open and read template
template = open(template)
template_contents = template.read()
template.close()

# Format the holds
holds = literal_eval(holds)

# Format the volumes
try:
    vols = literal_eval(vols)

except Exception:
    pass

runs = np.arange(runs)
runs = ['run_'+str(i) for i in runs]

# Directories back to main working directory
back = (len(os.path.split(save)[0].split('/'))-1)*'../'

for run in runs:

    contents = run_creator(
                           template_contents,
                           elements,
                           os.path.join(back, traj),
                           os.path.join(back, potential),
                           potential_type,
                           timestep,
                           dump_rate,
                           ensemble,
                           vols,
                           holds,
                           )

    # Write the input file
    path = os.path.join(save, run)

    if not os.path.exists(path):
        os.makedirs(path)

    file_out = open(os.path.join(path, 'vp_steps.in'), 'w')
    file_out.write(contents)
    file_out.close()
