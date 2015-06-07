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


for node in conf.sections():
	result = w.basicNode('getThreshold',conf,node)
	if result[0] == True:
		db = result[1]
		cursor = db.cursor()
	else:
	        print result[1]
	        exit(1)
	
	
	cursor.execute(sql_latest)
	this_latest = cursor.fetchone()[0]
	last_latest = w.getValue(data,'last_latest','1000-01-01 01:01:01.000009 +08:00')
	
	cursor.execute(sql_report,this_latest = this_latest,last_latest = last_latest)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
