#!/usr/bin/python

import cx_Oracle

db = cx_Oracle.connect('u1/u1@192.168.56.60:1521/db11g')

def getdb():
	return db

def getdata(database):
	cursor = database.cursor()
	cursor.execute('select * from u1.test1')
	for i in cursor.fetchall():
		print i

def choose(i):
	if i == 'db':
		return db
	elif i == 'str':
		return 'hello'
	elif i == 'bool':
		return True

def getreturn():
	return 23,''
