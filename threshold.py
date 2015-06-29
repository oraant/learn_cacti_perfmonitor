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

#get basic info : enable or not, configure file, dbm file, logger, and sql statements.
if w.verifyEnable('threshold') != True:
	exit(1)

conf,data,logger = w.getFiles('getThreshold')
logger.debug(" ====== Model start. ====== ")


sql_latest = 'select to_char(time_suggested,\'YYYY-MM-DD HH24:MI:SS.FF TZH:TZM\') from dba_outstanding_alerts'
sql_report = '''
select instance_number,
       sequence_id,
       message_level,
       reason,
       to_char(creation_time, 'YY/MM/DD HH24:MI:SS') first_create,
       to_char(time_suggested, 'YY/MM/DD HH24:MI:SS') last_update
  from dba_outstanding_alerts
 where time_suggested <=
       to_timestamp_tz(:this_latest, 'YYYY-MM-DD HH24:MI:SS.FF TZH:TZM')
   and time_suggested >
       to_timestamp_tz(:last_latest, 'YYYY-MM-DD HH24:MI:SS.FF TZH:TZM')
   and systimestamp - time_suggested < to_dsinterval('+0 0:5:0.0')
'''


#loop for all nodes
mailtext = '来自Perfmonitor阈值告警功能的报告：\n\n\n'
smstext = 'Perfmonitor阈值告警功能：\\n'
sms_db_count = 0
sms_rept_count = 0
for node in conf.sections():

	#connect with node
	logger.debug(" ------ Enter into loop,node is " + node + " ------ ")
	result = w.basicNode('getThreshold',node,conf,data)
	if result[0] == True:
		db = result[1]
		cursor = db.cursor()
		logger.debug("Got connection and cursor from " + node)
	else:
		logger.warning("Connect failed with " + node + ". \n\tReason is : " + result[1])
		continue
	
	
	#get latest update time in dba_outstanding_alerts
	cursor.execute(sql_latest)
	sql_result = cursor.fetchall()
	if len(sql_result) == 0:
		logger.debug("can't get latest update time in dba_outstanding_alerts with " + node + ". end this node.")
		continue
	else:
		this_latest = sql_result[0][0]
		logger.debug("the latest update time in dba_outstanding_alerts with " + node + " is : " + this_latest)


	#get last latest update time saved in dbm file
	key_string = node + 'last_latest'
	last_latest = w.getValue(data,key_string,'1000-01-01 01:01:01.000009 +08:00')
	logger.debug("the last latest update time in dbm file with " + node + " is : " + last_latest)
	data[key_string] = this_latest


	#get alerts from node which update time between last latest update time and latest update time,and appear in five minutes.
	cursor.execute(sql_report,this_latest = this_latest,last_latest = last_latest)
	alerts = cursor.fetchall()
	if len(alerts) == 0:
		logger.debug('did not get data from dba_outstanding_alerts table,end this node')
		continue


	#format datas got from dba_outstanding_alerts,and format it.
	logger.debug('got datas from dba_outstanding_alerts, now format it.')
	tnsname = w.decrypt(conf.get(node,'tnsname'))
	mailtext += '\n产生告警的库的连接是：' + tnsname + '\n'
	sms_db_count += 1
	for alert in alerts:
		mailtext += '报警的实例号：' + str(alert[0]) + '\n'
		mailtext += '报警的序号：' + str(alert[1]) + '\n'
		mailtext += '报警级别: ' + str(alert[2]) + '\n'
		mailtext += '报警原因：' + str(alert[3]) + '\n'
		mailtext += '报警产生时间：' + str(alert[4]) + '\n'
		mailtext += '报警最后更新时间：' + str(alert[5]) + '\n\n'
		sms_rept_count += 1


#loop end,verify if captured data
logger.debug(' ------ Loop end.')
data.close()

if sms_db_count == 0:
	logger.debug("sms_db_count = 0,nothing to report,out.\n")
	exit(0)


#send mail and sms
logger.debug("Program end,send mail and sms.\n")
mailtext += '\n\n有任何疑问请联系北京中研软科技有限公司。公司网址：www.chinaitsoft.com'
mailsub = 'Oracle本身阀值告警'
smstext += '经检测，发现共' + str(sms_db_count) + '个库发生告警，告警条数共' + str(sms_rept_count) + '条。\\n详细内容已发送至您的邮箱。'
sendmail.send(mailsub,mailtext)
sendsms.send(smstext)

#print mailtext
#print '---'
#print smstext
