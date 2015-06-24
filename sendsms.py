#!/usr/bin/python
#-*- coding:utf-8 -*-

import commands
import widget as w

logger = w.getLogger('sendsms')

def verifyUsable():
	command = "/usr/bin/env gnokii --identify"
        (status,output) = commands.getstatusoutput(command)

        if status != 0:
                logger.error('can\'t get mac from linux,output is : ' + output)
                return False
        else:
                return True


