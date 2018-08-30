#!/usr/bin/env python
import pylab
import sqlite3
import pandas as pd

### CPU ###
conn = sqlite3.connect('cpu.db')

df = pd.read_sql_query('select * from cpu', conn)
conn.close()

fig = pylab.figure(figsize=(15, 10))
ax = fig.add_subplot(111)
ax.plot(df.loc[:, 'time'], df.loc[:, 'real'])
ax.plot(df.loc[:, 'time'], df.loc[:, 'user'])

### Network ###
conn = sqlite3.connect('network.db')
df = pd.read_sql_query('select * from ping', conn)
conn.close()

fig = pylab.figure(figsize=(15, 10))
targets = ['google', 'meta1']
for i, e in enumerate(targets):
	df2 = df[df['target']==e]
	ts = df2.loc[:, 'time']
	v1 = df2.loc[:, 'min']
	v2 = df2.loc[:, 'avg']
	v3 = df2.loc[:, 'max']

	ax = fig.add_subplot(len(targets), 1, i+1)
	ax.plot(ts, v1)
	ax.plot(ts, v2)
	ax.plot(ts, v3)

pylab.show()
