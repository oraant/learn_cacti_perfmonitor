#!/usr/bin/python
#-*- coding:utf-8 -*-

import inc
import time
import cx_Oracle

sql = 'select * from dual where 2=1'
link = 'system/oracle@192.168.56.60:1521/db11g'

db = cx_Oracle.connect(link)
cursor = db.cursor()
cursor.execute(sql)
r = cursor.fetchall()

print 'r ='
print r
print type(r)
print len(r)

for i in r:
	print 'i ='
	print i
	print type(i)
