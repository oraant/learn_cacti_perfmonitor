#!/usr/bin/python
#-*- coding:utf-8 -*-

#add one node's parameters into alert table
def addNode(cursor,target,param_table):
	sql_add_node = """
	insert into alert_10min (target_name,param_name) 
	select target_name,param_name
	  from """ + param_table + """
	 cross join (select '""" + target + """' target_name from dual)
	"""

	cursor.execute(sql_add_node)
	cursor.execute('commit')


#get history value at the same hour but last week or last month
def getDynamic(cursor):
	sql_get_last_month = '''
	update alert_10min
	   set last_month =
	       (select max(param_value)*1.3
	          from calvalue_arch
	         where update_time >=
	               sysdate - to_yminterval('P1M') - to_dsinterval('PT30M')
	           and update_time <=
	               sysdate - to_yminterval('P1M') + to_dsinterval('PT30M')
	           and alert_10min.target_name = calvalue_arch.target_name
	           and alert_10min.param_name = calvalue_arch.param_name
	         group by target_name, param_name)
	'''

	sql_get_last_week = '''
	update alert_10min
	   set last_week =
	       (select max(param_value)*1.3
	          from calvalue_arch
	         where update_time >=
	               sysdate - to_dsinterval('P7D') - to_dsinterval('PT30M')
	           and update_time <=
	               sysdate - to_dsinterval('P7D') - to_dsinterval('PT30M')
	           and alert_10min.target_name = calvalue_arch.target_name
	           and alert_10min.param_name = calvalue_arch.param_name
	         group by target_name, param_name)
	'''

	sql_get_last_hour = '''
	update alert_10min
	   set last_week =
	       (select max(param_value)
	          from calvalue_arch
	         where update_time >=
	               sysdate - to_dsinterval('PT60M')
	           and update_time <= sysdate
	           and alert_10min.target_name = calvalue_arch.target_name
	           and alert_10min.param_name = calvalue_arch.param_name
	         group by target_name, param_name)
	'''

	sql_get_last_hour2 = '''
	update alert_10min
	   set last_month =
	       (select min(param_value)
	          from calvalue_arch
	         where update_time >=
	               sysdate - to_dsinterval('PT60M')
	           and update_time <= sysdate
	           and alert_10min.target_name = calvalue_arch.target_name
	           and alert_10min.param_name = calvalue_arch.param_name
	         group by target_name, param_name)
	'''

	#cursor.execute(sql_get_last_month)
	#cursor.execute(sql_get_last_week)
	cursor.execute(sql_get_last_hour)
	cursor.execute(sql_get_last_hour2)
	cursor.execute('commit')


#get current value and compare with alert value
def getAlert(cursor):
	sql_get_alert = '''
	select *
	  from (select a.target_name,
	               a.param_name,
	               c.param_value,
	               case nvl(a.flag, 'last_time')
	                 when 'manul_value' then
	                  a.manul_value
	                 when 'last_month' then
	                  a.last_month
	                 when 'last_week' then
	                  a.last_week
	                 when 'last_time' then
	                  case
	                    when a.last_month is null and a.last_week is null then
	                     null
	                    when a.last_month is null then
	                     a.last_week
	                    when a.last_week is null then
	                     a.last_month
	                    else
	                     greatest(a.last_month, a.last_week)
	                  end
	               end as alert_value
	          from alert_10min a
	          join calvalue_10min c
	            on a.target_name = c.target_name
	           and a.param_name = c.param_name)
	 where param_value > alert_value
	 order by target_name
	'''
	cursor.execute(sql_get_alert)
	datas = cursor.fetchall()
	return datas
