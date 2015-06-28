#!/usr/bash/python
# -*- coding: utf-8 -*-
#author:'Micheal Dee'

import sys
import smtplib
import getopt
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart

#声明
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

from_addr = 'From: '
password = 'Password: '
smtp_server = 'SMTP server: '
to_addr = 'To: '

msg = MIMEMultipart()
print '------------------------'
print msg

#构造附件1
try:
        opts,args = getopt.getopt(sys.argv[1:], "f:p:s:t:m:",["help"])
except getopt.GetoptError:
        print "Error "#info as you want to give out
        sys.exit(1)
else:
        for opt,value in opts:
                if opt == '-f':
                        from_addr = value
                elif opt == '-p':
                        password = value
                elif opt == '-s':
                        smtp_server = value

                elif opt == '-t':
                        to_addr = value
                elif opt == '-m':
                        message = value
                elif opt == '--help':
                        print ("Usage:%s [-f|-p|-s|-t|-m] [--help| args...." );
                        sys.exit(5)

        #这个构造调用附件
        for arg in args:
                att1= MIMEText(open(arg, 'rb').read(), 'base64','gb2312')
                att1["Content-Type"] = 'application/octet-stream'
                att1["Content-Disposition"] = "attachment; filename=\""+arg+"\""
                msg.attach(att1)
                print '------------------------'
                print msg


text = MIMEText(message,_charset='utf-8')
msg.attach(text)
print '------------------------'
print msg

msg['From'] = _format_addr(u'中研软数据库运维预警监控平台 <%s>' % from_addr)
msg['To'] = _format_addr(u'产品用户 <%s>' % to_addr)
msg['Subject'] = Header(u'数据库性能诊断报告', 'utf-8').encode()
print '------------------------'
print msg

server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(0)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
