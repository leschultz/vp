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
                    '-p',
                    action='store',
                    type=str,
                    help='parent directory name'
                    )

parser.add_argument(
                    '-e',
                    action='store',
                    type=str,
                    help='name of output file extension'
                    )

args = parser.parse_args()

df = pd.read_csv(args.s)

temp = int(args.s.split('.')[-2].split('_')[0])

# Filter the data by temperatures and composition
df['run'] = df['run'].apply(lambda x: x.split(args.p)[-1].split('/')[1])

groups = df.groupby(['run'])

mean = groups.mean().add_suffix('_mean').reset_index()
std = groups.std().add_suffix('_std').reset_index()
sem = groups.sem().add_suffix('_sem').reset_index()
count = groups.count().add_suffix('_count').reset_index()

df = mean.merge(std)
df = df.merge(sem)
df = df.merge(count)
df['temp'] = temp

df.to_csv(
          args.s.split('.txt')[0]+args.e,
          index=False
          )

print(df)
