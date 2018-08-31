#!/usr/bin/env python

"""
ping test 
"""
import time
import subprocess
import sqlite3 

address={'google': 'www.google.com',
		 'meta1': 'meta1'
		 }


class NetworkMonitor:
	def __init__(self):
		conn = sqlite3.connect("network.db")
		cur = conn.cursor()
		cur.execute('create table if not exists ping (time datetime, target varchar(255), min float, avg float, max float, mdev float, loss float)')
		conn.commit()
		conn.close()

	def test(self):
		while True:
			self.single_run()

	def single_run(self):
		for ad in address:
			cmd = ['ping', address[ad], '-c', '50']
			p = subprocess.Popen(cmd,
								 stdout=subprocess.PIPE,
								 stderr=subprocess.PIPE)

			min = 0
			avg = 0
			max = 0
			mdev = 0
			loss = 0
			so, se = p.communicate()
			for l in so.split('\n'):
				if 'min/avg/max/mdev' in l:
					s = l.split()
					(min, avg, max, mdev) = s[3].split('/')
				if 'packet loss' in l:
					s = l.split()
					loss = float(s[5][:-1])

			conn = sqlite3.connect("network.db")
			now = time.strftime('%Y-%m-%d %H:%M:%S')
			cur = conn.cursor()
			cur.execute('insert into ping values ("%s", "%s", %s, %s, %s, %s, %s)'%(now, ad, min, avg, max, mdev, loss))
			conn.commit()
			conn.close()

if __name__ == '__main__':
	nm = NetworkMonitor()
	nm.test()


	

