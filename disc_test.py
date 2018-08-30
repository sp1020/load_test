#!/usr/bin/env python

"""

dd 

:Reference: https://www.cyberciti.biz/faq/howto-linux-unix-test-disk-performance-with-dd-command/

"""
import time
import subprocess
import sqlite3 

class Tester:
	def __init__(self):
		conn = sqlite3.connect("io.db")
		cur = conn.cursor()
		cur.execute('create table if not exists write (time datetime, speed float, latency float)')
		cur.execute('create table if not exists write (time datetime, speed float)')
		conn.commit()
		conn.close()

	def test(self):
		while True:
			self.single_run()

	def single_run(self):
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

		time.sleep(10)

if __name__ == '__main__':
	t = Tester()
	t.test()
