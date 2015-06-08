#!/usr/bash/python
# -*- coding: utf-8 -*-

import sys
import smtplib
import getopt
import widget as w
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart


#verify if this model can run
if w.verifyEnable('sendmail') != True:
        print 'model can not run'
        exit(0)


#get base configure
conf = w.conf
targets = conf.get('sendto','mails').split()
mail_from = conf.get('server','mail_from')
mail_pass = conf.get('server','mail_pass')
mail_server = conf.get('server','mail_server')
mail_text = '内容为空'


#get messages
msg = MIMEMultipart()

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def getatt(attachment):
	att = MIMEText(open(attachment, 'rb').read(), 'base64','gb2312')
	att["Content-Type"] = 'application/octet-stream'
	att["Content-Disposition"] = "attachment; filename=\""+arg+"\""
	return att

def report(text,attachments):
        for attachment in attachments:
		att = getatt(attachment)
                msg.attach(att)
	send(text)

def send(text):
	mail_text = MIMEText(text,_charset='utf-8')
	msg.attach(mail_text)
	sendToTargets()

def sendToTargets():
	server = smtplib.SMTP(mail_server, 25)
	server.set_debuglevel(0)
	server.login(mail_from, mail_pass)

	msg['From'] = _format_addr(u'中研软perfmonitor性能预警平台 <%s>' % mail_from)
	msg['Subject'] = Header(u'产品运行报告', 'utf-8').encode()

	for target in targets:
		msg['To'] = _format_addr(u'产品用户 <%s>' % target)
		server.sendmail(mail_from, target, msg.as_string())
	server.quit()