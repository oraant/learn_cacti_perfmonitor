#!/usr/bin/python
#-*- coding:utf-8 -*-

import widget as w
import logging
import dbm
import ConfigParser
import cx_Oracle
import time

if w.verifyEnable('threshold') != True:
	print 'model can not run'
        exit(0)

conf,data,logger = w.getFiles('getThreshold')


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

mailtext = '来自Perfmonitor阈值告警功能的报告：\n\n\n'
smstext = 'Perfmonitor阈值告警功能：\\n'
sms_db_count = 0
sms_rept_count = 0

for node in conf.sections():
	result = w.basicNode('getThreshold',conf,node)
	if result[0] == True:
		db = result[1]
		cursor = db.cursor()
	else:
	        print result[1]
	        exit(1)
	
	
	cursor.execute(sql_latest)
	sql_result = cursor.fetchall()
	if len(sql_result) == 0:
		continue
	else:
		this_latest = sql_result[0][0]

	key_string = node + 'last_latest'
	last_latest = w.getValue(data,key_string,'1000-01-01 01:01:01.000009 +08:00')
	data[key_string] = this_latest
	
	cursor.execute(sql_report,this_latest = this_latest,last_latest = last_latest)
	datas = cursor.fetchall()
	if len(datas) == 0:
		continue

	tnsname = w.decrypt(conf.get(node,'tnsname'))
	mailtext += '\n产生告警的库的连接是：' + tnsname + '\n'
	sms_db_count += 1
	for data in datas:
		mailtext += '报警的实例号：' + str(data[0]) + '\n'
		mailtext += '报警的序号：' + str(data[1]) + '\n'
		mailtext += '报警级别: ' + str(data[2]) + '\n'
		mailtext += '报警原因：' + str(data[3]) + '\n'
		mailtext += '报警产生时间：' + str(data[4]) + '\n'
		mailtext += '报警最后更新时间：' + str(data[5]) + '\n\n'
		sms_rept_count += 1

if sms_db_count == 0:
	exit(0)

mailtext += '\n\n有任何疑问请联系北京中研软科技有限公司。公司网址：www.chinaitsoft.com'
smstext += '经检测，发现共' + str(sms_db_count) + '个库发生告警，告警条数共' + str(sms_rept_count) + '条。\\n详细内容已发送至您的邮箱。'

#sendmail.send(mailtext)
#sendsms.send(smstext)
print mailtext
print '---'
print smstext
