#!/usr/bin/python
#-*- coding:utf-8 -*-

import inc
import time

a = float(str(0))
print type(a)
print a
print type(90)

old = time.time()
print 'old is : ' + str(old)

time.sleep(3)

now = time.time()
print 'now is : ' + str(now)

if now - old >= 2:
	print '\n>2'
else:
	print '\n<2'
