#!/bin/sh
#输入sqlplus串,instance_number，输出相邻两个snap Top 10 sql的sta

link=$1
instance_num=$2
file_name=$3
STA_name=sta_${file_name}.txt

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

####################STA
su - oracle<<EOF
sqlplus -S $link <<eof
set heading off
set echo off
set verify off
declare

  v_state boolean;

  --将top_aql结果缓存在临时表中
  cursor c_top_sql_tbs is
  select SQL_TEXT from dba_hist_sqltext;
  type nested_top_sql is table of c_top_sql_tbs%rowtype;
  top_sql_tab nested_top_sql;

  --报告名声明
  v_sta_name varchar2(100);
  
  --判断SAA、STA是否成功生成
  v_sta_state boolean;
  
begin
  v_state := true;

  --获得top_sql结果集
  select *
  BULK COLLECT INTO top_sql_tab
  from (select nvl(st.sql_text, to_clob(' ** SQL Text Not Available ** '))
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
  
  
  
  FOR i IN top_sql_tab.FIRST .. top_sql_tab.LAST  
    LOOP 
      --生成saa、sta报告名
      select  'sta_rep'||i into v_sta_name from dual;
      
      --生成sta报告
      v_sta_state := sta_make(i_task_name => v_sta_name, i_sql_text => top_sql_tab(i).SQL_TEXT);
      
    end loop;
 
end;
/
eof

sqlplus -S $link <<eof
set long 999999
set serveroutput on size 999999
set line 120
set heading off
set echo off
set verify off
set feedback off
spool $STA_name
select DBMS_SQLTUNE.REPORT_TUNING_TASK( 'sta_rep1') from dual;
select DBMS_SQLTUNE.REPORT_TUNING_TASK( 'sta_rep2') from dual;
select DBMS_SQLTUNE.REPORT_TUNING_TASK( 'sta_rep3') from dual;
select DBMS_SQLTUNE.REPORT_TUNING_TASK( 'sta_rep4') from dual;
select DBMS_SQLTUNE.REPORT_TUNING_TASK( 'sta_rep5') from dual;
select DBMS_SQLTUNE.REPORT_TUNING_TASK( 'sta_rep6') from dual;
select DBMS_SQLTUNE.REPORT_TUNING_TASK( 'sta_rep7') from dual;
select DBMS_SQLTUNE.REPORT_TUNING_TASK( 'sta_rep8') from dual;
select DBMS_SQLTUNE.REPORT_TUNING_TASK( 'sta_rep9') from dual;
select DBMS_SQLTUNE.REPORT_TUNING_TASK( 'sta_rep10') from dual;
spool off 
exec dbms_sqltune.drop_tuning_task('sta_rep1');
exec dbms_sqltune.drop_tuning_task('sta_rep2');
exec dbms_sqltune.drop_tuning_task('sta_rep3');
exec dbms_sqltune.drop_tuning_task('sta_rep4');
exec dbms_sqltune.drop_tuning_task('sta_rep5');
exec dbms_sqltune.drop_tuning_task('sta_rep6');
exec dbms_sqltune.drop_tuning_task('sta_rep7');
exec dbms_sqltune.drop_tuning_task('sta_rep8');
exec dbms_sqltune.drop_tuning_task('sta_rep9');
exec dbms_sqltune.drop_tuning_task('sta_rep10');
eof
EOF


