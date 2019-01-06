import pybaseball
df = pybaseball.batting_stats_bref(2009)
import os
print(os.getcwd())
data_dir = 'data'

fname = '2018_stats.csv'
data_path = data_dir + '/' + fname
print(data_path)
df.to_csv(data_path, index=False)

df3
