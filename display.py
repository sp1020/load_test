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
ax.set_ylabel('spent time for calculation')
fig.tight_layout()
fig.savefig('cpu.png')

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
	ax.set_ylabel('ping latency (ms)')
fig.tight_layout()
fig.savefig('network.png')

### IO ###
conn = sqlite3.connect('io.db')
read = pd.read_sql_query('select * from read', conn)
write = pd.read_sql_query('select * from write', conn)
conn.close()

fig = pylab.figure(figsize=(15, 10))
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)

ts = read.loc[:, 'time']
sp = read.loc[:, 'speed']
lt = read.loc[:, 'latency']

ax1.plot(ts, sp)
ax1.set_ylabel('read rate')
ax1_2 = ax1.twinx()
ax1_2.plot(ts, lt, c='gray')
ax1_2.set_ylabel('time spent')

ts = write.loc[:, 'time']
sp = write.loc[:, 'speed']
lt = write.loc[:, 'latency']

ax2.plot(ts, sp)
ax2.set_ylabel('write rate')
ax2_2 = ax2.twinx()
ax2_2.plot(ts, lt, c='gray')
ax2_2.set_ylabel('time spent')
fig.tight_layout()
fig.savefig('io.png')

pylab.show()
