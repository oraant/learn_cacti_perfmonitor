#!/usr/bin/python
#-*- coding:utf-8 -*-

import paramiko
import dbm
import widget as w

hostname = '192.168.20.151'
username = 'root'
password = 'rootroot'

local_data = w.getDbm('getlinux')

def connect(host,user,passwd):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(host,username = user,password = passwd)
	return ssh

def command(session,cmd):
	stdin,stdout,stderr = session.exec_command(cmd)
	out = stdout.readlines()
	err = stderr.readlines()
	if len(err) == 0:
		return out
	else:
		return err

def output(list):
	print len(list)
	for i in list:
		print i.strip('\n')

def cpuinfo():
	def total():
		#get total_now
		cmd = "cat /proc/stat|grep 'cpu '|awk '{print $2,$3,$4,$5,$6,$7,$8,$9}'"
		datas = command(s,cmd)[0].strip('\n').split()
		total_now = 0
		for i in datas:
			total_now += int(i)
	
		#get total_last
		key_string = hostname + 'cpu_total'
		total_last = int(w.getValue(local_data,key_string,'0'))
		local_data[key_string] = str(total_now)
	
		#get diff value
		total_diff = 0
		if total_last == 0:
			total_diff = 0
		else:
			total_diff = total_now - total_last
	
		return total_diff

	def idle():
		#get idle_now
		cmd = "cat /proc/stat |grep 'cpu '|awk '{print $5}'"
		data = command(s,cmd)[0].strip('\n')
		idle_now = int(data)

		#get idle_last
		key_string = hostname + 'cpu_idle'
		idle_last = int(w.getValue(local_data,key_string,'0'))local_data[key_string] = str(total_now)

s = connect(hostname,username,password)
print cpuinfo()
s.close()
