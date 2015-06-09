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


dmHandler.begin(cursor)
print 'begin'

capture_counter = 0
calculate_counter = 0
for node in conf.sections():
	#connect with node
	result = w.advancedNode('getOracle',conf,node)
	print ' ====== node is ' + node + ' ====== '
	if result[0] == True:
		node_db = result[1]
		node_cursor = node_db.cursor()
	else:
		dmHandler.delNode(cursor,node)
		print result[1]
		print 'delete datas from rawdata_last table.'
		continue


	#get raw data
	dmCapture.main(node_cursor,cursor,node)
	capture_counter += 1
	node_cursor.close()
	node_db.close()
	print 'capture done'


	#calculate
	sql_verify = "select count(1) from rawdata_10min_last where target_name = '" + node + "'"
	cursor.execute(sql_verify)
	rows = cursor.fetchone()[0]
	if rows == 0:
		print 'no data found in rawdata_10min_last with this node.'
		continue
	else:
		param_table = w.decrypt(conf.get(node,'param_table'))
		dmHandler.calculate(cursor,node,param_table)
		calculate_counter += 1

		#dbg
		sql_verify = "select count(1) from calvalue_10min where target_name = '" + node + "'"
		cursor.execute(sql_verify)
		rows = cursor.fetchone()[0]
		print 'calculate done,rows in calvalue table with this node is ' + str(rows)


	#to file
	pathname = w.decrypt(conf.get(node,'pathname')).upper()
	filename = w.decrypt(conf.get(node,'filename'))
	param_table = w.decrypt(conf.get(node,'param_table'))
	name = node
	tofile_sql = "select to_file('" + name + "','" + param_table + "','" + pathname + "','" + filename + "') from dual"
	cursor.execute(tofile_sql)
	if cursor.fetchone()[0].upper() != 'TRUE':
		print 'failed when write calculate values to files with ' + node
		continue


	#maintain alert table
	sql_verify = "select count(1) from alert_10min where target_name = '" + node + "'"
	cursor.execute(sql_verify)
	rows = cursor.fetchone()[0]
	if rows == 0:
		print 'need to add node to alert table'
		dmAlert.addNode(cursor,node,param_table)


print ' ====== end of loop ======'

#verify if captured or calculated
if capture_counter == 0:
	print 'capture counter = 0,exit.'
	cursor.close()
	server.close()
	exit()

if calculate_counter == 0:
	print 'calculate counter = 0,end and exit.'
	dmHandler.end(cursor)
	cursor.close()
	server.close()
	exit()
	

#get alert report
dmAlert.getDynamic(cursor)
print 'dbg - got Dynamic'
datas = dmAlert.getAlert(cursor)


#format alert report
if len(datas) != 0:
	mail_text = '中研软Perfmonitor性能预警平台发来报告：\n'
	sms_text = 'Perfmonitor阈值告警功能：\\n'
	for data in datas:
		mail_text += '节点：%-20s参数：%-50s当前的值：%-15.2f告警值：%-15.2f\n'%(data[0],data[1],data[2],data[3])
	
	sms_text += '本次检测，发现共' + str(len(datas)) + '个参数超过警戒值。\\n详细内容已发送至您的邮箱。'
	print mail_text
	print sms_text
else:
	print 'no Alert.'


dmHandler.end(cursor)
cursor.close()
server.close()
exit()
