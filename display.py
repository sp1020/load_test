#!/usr/bin/env python
import pylab
import sqlite3
import pandas as pd

### CPU ###
conn = sqlite3.connect('cpu.db')

df = pd.read_sql_query('select * from cpu', conn)
conn.close()

print df

fig = pylab.figure(figsize=(15, 10))
ax = fig.add_subplot(111)
ax.grid()
ax.plot(df.loc[:, 'time'], df.loc[:, 'real'])
ax.plot(df.loc[:, 'time'], df.loc[:, 'user'])

pylab.show()
