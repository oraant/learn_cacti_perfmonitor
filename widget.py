#!/usr/bin/python
#-*- coding:utf-8 -*-

import ConfigParser
import logging
import dbm
import commands
import base64
import sys

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
