#!/usr/bin/python
#-*- coding:utf-8 -*-

import widget as w
import logging
import dbm
import ConfigParser
import cx_Oracle
import time
import sendmail
import sendsms
import dmHandler
import dmAlert
import dmCapture
import commands

#get basic info : enable or not, configure file, dbm file, logger, and connection with server.
if w.verifyEnable('datamanager') != True:
	exit(1)

conf,data,logger = w.getFiles('getOracle')
logger.debug(" ====== Model start. ====== ")

try:
	server = w.getServer()
	cursor = server.cursor()
except:
	logger.critical("Can't connect with server")
	data.close()
	exit(1)


#manage datas in tables at the begin.
dmHandler.begin(cursor)
logger.debug("Program Startup with dmHandler.begin()")


#loop for all nodes
capture_counter = 0
calculate_counter = 0
for node in conf.sections():

	#connect with node
	logger.debug(" ------ Enter into loop,node is " + node + " ------ ")
	result = w.advancedNode('getOracle',node,conf,data)
	if result[0] == True:
		node_db = result[1]
		node_cursor = node_db.cursor()
		logger.debug("Got connection and cursor from " + node)
	else:
		dmHandler.delNode(cursor,node)
		logger.warning("Connect failed with " + node + ", deleted datas from rawdata_last table.\n\tReason is : " + result[1])
		continue


	#capture raw data
	dmCapture.main(node_cursor,cursor,node)
	capture_counter += 1
	node_cursor.close()
	node_db.close()

	#dbg for rows of capture
	sql_verify = "select count(1) from rawdata_10min where target_name = '" + node + "'"
	cursor.execute(sql_verify)
	rows = cursor.fetchone()[0]
	logger.debug("Captured " + str(rows) + " rows from " + node + ", close connetion and cursor.")

	#calculate
	sql_verify = "select count(1) from rawdata_10min_last where target_name = '" + node + "'"
	cursor.execute(sql_verify)
	rows = cursor.fetchone()[0]
	if rows == 0:
		logger.warning('no data found in rawdata_10min_last with ' + node + ', end this node.' )
		continue
	else:
		param_table = w.decrypt(conf.get(node,'param_table'))
		dmHandler.calculate(cursor,node,param_table)
		calculate_counter += 1

		#dbg for rows of calculate
		sql_verify = "select count(1) from calvalue_10min where target_name = '" + node + "'"
		cursor.execute(sql_verify)
		rows = cursor.fetchone()[0]
		logger.debug('calculate done,rows in calvalue table with this node is ' + str(rows))


	#output datas in calvalue table to output file of this node
	pathname = w.decrypt(conf.get(node,'pathname')).upper()
	filename = w.decrypt(conf.get(node,'filename'))
	param_table = w.decrypt(conf.get(node,'param_table'))
	name = node
	tofile_sql = "select to_file('" + name + "','" + param_table + "','" + pathname + "','" + filename + "') from dual"
	cursor.execute(tofile_sql)
	if cursor.fetchone()[0].upper() != 'TRUE':
		logger.error('failed when write calculate values to files with ' + node + ', end this node.' )
		continue
	logger.debug("output datas to " + pathname + "/" + filename + " successed.")


	#maintain alert table
	sql_verify = "select count(1) from alert_10min where target_name = '" + node + "'"
	cursor.execute(sql_verify)
	rows = cursor.fetchone()[0]
	if rows == 0:
		logger.debug("didn't found data in alert table, now add " + node + " in it.")
		dmAlert.addNode(cursor,node,param_table)



#loop end,verify if captured or calculated
logger.debug(' ------ Loop end.')
if capture_counter == 0:
	logger.debug("capture counter = 0, close connection and cursor with server, exit program.\n")
	cursor.close()
	server.close()
	data.close()
	exit(0)

if calculate_counter == 0:
	logger.debug("calculate counter = 0, archive datas with end function. Close connection and cursor with server, exit program.\n")
	dmHandler.end(cursor)
	cursor.close()
	server.close()
	data.close()
	exit(0)


#get alert report
scale = float(w.conf.get('getOracle','scale'))
dmAlert.getDynamic(cursor)
alerts = dmAlert.getAlert(cursor,scale)
logger.debug("Generate dynamic alert value, and get parameter values that bigger than alert value.")


mailsub = 'Oracle性能参数告警'
#format alert report
if len(alerts) != 0:
	logger.debug("Got alert,sending mail, sms and reports.")

	mailtext = '中研软Perfmonitor性能预警平台发来报告：\n'
	smstext = '数据库参数告警功能：\\n'
	for alert in alerts:
		mailtext += '节点：%-20s参数：%-50s当前的值：%-15.2f告警值：%-15.2f\n'%(alert[0],alert[1],alert[2],alert[3])
	
	smstext += '本次检测，发现共' + str(len(alerts)) + '个参数超过警戒值。\\n详细内容已发送至您的邮箱。'

	sendmail.send(mailsub,mailtext)
	sendsms.send(smstext)
	#print mailtext
	#print smstext


	targets = [alert[0] for alert in alerts]
	targets = list(set(targets))
	logger.debug('hosts need to generate reports is : ' + str(targets))
	for target in targets:
		tnsname = w.decrypt(conf.get(target,'tnsname'))
		pathname = w.decrypt(conf.get(target,'pathname'))
		version = pathname[-3:-1]
		inst_num = w.decrypt(conf.get(target,'instance_num'))
		base_line = 'perfbl'

		command = '/perfmonitor/reports/main.sh ' + tnsname + ' ' + version + ' ' + inst_num + ' ' + base_line
		(status,output) = commands.getstatusoutput(command)
		if status != 0:
			logger.error('can\'t send reports for ' + target + ', output is : ' + output)
		else:
			logger.debug('send reports for ' + target)

	logger.debug("Sending done.")
else:
	logger.debug("No Alert this time.")


#Program termination
logger.debug("Archive datas with end function. Close connection and cursor with server, exit program.\n")
dmHandler.end(cursor)
cursor.close()
server.close()
data.close()
exit(0)
