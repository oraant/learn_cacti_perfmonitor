#!/bin/sh

version=$1
link=$2
baseline=$3
inst_num=$4


####生成文件名
filename=`date +%Y%m%d_%H%M`

######报告生成
/perfmonitor/reports/rep_make.sh $link $inst_num $baseline $version $filename
/perfmonitor/reports/sql_addm.sh $link $inst_num $filename
/perfmonitor/reports/sta_make.sh $link $inst_num $filename

#####发邮件
python /perfmonitor/reports/sendmail.py -f zyrmail@perfm.mail -p zyrmail -s perfm.mail -t zyrmail@perfm.mail -m '你好,客户，我们是北京中言软科技有限公司的高级DBA工程师，现在您的机器存在问题，已发送短信和邮件，请注意查看' /home/oracle/awrrpt_$filename.txt /home/oracle/ashrpt_$filename.txt /home/oracle/awrdiff_$filename.txt /home/oracle/top_sql_elps_$filename.txt /home/oracle/sta_$filename.txt /home/oracle/addm_$filename.txt  #1>/dev/null 2>/movecom/test/python/error.log 
