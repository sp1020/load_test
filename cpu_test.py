#!/usr/bin/env python

import numpy as np

cnt = 0
while True:
	cnt += 1
	if cnt < 0:
		cnt = 1
	if cnt % 1000000 == 0:
		print np.log(cnt)

