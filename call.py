#!/usr/bin/python
#-*- coding:utf-8 -*-

import widget as w
import logging
import dbm
import ConfigParser
import cx_Oracle
import time
import sendmail

s = 'asdfsadfsadfasdlfkjasl;dfkjaskdfjhasldkfjhaslkdfjhasldkfjasldfkjsa ads ;lkf ja阿萨来啃静安寺扥灵撒旦法；阿萨来啃囧啊扥'
sendmail.send(s)

exit(0)

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
