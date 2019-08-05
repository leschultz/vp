'''
Store generic fuctions.
'''

from shutil import copyfile
from os.path import join

import pandas as pd
import numpy as np
import os


def finder(name, source):
    '''
    Find the diretories with a file.

    inputs:
        name = The generic name for files to be copied
        source = The parent directory of all files
    outputs:
        paths = The matching paths
    '''

    # Count all mathching paths
    paths = []
    for item in os.walk(source):

        if name not in item[2]:
            continue

        paths.append(os.path.abspath(item[0]))

    return paths


def copier(source, name, destination):
    '''
    Search for all possible files to copy.

    inputs:
        source = The parent directory of all files
        name = The generic name for files to be copied
        destination = Path to save copy of files

    outputs:
        A collection of data files
    '''

    # Get absolute paths
    source = os.path.abspath(source)
    destination = os.path.abspath(destination)

    # Gather common ancestor
    ancestor = os.path.commonprefix([source, destination])

    # Count all mathching paths
    paths = finder(name, source)
    count = str(len(paths))

    # Copy files
    newcount = 1
    for path in paths:

        print('Copying '+'('+str(newcount)+'/'+count+'): '+path)

        dump = join(destination, path.replace(ancestor, ''))
        if not os.path.exists(dump):
            os.makedirs(dump)

        copyfile(join(path, name), join(dump, name))

        newcount += 1
