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
                    help='name of save file wiht path'
                    )

args = parser.parse_args()

df = pd.read_csv(args.s)

groups = df.groupby(['run', 'temperature'])

mean = groups.mean().add_suffix('_mean').reset_index()
std = groups.std().add_suffix('_std').reset_index()
sem = groups.sem().add_suffix('_sem').reset_index()
count = groups.count().add_suffix('_count').reset_index()

df = mean.merge(std)
df = df.merge(sem)
df = df.merge(count)

df.to_csv(
          args.n,
          index=False
          )

print(df)
