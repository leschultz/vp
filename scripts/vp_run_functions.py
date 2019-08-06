from ast import literal_eval
import numpy as np
import random


def run_creator(
                template_contents,
                elements,
                traj,
                potential,
                potential_type,
                timestep,
                dump_rate,
                ensemble,
                vols,
                holds
                ):
    '''
    Generate a LAMMPS input file
    '''

    # Random number used by LAMMPS
    seed = random.randint(0, 9999999)

    # Replace keywords within a template document
    contents = template_contents
    contents = contents.replace('#replace_elements#', elements)
    contents = contents.replace('#replace_initial_trajectories#', traj)
    contents = contents.replace('#replace_potential#', potential)
    contents = contents.replace('#replace_potential_type#', potential_type)
    contents = contents.replace('#replace_timestep#', timestep)
    contents = contents.replace('#replace_dumprate#', dump_rate)

    # Randomize initial velocites
    steps = (
             'velocity all create ' +
             str(holds[0][0]) +
             ' ${seed} rot yes dist gaussian' +
             2*'\n'
             )

    # Create a step for every temperature and hold defined
    if ensemble == 'npt':
        for temp, step in holds:
            temp = str(temp)
            step = str(step)

            steps += (
                      'fix step all npt temp ' +
                      temp +
                      ' ' +
                      temp +
                      ' '
                      '0.1 ' +
                      'iso 0 0 1\n' +
                      'run ' +
                      step +
                      '\n' +
                      'unfix step\n'
                      )

    if ensemble == 'nvt':
        for hold, vol in zip(holds, vols):
            temp = str(hold[0])
            step = str(hold[1])
            side_l = str(vol**(1/3))

            steps += 'change_box all'
            steps += ' x final 0.0 '+side_l
            steps += ' y final 0.0 '+side_l
            steps += ' z final 0.0 '+side_l
            steps += ' units box'
            steps += '\n'

            steps += (
                      'fix step all nvt temp ' +
                      temp +
                      ' ' +
                      temp +
                      ' '
                      '0.1\n' +
                      'run ' +
                      step +
                      '\n' +
                      'unfix step\n'
                      )

    contents = contents.replace('#replace_holds#', steps)
    contents = contents.replace('#replace_seed#', str(seed))

    return contents


def input_parse(infile):
    '''
    Parse the input file for important parameters

    inputs:
        infile = The name and path of the input file
    outputs:
        param = Dictionary containing run paramters
    '''

    holdsteps = []
    temperatures = []
    with open(infile) as f:
        for line in f:

            line = line.strip().split(' ')

            if 'units' in line:
                units = line[-1]

            if 'run' == line[0]:
                holdsteps.append(int(line[-1]))

            if 'mydumprate' in line:
                line = [i for i in line if i != '']
                dumprate = int(line[-1])

            if 'pair_coeff' in line:
                line = [i for i in line if i != '']
                elements = line[4:]

            if 'mytimestep' in line:
                timestep = float(line[-1])

            if ('temp' in line) and ('fix' in line):
                line = [i for i in line if i != '']
                temperatures.append(float(line[5]))

    param = {
             'units': units,
             'holdsteps': holdsteps,
             'dumprate': dumprate,
             'elements': elements,
             'timestep': timestep,
             'temperatures': temperatures,
             }

    return param


def system_parse(sysfile):
    '''
    Parse the thermodynamic data file

    inputs:
        sysfile = The name and path of the thermodynamic data file
    outputs:
        columns = The columns for the data
        data = The data from the file
    '''

    data = []
    with open(sysfile) as f:
        line = next(f)
        for line in f:

            if '#' in line:
                values = line.strip().split(' ')
                columns = values[1:]
                columns = list(map(lambda x: x.split('_')[-1], columns))

            else:
                values = line.strip().split(' ')
                values = list(map(literal_eval, values))
                data.append(values)

    return columns, data


def units(style):
    '''
    Define the units by the style used in LAMMPS.

    inputs:
        style = The units style used in LAMMMPS
    outputs:
        x = A dictionary containing the units.
    '''

    if style == 'metal':
        x = {
             'Volume': r'$\AA^{3}$',
             'Time': r'$ps$',
             'PE': r'$eV$',
             'KE': r'$eV$',
             'Temperature': r'$K$',
             'Pressure': r'$bars$',
             }

    return x
