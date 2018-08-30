#!/usr/bin/env python

"""

dd 

:Reference: https://www.cyberciti.biz/faq/howto-linux-unix-test-disk-performance-with-dd-command/

"""

import sys
import time
import subprocess
import sqlite3 

class Tester:
	def __init__(self):
		conn = sqlite3.connect("io.db")
		cur = conn.cursor()
		cur.execute('create table if not exists write (time datetime, speed float, latency float)')
		cur.execute('create table if not exists read (time datetime, speed float, latency float)')
		conn.commit()
		conn.close()

		# create a big file for read test 
		cmd = 'dd if=/dev/zero of=./test_read bs=10M count=2000 oflag=dsync'
		p = subprocess.Popen(cmd,
							 shell=True)
		p.communicate()
		
	def test(self, flag):
		while True:
			self.single_run(flag)

	def single_run(self, flag):
		speed = 0
		latency = 0
		# write 
		cmd = 'dd if=/dev/zero of=./test bs=1G count=1 oflag=dsync'
		p = subprocess.Popen(cmd,
							 shell=True,
							 stdout=subprocess.PIPE,
							 stderr=subprocess.PIPE)
		so, se = p.communicate()
		for l in se.split('\n'):
			if 'copied' in l:
				s = l.split()
				now = time.strftime('%Y-%m-%d %H:%M:%S')
				speed = s[-2]
				
		# latency 
		cmd = 'dd if=/dev/zero of=./test bs=512 count=1000 oflag=dsync'
		p = subprocess.Popen(cmd,
							 shell=True,
							 stdout=subprocess.PIPE,
							 stderr=subprocess.PIPE)
		so, se = p.communicate()
		for l in se.split('\n'):
			if 'copied' in l:
				s = l.split()
				now = time.strftime('%Y-%m-%d %H:%M:%S')
				latency = s[-4]

		conn = sqlite3.connect("io.db")
		now = time.strftime('%Y-%m-%d %H:%M:%S')
		cur = conn.cursor()
		cur.execute('insert into write values ("%s", %s, %s)'%(now, speed, latency))
		conn.commit()
		conn.close()

		# read test
		if flag:
			cmd = 'echo 3 | tee /proc/sys/vm/drop_caches; dd if=./test_read of=/dev/null bs=8k'
		else:
			cmd = 'dd if=./test_read of=/dev/null bs=8k'
			
		now = time.strftime('%Y-%m-%d %H:%M:%S')
		speed = 0
		read_time = 0
		p = subprocess.Popen(cmd,
							 shell=True,
							 stdout=subprocess.PIPE,
							 stderr=subprocess.PIPE)
		so, se = p.communicate()
		for l in se.split('\n'):
			if 'copied' in l:
				s = l.split()
				speed = s[-2]
				
			s = l.split()
				
			if len(s) == 2:
				if s[0] == 'real':
					read_time = float(s[1])
					
		conn = sqlite3.connect("io.db")
		now = time.strftime('%Y-%m-%d %H:%M:%S')
		cur = conn.cursor()
		cur.execute('insert into read values ("%s", %s, %s)'%(now, speed, read_time))
		conn.commit()
		conn.close()

		time.sleep(10)

if __name__ == '__main__':
	t = Tester()
	if len(sys.argv)>=2 and sys.argv[1] == 'superuser':
		print 'superuser mode'
		t.test(True)
	else:
		print sys.argv
		t.test(False)
