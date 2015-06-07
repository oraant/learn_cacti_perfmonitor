#!/usr/bin/python
#-*- coding:utf-8 -*-

import ConfigParser
import logging
import dbm
import commands
import base64
import sys

#get config,dbm and logger
def getfiles(flag):
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
conf,data,logger = getfiles('global')
def getslink():
	return conf.get('server','slink')


#if a model can run
def verifymac():
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

def verifyenable(flag):
	if conf.getboolean('enable','global') != True:
		return False
	if conf.getboolean('enable',flag) != True:
                return False
	if verifymac() != True:
                return False
	return True
