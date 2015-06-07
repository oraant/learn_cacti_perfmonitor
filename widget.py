#/usr/bin/python
#-*- coding:utf-8 -*-

import ConfigParser
import logging
import dbm
import commands
import base64
import sys
import cx_Oracle
import time

#get config,dbm and logger
def getFiles(flag):
	path_conf_global = sys.path[0] + '/conf/global.conf'
	path_conf = sys.path[0] + '/conf/' + flag + '.conf'
	path_log  = sys.path[0] + '/log/' + flag + '.log'
	path_dbm  = sys.path[0] + '/dbm/' + flag

	cf_global = ConfigParser.ConfigParser()
	cf_global.read(path_conf_global)
	log_level = cf_global.getint('server','log_level')

	cf = ConfigParser.ConfigParser()
	cf.read(path_conf)

	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s -- %(message)s')
	fh = logging.FileHandler(path_log)
	fh.setFormatter(formatter)

	logger = logging.getLogger(flag)
	logger.setLevel(log_level)
	logger.addHandler(fh)

	data = dbm.open(path_dbm,'c')

	return cf,data,logger


#decrypt or encrypt one string
def decrypt(string):
	return base64.decodestring(base64.decodestring(base64.decodestring(base64.decodestring(string))))
def encrypt(string):
	return base64.encodestring(base64.encodestring(base64.encodestring(base64.encodestring(string))))


#get slink from config file
conf,data,logger = getFiles('global')
def getSlink():
	return conf.get('server','slink')


#if a model can run
def verifyMac():
	cf_verify = ConfigParser.ConfigParser()
	cf_verify.read(sys.path[0] + '/conf/verify.conf')
	mac = decrypt(cf_verify.get("mac", "mac"))

	command = "/sbin/ifconfig -a|grep HWaddr|head -1|awk '{print $NF}'"
	(status,output) = commands.getstatusoutput(command)

	if status != 0:
		logger.error('can\'t get mac from linux,output is : ' + output)
		return False
	elif output != mac:
		logger.error('wrong mac,configure is ' + mac + ',ifconfig is ' + output)
		return False
	else:
		return True

def verifyEnable(flag):
	if conf.getboolean('enable','global') != True:
		return False
	if conf.getboolean('enable',flag) != True:
		return False
	if verifyMac() != True:
		return False
	return True


#verify a node link in basic mode
def getValue(data,key,default):
	for i in data.keys():
		if i == key:
			return data[i]
	return default

def closeNode(conf_path,node):
	cf = ConfigParser.ConfigParser()
	cf.read(conf_path)
	enable = encrypt('False')
	cf.set(node,'enable',enable)
	cf.write(open(conf_path,"w"))


def basicNode(flag,conf,node):
	conf_path = sys.path[0] + '/conf/' + flag + '.conf'
	key_string = flag + 'failCount'


	enable = decrypt(conf.get(node,'enable')).upper()
	if enable != 'TRUE':
		return False,'not enable'


	tnsname = decrypt(conf.get(node,'tnsname')).lower()
	try:
		db = cx_Oracle.connect(tnsname)
	except:
		failCount = int(getValue(data,key_string,'0')) + 1
		if failCount >= 3:
			closeNode(conf_path,node)
		data[key_string] = str(failCount)

		logger.error('can\'t connect to node,error is : ' + sys.exc_info() + '.\nDetail is : ' + sys.exc_info()[1])
		return False,'failed three times'
	else:
		data[key_string] = '0'


	sql_dbid = 'select dbid from v$database'
	sql_inum = 'select INSTANCE_NUMBER from v$instance'
	cursor = db.cursor()

	cursor.execute(sql_dbid)
	dbid_node = str(cursor.fetchone()[0])
	dbid_conf = decrypt(conf.get(node,'dbid')).lower()
	if dbid_node != dbid_conf:
		closeNode(conf_path,node)
		return False,'dbid is wrong'

	cursor.execute(sql_inum)
	inum_node = str(cursor.fetchone()[0])
	inum_conf = decrypt(conf.get(node,'instance_num')).lower()
	if inum_node != inum_conf:
		closeNode(conf_path,node)
		return False,'instance number is wrong' 

	return True,db


#verify a node link in advanced mode
def advancedNode(flag,conf,node):
	result = basicNode('getOracle',conf,'xuniji')
	if result[0] == True:
		db = result[1]
	else:
		return False,result[1]

	
	key_string = flag + 'lasCall'
	lastcall = float(getValue(data,key_string,'0'))
	nowtime = time.time()
	diff = nowtime - lastcall
	data[key_string] = str(nowtime)
	if diff > 700:
		return False,'time interval out of range,gap is : ' + str(diff)


	cursor = db.cursor()
	sql_running = 'select (sysdate-startup_time)*24*3600 from v$instance'
	cursor.execute(sql_running)
	running_time = cursor.fetchone()[0]
	if running_time < 700:
		return False,'running time less than 10min,running time is : ' + str(running_time)
	else:
		return True,db
