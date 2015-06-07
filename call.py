#!/usr/bin/python
#-*- coding:utf-8 -*-

import widget as w
import logging
import dbm
import ConfigParser
import cx_Oracle
import time

old = time.time()
if w.verifyEnable('datamanager') != True:
	print 'model can\'t run'
	exit(1)

conf,data,logger = w.getFiles('getOracle')
result = w.advancedNode('getOracle',conf,'xuniji')

if result[0] == True:
	db = result[1]
else:
	print result[1]
	exit()

cursor = db.cursor()
cursor.execute('select sysdate from v$database')
print cursor.fetchall()
now = time.time()
print now - old
