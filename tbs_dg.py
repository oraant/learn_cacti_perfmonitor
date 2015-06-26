#!/usr/bin/env python
#-*- coding:utf-8 -*-

import widget as w
import logging
import dbm
import ConfigParser
import cx_Oracle
import time
import sendmail
import sendsms

#Get basic info : enable or not, configure file, dbm file, logger, and sql statements.
if w.verifyEnable('tbs_dg') != True:
	exit(1)

conf,local_data,logger = w.getFiles('getTbs_dg')
local_data.close()
logger.debug(" ====== Model start. ====== ")

#Define sql text to get remote data
sql_for_dg = 'select name, (total_mb-free_mb)/total_mb*100  "percent" from v$asm_diskgroup'
sql_for_tbs = 'select a.tablespace_name, round(((totalspace - nvl(freespace, 0)) / totalspace), 3) * 100 "Used_Rate(%)", totalspace || \' M\' "Sum_space(M)", round((totalspace - nvl(freespace, 0)), 3) || \' M\' "Used_space(M)" from (select tablespace_name, sum(bytes) / 1048576 totalspace from dba_data_files group by tablespace_name) a, (select tablespace_name, sum(Bytes) / 1048576 freespace from dba_free_space group by tablespace_name) b where a.tablespace_name = b.tablespace_name(+) union select a.tablespace_name, round(nvl(used_space, 0) / space * 100, 2) "Used_Rate(%)", space || \' M\' "Sum_space(M)", used_space || \' M\' "Used_space(M)" from (select tablespace_name, round(sum(bytes) / (1024 * 1024), 2) space, sum(blocks) blocks from dba_temp_files group by tablespace_name) a, (select tablespace_name, round(sum(bytes_used) / (1024 * 1024), 2) used_space, round(sum(bytes_free) / (1024 * 1024), 2) free_space from v$temp_space_header group by tablespace_name) b where a.tablespace_name = b.tablespace_name(+)'

#Predefine variables for ergodic
mailtext = '来自Perfmonitor表空间及DG告警功能的报告：\n\n\n'
smstext = 'Perfmonitor表空间及DG告警功能：\\n'
send = False
global_alert_value = 70
logger.debug("global_alert_value = " + str(global_alert_value))

#Ergodic every node in configure file
for node in conf.sections():

        #Connect with node
        logger.debug(" ------ Enter into loop,node is " + node + " ------ ")
        result = w.basicNode('getTbs_dg',conf,node)
        if result[0] == True:
                db = result[1]
                cursor = db.cursor()
                logger.debug("Got connection and cursor from " + node)
        else:
                logger.warning("Connect failed with " + node + ". \n\tReason is : " + result[1])
                continue

        #Get information about remote disk group
        logger.debug('begin fetch data from v$asm_diskgroup table.')
        cursor.execute(sql_for_dg)
        sql_dgs = cursor.fetchall()
        if len(sql_dgs) == 0:
                logger.debug('did not get data from v$asm_diskgroup table.')
	else:
	        logger.debug('got datas from v$asm_diskgroup, now format it.')
		#Ergodic every dg key-value in this node
		mailtext += '节点：' + node + '的asm磁盘使用情况：\n'
	        for sql_dg in sql_dgs:
	         	#Contrast the current value with pre-define value in configure file       
	                try:
				alert_value = int(w.decrypt(conf.get(node,str(sql_dg[0]))))
			except:
				logger.error("Didn't get data from conf for " + sql_dg[0] + ", use default global_alert_value, node is " + node)
				alert_value = global_alert_value
			finally:
				if sql_dg[1] > alert_value:
					dg_name = str(sql_dg[0])
					dg_value = str(sql_dg[1])
					mailtext += '\tASM磁盘：' + dg_name + ' 的使用率为：' + dg_value + ' ，超出预设的：' + str(alert_value) + '%\n'
				        send = True


        #Get information about remote tablespace
        logger.debug('begin fetch data from tablespace table.')
        cursor.execute(sql_for_tbs)
        sql_tbss = cursor.fetchall()
        if len(sql_tbss) == 0:
                logger.debug('did not get remote tablespace information.')
	else:
        	logger.debug('got remote tablespace information, now format it.')
		#Ergodic every tbs key-value in this node
		mailtext += '节点：' + node + '的表空间使用情况：\n'
	        for sql_tbs in sql_tbss:
	      		#Contrast the current value with pre-define value in configure file      
	                try:
				alert_value = int(w.decrypt(conf.get(node,str(sql_tbs[0]))))
			except:
				logger.error("Didn't get data from conf for " + sql_tbs[0] + ", use default global_alert_value, node is " + node)
				alert_value = global_alert_value
			finally:
				if sql_tbs[1] > alert_value:
					tbs_name = str(sql_tbs[0])
					tbs_value = str(sql_tbs[1])
					mailtext += '\t表空间：' + tbs_name + ' 的使用率为：' + tbs_value + ' ，超出预设的：' + str(alert_value) + '%\n'
					send = True
				                        
	#Close connection and cursor for this node
	cursor.close()
	db.close()
	mailtext += '\n'

#Loop end
logger.debug(' ------ Loop end.')

#Send mail and sms
if send == True:
	logger.debug("found alert value,send mail and sms.\n")
	mailtext += '\n\n有任何疑问请联系北京中研软科技有限公司。\n公司网址：www.chinaitsoft.com'
	smstext = mailtext
	sendmail.send(mailtext)
	sendsms.send(smstext)

logger.debug("Program end.exit")

#print mailtext
#print '---'
#print smstext
