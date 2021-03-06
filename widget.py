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
def getDbm(flag):
	path_dbm  = sys.path[0] + '/dbm/' + flag
	data = dbm.open(path_dbm,'c')
	return data

def getConf(flag):
	path_conf = sys.path[0] + '/conf/' + flag + '.conf'
	cf = ConfigParser.ConfigParser()
	cf.read(path_conf)
	return cf

def getLogger(flag):
	cf_global = getConf('global')
	log_level = cf_global.getint('server','log_level')

	path_log  = sys.path[0] + '/log/' + flag + '.log'
	fh = logging.FileHandler(path_log)
	formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s -- %(message)s')
	fh.setFormatter(formatter)

	logger = logging.getLogger(flag)
	logger.setLevel(log_level)
	logger.addHandler(fh)

	return logger
	

def getFiles(flag):
	cf = getConf(flag)
	data = getDbm(flag)
	logger = getLogger(flag)
	return cf,data,logger


#decrypt or encrypt one string
def decrypt(string):
	return base64.decodestring(base64.decodestring(base64.decodestring(base64.decodestring(string))))
def encrypt(string):
	return base64.encodestring(base64.encodestring(base64.encodestring(base64.encodestring(string))))


#get slink from config file
conf = getConf('global')
logger = getLogger('global')

def getServer():
	slink = conf.get('server','slink')
	server = cx_Oracle.connect(slink)
	return server


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

def closeNode(conf_path,node,reason,flag):
	print 'closing node'
	cf = ConfigParser.ConfigParser()
	cf.read(conf_path)
	enable = encrypt('False')
	cf.set(node,'enable',enable)
	cf.write(open(conf_path,"w"))

	import sendmail
	import sendsms
	text = '模块 ' + flag + ' 已将节点 ' + node + ' 关闭，原因如下：\n'
	text += reason
	sendmail.send('产品运行报告',text)
	sendsms.send(text)

def basicNode(flag,node,node_conf,node_data):
	data = node_data
	conf = node_conf
	conf_path = sys.path[0] + '/conf/' + flag + '.conf'
	key_string = flag + node + 'failCount'


	enable = decrypt(conf.get(node,'enable')).upper()
	if enable != 'TRUE':
		return False,'not enable, value about enable of this node is ' + enable + '. Or the configure file did not encrypted.'


	tnsname = decrypt(conf.get(node,'tnsname')).lower()
	try:
		db = cx_Oracle.connect(tnsname)
	except:
		failCount = int(getValue(data,key_string,'0')) + 1
		if failCount >= 3:
			reason = 'Connection with ' + node + ' failed three times, closing node.'
			closeNode(conf_path,node,reason,flag)
			return False,reason
		data[key_string] = str(failCount)

		logger.error('can\'t connect to node,node is : ' + node + ', error is : ' + str(sys.exc_info()) + '.\nDetail is : ' + str(sys.exc_info()[1]))
		return False,'connection failed'
	else:
		data[key_string] = '0'


	sql_dbid = 'select dbid from v$database'
	sql_inum = 'select INSTANCE_NUMBER from v$instance'
	cursor = db.cursor()

	cursor.execute(sql_dbid)
	dbid_node = str(cursor.fetchone()[0])
	dbid_conf = decrypt(conf.get(node,'dbid')).lower()
	if dbid_node != dbid_conf:
		reason = 'The dbid of ' + node + ' is wrong, closing node.'
		closeNode(conf_path,node,reason,flag)
		return False,reason

	cursor.execute(sql_inum)
	inum_node = str(cursor.fetchone()[0])
	inum_conf = decrypt(conf.get(node,'instance_num')).lower()
	if inum_node != inum_conf:
		reason = 'The instance number of ' + node + ' is wrong, closing node.'
		closeNode(conf_path,node,reason,flag)
		return False,reason

	return True,db


#verify a node link in advanced mode
def advancedNode(flag,node,node_conf,node_data):
	result = basicNode(flag,node,node_conf,node_data)
	if result[0] == True:
		db = result[1]
	else:
		return False,result[1]


	data = node_data
	key_string = flag + node + 'lasCall'
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
