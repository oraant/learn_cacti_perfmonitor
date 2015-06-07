#!/usr/bin/python
#-*- coding:utf-8 -*-

import inc
import ConfigParser

cf = ConfigParser.ConfigParser()
cf.read('config')

conf = ConfigParser.ConfigParser()
conf.read('config')

for i in conf.sections():
	print i

for i in cf.sections():
	print i

conf.set('A','a','oooo')
cf.set('A','a','cfcfcfcf')
cf.write(open('config',"w"))
conf.write(open('config',"w"))
