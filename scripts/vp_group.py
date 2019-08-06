import pandas as pd
import argparse

import os

parser = argparse.ArgumentParser(
                                 description='Arguments for ICO analysis'
                                 )

parser.add_argument(
                    '-s',
                    action='store',
                    type=str,
                    help='the file with fraction data'
                    )

parser.add_argument(
                    '-n',
                    action='store',
                    type=str,
                    help='name of save file with the path'
                    )

args = parser.parse_args()

# Create a folder for analysis data
datadir = os.path.join(*args.n.split('/')[:-1])
if not os.path.exists(datadir):
    os.makedirs(datadir)

df = pd.read_csv(args.s)

# Remove last directory to group for run set
df['run'] = df['run'].apply(lambda x: os.path.join(*x.split('/')[:-1]))

groupcols = ['run', 'temperature', 'atoms']
groups = df.groupby(groupcols)

# Compute population statistics
mean = groups.mean().add_suffix('_mean').reset_index()
std = groups.std().add_suffix('_std').reset_index()
sem = groups.sem().add_suffix('_sem').reset_index()
count = groups.count().add_suffix('_count').reset_index()

# Merge datafframes
df = mean.merge(std)
df = df.merge(sem)
df = df.merge(count)

# Compute percent errors
df['fraction_std_percent'] = df['fraction_std']/df['fraction_mean']*100
df['fraction_sem_percent'] = df['fraction_sem']/df['fraction_mean']*100

df.to_csv(
          args.n,
          index=False
          )
