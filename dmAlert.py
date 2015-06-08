#!/usr/bin/python
#-*- coding:utf-8 -*-

add_node = '''
insert into alert_10min (target_name,param_name) 
select c,param_name
  from parameter_oracle11g
  cross join (select 'yitiji' c from dual
        union
        select 'xuniji' c from dual) targets;
commit;
'''

last_month = '''
update alert_10min
   set last_month =
       (select max(param_value)
          from calvalue_arch
         where update_time >=
               sysdate - to_yminterval('P1M') - to_dsinterval('PT30M')
           and update_time <=
               sysdate - to_yminterval('P1M') + to_dsinterval('PT30M')
           and alert_10min.target_name = calvalue_arch.target_name
           and alert_10min.param_name = calvalue_arch.param_name
         group by target_name, param_name);
commit;
'''

last_week = '''
update alert_10min
   set last_week =
       (select max(param_value)
          from calvalue_arch
         where update_time >=
               sysdate - to_dsinterval('P7D') - to_dsinterval('PT30M')
           and update_time <=
               sysdate - to_dsinterval('P7D') - to_dsinterval('PT30M')
           and alert_10min.target_name = calvalue_arch.target_name
           and alert_10min.param_name = calvalue_arch.param_name
         group by target_name, param_name);
commit;
'''

get_alert = '''
select *
  from (select a.target_name,
               a.param_name,
               c.param_value,
               case a.flag
                 when 'manul_value' then
                  a.manul_value
                 when 'last_month' then
                  a.last_month
                 when 'last_week' then
                  a.last_week
                 when 'last_time' then
                  GREATEST(a.last_month, a.last_week)
                 when 'max_value' then
                  GREATEST(a.manul_value, a.last_month, a.last_week)
               end alert_value
          from alert_10min a
          join calvalue_10min c
            on a.target_name = c.target_name
           and a.param_name = c.param_name)
 where param_value > alert_value
'''
