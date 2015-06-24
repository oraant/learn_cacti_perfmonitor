#!/bin/bash
#输入sqlplus串,instance_number，输出相邻两个snap的top sql 、addm

link=$1
instance_num=$2
file_name=$3
top_sql_name=top_sql_elps_${file_name}.txt
addm_name=addm_${file_name}.txt

export ORACLE_BASE=/u01/app/oracle
export ORACLE_HOME=$ORACLE_BASE/product/11.2.0/db_1
export ORACLE_UNQNAME=db11g
export ORACLE_SID=db11g
export PATH=$ORACLE_HOME/bin:$PATH

su - oracle<<EOF
sqlplus -S $link <<eof
set heading off
set echo off
set verify off
set feedback off
set numwidth 12
spool base_info.txt
select snap_id,snap_id-1,dbid from (select * from dba_hist_snapshot order by snap_id desc) where rownum = 1;
spool off
eof
EOF

end_snap=`cat /home/oracle/base_info.txt|awk 'NR==2{print $1}'`
begin_snap=`cat /home/oracle/base_info.txt|awk 'NR==2{print $2}'` 
v_dbid=`cat /home/oracle/base_info.txt|awk 'NR==2{print $3}'`
rm -f /home/oracle/base_info.txt

####################top sql

su - oracle<<EOF
sqlplus -S $link <<eof
set heading on
set echo off
set verify off
set pagesize 5000
set linesize 300
set long 400000
set feedback off
set numwidth 12
column sql_id format a15
column sql_text format a100
spool $top_sql_name
select *
  from (select nvl((sqt.elap / 1000000), to_number(null)) elappct,
               sqt.exec,
               sqt.sql_id,
               nvl(st.sql_text, to_clob(' ** SQL Text Not Available ** ')) sql_text
          from (select sql_id,
                       max(module) module,
                       sum(elapsed_time_delta) elap,
                       sum(cpu_time_delta) cput,
                       sum(executions_delta) exec
                  from dba_hist_sqlstat
                 where dbid = $v_dbid
                   and instance_number = $instance_num
                   and $begin_snap < snap_id
                   and snap_id <= $end_snap
                 group by sql_id) sqt,
               dba_hist_sqltext st
         where st.sql_id(+) = sqt.sql_id
           and st.dbid(+) = $v_dbid
         order by nvl(sqt.elap, -1) desc, sqt.sql_id)
 where rownum < 65
   and (rownum <=10);
spool off
eof
EOF
   
####################addm
su - oracle<<EOF
sqlplus -S $link <<eof
--删除
exec dbms_advisor.delete_task(task_name => 'DEMO_ADDM01');

--生成优化建议
DECLARE
    task_name VARCHAR2(30) := 'DEMO_ADDM01';
    task_desc VARCHAR2(30) := 'ADDM Feature Test';
    task_id NUMBER;
BEGIN
    dbms_advisor.create_task('ADDM', task_id, task_name, task_desc, null);
    dbms_advisor.set_task_parameter(task_name, 'START_SNAPSHOT', $begin_snap);
    dbms_advisor.set_task_parameter(task_name, 'END_SNAPSHOT', $end_snap);
    dbms_advisor.set_task_parameter(task_name, 'INSTANCE', $instance_num);
    dbms_advisor.set_task_parameter(task_name, 'DB_ID', $v_dbid);
    dbms_advisor.execute_task(task_name);
END;
/
eof

sqlplus -S $link <<eof
--查看
SET LONG 1000000 PAGESIZE 0 LONGCHUNKSIZE 1000
set echo off
set verify off
set feedback off
COLUMN get_clob FORMAT a80
spool $addm_name
SELECT dbms_advisor.get_task_report('DEMO_ADDM01', 'TEXT', 'ALL') FROM DUAL;
spool off
eof
EOF
