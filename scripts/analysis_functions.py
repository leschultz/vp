'''
Functions for Voronoi polyhedra (VP) analysis
'''

from PyQt5 import QtGui  # Added to be able to import ovito

from ovito.modifiers import VoronoiAnalysisModifier
from ovito.io import import_file

from shutil import copyfile
from os.path import join

import pandas as pd
import numpy as np


def vp(traj, edges, faces, threshold):
    '''
    Count the fraction of Voronoi polyhedra (VP) meeting criteria.

    inputs:
        traj = The trajectory files
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
    for frame in range(node.source.num_frames+1):
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


def vp_iterator(name, data, *args, **kwaargs):
    '''
    Conduct Voronoi polyhedra (VP) analysis for all matching files.

    inputs:
        name = The trajectory file name
        data = The parent directory of all data
    outputs:
    '''

    # Count all mathching paths
    paths = finder(name, data)
    count = str(len(paths))

    newcount = 1
    df = []
    for path in paths:

        run = join(path, name)
        print('Voronoi polyhedra '+'('+str(newcount)+'/'+count+'): '+run)

        fraction = vp(run, **kwaargs)
        df.append(fraction)

        newcount += 1

    df = {'run': paths, 'fraction': df}
    df = pd.DataFrame(df)

    return df
