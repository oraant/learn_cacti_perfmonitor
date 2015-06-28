#!/bin/sh

link=$1
version=$2
inst_num=$3
baseline=$4


####生成文件名
filename=`date +%Y%m%d_%H%M`

######报告生成
/perfmonitor/reports/rep_make.sh $link $inst_num $baseline $version $filename > /perfmonitor/log/reports.log
/perfmonitor/reports/sql_addm.sh $link $inst_num $filename >> /perfmonitor/log/reports.log
/perfmonitor/reports/sta_make.sh $link $inst_num $filename >> /perfmonitor/log/reports.log

#####发邮件
python /perfmonitor/reports/sendmail.py -f zyrmail@perfm.mail -p zyrmail -s perfm.mail -t test@perfm.mail -m "数据库 $link 的AWR, AWR_DIFF, ASH, ADDM, STA 报告已生成，>详情请见附件。" /home/oracle/awrrpt_$filename.txt /home/oracle/ashrpt_$filename.txt /home/oracle/awrdiff_$filename.txt /home/oracle/top_sql_elps_$filename.txt /home/oracle/sta_$filename.txt /home/oracle/addm_$filename.txt > /dev/null 2>>/perfmonitor/log/reports.err || echo -e "`date` \n" >>/perfmonitor/log/reports.err


#####转移文件到指定目录
mv /home/oracle/*$filename* /home/oracle/perf_reports > /dev/null 2>>/perfmonitor/log/reports.err || echo -e "`date` \n" >>/perfmonitor/log/reports.err
