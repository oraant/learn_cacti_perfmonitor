#!/usr/bin/python
#-*- coding:utf-8 -*-

import widget as w
import logging
import dbm
import ConfigParser
import cx_Oracle
import time
import sendmail
import dmHandler
import dmAlert
import dmCapture

if w.verifyEnable('datamanager') != True:
	print 'model can\'t run'
	exit(1)

conf,local_data,logger = w.getFiles('getOracle')

try:
	server = w.getServer()
	cursor = server.cursor()

except:
	print "can't connect with server"
	exit(1)


mail_text = ''
sms_text = ''

for node in conf.sections():
	result = w.advancedNode('getOracle',conf,node)
	print 'node is ' + node
	if result[0] == True:
		node_db = result[1]
		node_cursor = node_db.cursor()
	else:
		print result[1]
		continue


	dmCapture.main(node_cursor,cursor,node)
	node_cursor.close()
	node_db.close()


	sql_verify = "select count(1) from rawdata_10min_last where target_name = '" + node + "'"
	cursor.execute(sql_verify)
	if cursor.fetchone()[0] == 0:
		continue
	else:
		param_table = w.decrypt(conf.get(node,'param_table'))
		dmHandler.calculate(cursor,node,param_table)


	pathname = w.decrypt(conf.get(node,'pathname')).upper()
	filename = w.decrypt(conf.get(node,'filename'))
	param_table = w.decrypt(conf.get(node,'param_table'))
	name = node
	tofile_sql = "select to_file('" + name + "','" + param_table + "','" + pathname + "','" + filename + "') from dual"
	#cursor.execute(tofile_sql)
	#if cursor.fetchone()[0].upper() != 'TRUE':
	#	 print 'failed when write calculate values to files'
	#	 exit(4)


	sql_verify = "select count(1) from alert_10min where target_name = '" + node + "'"
	cursor.execute(sql_verify)
	if cursor.fetchone()[0] == 0:
		print 'need to add node to alert table'
		dmAlert.addNode(cursor,node)
	dmAlert.getDynamic(cursor)
	datas = dmAlert.getAlert(cursor)
	mail_text += str(datas)

dmHandler.finish(cursor)

cursor.close()
server.close()

mail_text = datas
sms_text = ''
print mail_text
