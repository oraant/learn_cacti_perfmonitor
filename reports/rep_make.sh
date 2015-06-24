#!/bin/sh
###第一个参数输入dblink连接串
###第二个参数输入对象instance_number
###第三个参数输入AWR基线名
###第四个参数输入数据库版本
###第五个参数输入文件名

dblink=$1
instance_num=$2
baseline_name=$3
version=$4
file_name=$5

#user define

tempfile=/root/tmp/tmpfile
awr_type=text
awr_day=1
awr_diff_day=30
report_type=text
report_start_time=-10
report_end_time=10
#..DB_time...

if [[ $version = 10 ]] ; then
ashscript=@?/rdbms/admin_10g/ashrpt.sql
fi

if [[ $version = 11 ]] ; then
ashscript=@?/rdbms/admin/ashrpt.sql
fi

export ORACLE_BASE=/u01/app/oracle
export ORACLE_HOME=$ORACLE_BASE/product/11.2.0/db_1
export ORACLE_UNQNAME=db11g
export ORACLE_SID=db11g
export PATH=$ORACLE_HOME/bin:$PATH



#..DBtime..30min.......
su - oracle<<EOF_ORACLE
sqlplus -S $dblink <<eof
set echo off
set verify off
set head off
--......
exec DBMS_WORKLOAD_REPOSITORY.CREATE_SNAPSHOT ();
eof
sqlplus -S $dblink <<eof
set echo off
set verify off
set head off

spool sqluser1.txt
--..awr..snap
select * from (select snap_id from dba_hist_snapshot where snap_id < (select max(snap_id) from dba_hist_snapshot) and instance_number = $instance_num order by snap_id desc) where rownum = 1;
select max(snap_id) from dba_hist_snapshot where instance_number = $instance_num;
--..awrdiff..snap
select start_snap_id from dba_hist_baseline where baseline_name = '$baseline_name';
select end_snap_id from dba_hist_baseline where baseline_name = '$baseline_name';
select to_char(time + INTERVAL '-5' minute,'YYYY/MM/DD HH24:MI:SS') from (select max(record_time) time from records_m_user);
spool off
eof
EOF_ORACLE


#.spool.....
#sed 's/\ //g' /home/oracle/sqluser1.txt > /home/oracle/sqluser2.txt
#sed '/^$/d' /home/oracle/sqluser2.txt > /home/oracle/user1.txt
sed '/^$/d' /home/oracle/sqluser1.txt > /home/oracle/sqluser2.txt
awk '{ printf "%-10s %s\n", $1, $2 ;}' /home/oracle/sqluser2.txt > /home/oracle/user1.txt
rm -f /home/oracle/sqluser1.txt /home/oracle/sqluser2.txt
rm -f /home/oracle/sqluser1.txt /home/oracle/sqluser2.txt


#提取参数
beg_id=`cat /home/oracle/user1.txt|awk 'NR==1{print $1}'`
end_id=`cat /home/oracle/user1.txt|awk 'NR==2{print $1}'`
diff_beg_id=`cat /home/oracle/user1.txt|awk 'NR==3{print $1}'`
diff_end_id=`cat /home/oracle/user1.txt|awk 'NR==4{print $1}'`
sort_begin_time=`cat /home/oracle/user1.txt|awk 'NR==5{print $1,$2}'`



#生成报告名
awr_name=awrrpt_${file_name}.txt
awr_diff_name=awrdiff_${file_name}.txt
report_name=ashrpt_${file_name}.txt
#echo "awr_name:'$awr_name' awr_diff_name:'$awr_diff_name' report_name:'$report_name' sort_begin_time:'$sort_begin_time'"
rm -f /home/oracle/user1.txt
#echo "report_type:'$report_type' report_start_time:'$report_start_time' report_end_time:'$report_end_time' report_name:'$report_name'"


#生成报告
su - oracle<<EOF_ORACLE
sqlplus $dblink  <<eof
$ashscript
$report_type
$report_start_time
$report_end_time
$report_name
@?/rdbms/admin/awrrpt.sql
$awr_type
$awr_day
$beg_id
$end_id
$awr_name
@?/rdbms/admin/awrddrpt.sql
$awr_type
$awr_day
$beg_id
$end_id
$awr_diff_day
$diff_beg_id
$diff_end_id
$awr_diff_name
eof
EOF_ORACLE
