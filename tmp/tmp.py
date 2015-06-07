#!/usr/bin/python
#-*- coding:utf-8 -*-

import inc

def f(eee):
	for i in ['aaa','bbb','ccc']:
		if i == eee:
			return 'rrr'
	return 'nothing'


print f('aaa')
