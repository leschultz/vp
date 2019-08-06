'''
Functions for Voronoi polyhedra (VP) analysis
'''

from PyQt5 import QtGui  # Added to be able to import ovito

from ovito.modifiers import VoronoiAnalysisModifier
from ovito.io import import_file

from shutil import copyfile
from os.path import join

from vp_run_functions import system_parse, input_parse
from functions import finder

import pandas as pd
import numpy as np


def vp(traj, frames, edges, faces, threshold):
    '''
    Count the fraction of Voronoi polyhedra (VP) meeting criteria.

    inputs:
        traj = The trajectory files
        frames = A list of frames to analyize
        edges = The VP edge considered
        faces = The minimum number of faces for considered edge
        threshold = The minimum length for VP edge

    outputs:
        fraction = The fraction of VP meeting criteria
    '''

    # Indexing correction
    edges -= 1

    # Load input data and create an ObjectNode with a data pipeline.
    node = import_file(traj, multiple_frames=True)

    voro = VoronoiAnalysisModifier(
                                   compute_indices=True,
                                   use_radii=False,
                                   edge_threshold=threshold
                                   )

    node.modifiers.append(voro)

    all_indexes = []
    for frame in frames:
        out = node.compute(frame)
        indexes = out.particle_properties['Voronoi Index'].array
        all_indexes.append(indexes)

    # Combine all the frames
    all_indexes = [pd.DataFrame(i) for i in all_indexes]
    df = pd.concat(all_indexes)
    df = df.fillna(0)  # Make sure indexes are zero if not included
    df = df.astype(int)  # Make sure all counts are integers

    total = df.shape[0]  # The total number of VP
    count = df[df[edges] >= faces].shape[0]  # Counts matching of matching VP
    fraction = count/total  # The fraction of matching VP

    return fraction


def vp_iterator(inputname, trajname, sysname, data, parent, *args, **kwaargs):
    '''
    Conduct Voronoi polyhedra (VP) analysis for all matching files.

    inputs:
        inputname = The input file name
        trajname = The trajectory file name
        sysname = The thermodynamic data file name
        data = The location to the parent directory of all data
        parent = The top directory name of the parent directory
    outputs:
    '''

    # Count all mathching paths
    paths = finder(trajname, data)
    count = str(len(paths))

    newcount = 1
    df = []
    for path in paths:

        inp = join(path, inputname)
        traj = join(path, trajname)
        sys = join(path, sysname)

        print('Voronoi polyhedra '+'('+str(newcount)+'/'+count+'): '+path)

        param = input_parse(inp)  # Input parameters

        # Thermodynamic data
        cols, thermo = system_parse(sys)
        thermo = pd.DataFrame(thermo, columns=cols)
        thermo['Time'] = thermo['TimeStep']*param['timestep']
        thermo['frames'] = thermo.index+1  # The simulation frames

        prev = 0
        fractions = []
        for step in np.cumsum(param['holdsteps']):
            cond = (thermo['TimeStep'] >= prev) & (thermo['TimeStep'] <= step)
            d = thermo[cond]
            fractions.append(vp(traj, d['frames'].values, **kwaargs))

            prev = step

        fractions = pd.DataFrame({
                                  'temperature': param['temperatures'],
                                  'fraction': fractions
                                  })

        fractions['run'] = path.split(parent)[-1]  # The name of run

        df.append(fractions)

        newcount += 1

    df = pd.concat(df)

    return df
