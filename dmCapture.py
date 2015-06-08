#!/usr/bin/python
#-*- coding:utf-8 -*-

import cx_Oracle
import sys

def _getData(cursor,name):
	swapsql="""
	select :target, replace(name, chr(39), 'danyinhao'), value
	  from v$sysstat where name != 'DB time'
	union all
	select :target, name, value
	  from v$pgastat
	union all
	select :target, component, current_size
	  from v$sga_dynamic_components
	union all
	select :target, stat_name, value
	  from v$sys_time_model where stat_name like 'DB%'
	union all
	select :target, replace(event, chr(38), 'yufuhao'), total_waits
	  from v$system_event
	"""
	cursor.execute(swapsql,target = name)
	datas=cursor.fetchall()
	return datas

def _putData(cursor,datas,table):
	try:
		for i in datas:
			insertsql="insert into " + table + " values('%s', replace(replace('%s','danyinhao',chr(39)),'yufuhao',chr(38)), %s)"%(i[0],i[1],i[2])
			cursor.execute(insertsql)
		cursor.execute("commit")
		return True
	except:
		cursor.execute("rollback")
		cursor.execute("commit")
		print sys.exc_info()[1]
		return False

def main(remote_cursor,server_cursor,name,table = 'rawdata_10min'):
		datas = _getData(remote_cursor,name)
		result = _putData(server_cursor,datas,table)
