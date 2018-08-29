#!/usr/bin/env python

import numpy as np
import subprocess

if __name__ == '__main__':
	for i in range(100):
		p = subprocess.Popen('time ./count.py',
							 stdout=subprocess.PIPE,
							 shell=True)
		so, se = p.communicate()

		print so
	
