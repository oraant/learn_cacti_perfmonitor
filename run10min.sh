#!/bin/bash

PATH=$PATH:$HOME/bin
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/u01/app/oracle/product/11.2.0/db_1/lib/
export ORACLE_BASE=/u01/app/oracle
export ORACLE_HOME=$ORACLE_BASE/product/11.2.0/db_1
export ORACLE_UNQNAME=db11g
export ORACLE_SID=db11g
export PATH=$ORACLE_HOME/bin:$ORACLE_HOME/OPatch:$PATH

export PATH
export LD_LIBRARY_PATH
export NLS_LANG='SIMPLIFIED CHINESE_CHINA.AL32UTF8'


sleep 10;/usr/bin/python /perfmonitor/tbs_dg.py 1>>/perfmonitor/run.log 2>&1 || echo -e "`date` \n" >>/perfmonitor/run.log
sleep 20;/usr/bin/python /perfmonitor/dataManager.py 1>>/perfmonitor/run.log 2>&1 || echo -e "`date` \n" >>/perfmonitor/run.log
