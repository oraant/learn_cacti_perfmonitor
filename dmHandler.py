#!/usr/bin/python
#-*- coding:utf-8 -*-

import cx_Oracle
import time

def _systime():
	return time.strftime('%y-%m-%d %H:%M:%S',time.localtime(time.time()))

def delNode(cursor,node):
	sql_delete_all = 'delete from rawdata_10min_last where target_name = :target_name'
	cursor.execute(sql_delete_all,target_name = node)
	cursor.execute('commit')


def delAll(cursor):
	sql_delete_all = 'delete from rawdata_10min_last'
	cursor.execute(sql_delete_all)
	cursor.execute('commit')

def _toLast(cursor):
	delAll(cursor)
	sql_rawdata_to_last = 'insert /*+append*/ into rawdata_10min_last select r.target_name, r.param_name, r.param_value from rawdata_10min r'
	cursor.execute(sql_rawdata_to_last)
	cursor.execute('commit')

def _archive(cursor):
	sql_archive_rawdata = "insert /*+append*/ into rawdata_arch select to_date(:time,'YY-MM-DD HH24:MI:SS'),10,r.target_name,r.param_name,r.param_value from rawdata_10min r"
	sql_archive_calvalue = "insert /*+append*/ into calvalue_arch select to_date(:time,'YY-MM-DD HH24:MI:SS'),10,r.target_name,r.param_name,r.param_value from calvalue_10min r"
	cursor.execute(sql_archive_rawdata, time = _systime())
	cursor.execute(sql_archive_calvalue, time = _systime())
	cursor.execute('commit')

def _clear(cursor):
	sql_clear_rawdata = "delete from rawdata_10min"
	sql_clear_calvalue = "delete from calvalue_10min"
	cursor.execute(sql_clear_rawdata)
	cursor.execute(sql_clear_calvalue)
	cursor.execute('commit')

def begin(cursor):
	_clear(cursor)

def end(cursor):
	_toLast(cursor)
	_archive(cursor)
	
def calculate(cursor,target,param_table):
	current_rawdata_10min_to_calvalue = '''
        insert /*+append*/ into calvalue_10min
          select r.target_name, r.param_name, r.param_value / p.divisor
            from rawdata_10min r
            join ''' + param_table + ''' p
              on r.param_name = p.param_name
           where p.param_type = 'current'
             and r.target_name = :target_name
        '''

	aggregate_rawdata_10min_to_calvalue = '''
        insert /*+append*/ into calvalue_10min
          select r.target_name,
                 r.param_name,
                 (r.param_value - rl.param_value) / p.divisor
            from rawdata_10min r
            join ''' + param_table + ''' p
              on r.param_name = p.param_name
            join rawdata_10min_last rl
              on rl.param_name = p.param_name
           where p.param_type = 'aggregate'
             and r.target_name = :target_name
             and rl.target_name = :target_name
        '''

	cursor.execute(current_rawdata_10min_to_calvalue, target_name = target)
	cursor.execute('commit')
	cursor.execute(aggregate_rawdata_10min_to_calvalue, target_name = target)
	cursor.execute('commit')
