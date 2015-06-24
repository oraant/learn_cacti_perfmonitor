#!/usr/bin/python
#-*- coding:utf-8 -*-

import commands
import time
import widget as w


#verify if this model can run
if w.verifyEnable('sendsms') != True:
        exit(0)

#get base configure
logger = w.getLogger('sendsms')
conf = w.conf
targets = conf.get('sendto','tels').split()


#verify if GSM MODEM is usable
def verifyUsable():
	command = "/usr/local/bin/gnokii --identify"
	(status,output) = commands.getstatusoutput(command)

	if status == 0:
		logger.debug('GSM MODEM is OK')
		return True
	else:
		logger.error('GSM MODEM not usable,\n\toutput is : \n' + output + '\n')
		return False


#send messages to targets
def send(string):

	if verifyUsable() != True:
		exit(1)

	for target in targets:
		logger.debug('Try to send sms to ' + target)
		command = "echo '" + string + "'|/usr/local/bin/gnokii --sendsms " + target
		(status,output) = commands.getstatusoutput(command)

		if status == 0:
			logger.debug('Message has send successful.')
		elif status == 11:
			logger.error('Time out, please move the movecom! \n\toutput is : ' + output)
		elif status == 27:
			logger.error('SIM card has problem, please check it. \n\toutput is : ' + output)
		elif status == 255:
			logger.error('USB connection has problem, please check it. \n\toutput is : ' + output)
		else:
			logger.error('Message send failed with unknown error. status = ' + str(status) + '\n\toutput is : ' + output)

	logger.debug('sendsms model finished.\n')
