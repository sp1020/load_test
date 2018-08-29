#!/usr/bin/env python

import numpy as np
import subprocess
import pylab 

class TestSingle:
	def __init__(self):
		self.real = []
		self.user = []
		self.sys = []

	def test(self):
		# test 
		for i in range(10):
			self.single_run()

		# report
		print np.average(self.real)
		print np.average(self.user)
		print np.average(self.sys)

	def single_run(self):
		p = subprocess.Popen('time -p ./count.py',
							 stdout=subprocess.PIPE,
							 stderr=subprocess.PIPE,
							 shell=True)
		so, se = p.communicate()
		for l in se.split('\n'):
			s = l.split()
			if len(s) == 2:
				if s[0] == 'real':
					self.real.append(float(s[1]))
				elif s[0] == 'user':
					self.user.append(float(s[1]))
				elif s[0] == 'sys':
					self.sys.append(float(s[1]))
		

if __name__ == '__main__':
	ts = TestSingle()
	ts.test()
