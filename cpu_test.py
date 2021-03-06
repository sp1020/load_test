#!/usr/bin/env python

import numpy as np
import subprocess
import sqlite3 
import time

class TestSingle:
	def __init__(self):
		conn = sqlite3.connect("cpu.db")
		cur = conn.cursor()
		cur.execute('create table if not exists cpu (time datetime, real float, user float, sys float)')
		conn.commit()
		conn.close()

	def test(self):
		while True:
			self.single_run()

	def single_run(self):
		p = subprocess.Popen('time -p ./count.py',
							 stdout=subprocess.PIPE,
							 stderr=subprocess.PIPE,
							 shell=True)
		so, se = p.communicate()

		real = 0 
		user = 0
		sys = 0
		for l in se.split('\n'):
			s = l.split()
			if len(s) == 2:
				if s[0] == 'real':
					real = float(s[1])
				elif s[0] == 'user':
					user = float(s[1])
				elif s[0] == 'sys':
					sys = float(s[1])

		conn = sqlite3.connect("cpu.db")
		now = time.strftime('%Y-%m-%d %H:%M:%S')
		cur = conn.cursor()
		cur.execute('insert into cpu values ("%s", %s, %s, %s)'%(now, real, user, sys))
		conn.commit()
		conn.close()

if __name__ == '__main__':
	ts = TestSingle()
	ts.test()
