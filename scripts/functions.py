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
