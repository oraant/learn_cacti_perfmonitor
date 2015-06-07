#!/usr/bin/python
#150527-1421


import base64
import ConfigParser
import commands
import sys


#functions
def usage():
	print '\nInput parameter is wrong.'
	print 'Usage:\n\n	' + sys.argv[0] + ' <-e/-d/-c> <file>\n'
	print 'Explain:\n'
	print '\t\"-e\" means encrypt the file'
	print '\t\"-d\" means decrypt the file'
	print '\t\"-c\" means compile the file\n'


def encrypt(conffile):
	cf = ConfigParser.ConfigParser()
	cf.read(conffile)
	for section in cf.sections():
		if section != 'global':
			for option in cf.options(section):
				context = cf.get(section,option)
				handler = base64.encodestring(base64.encodestring(base64.encodestring(base64.encodestring(context))))
				cf.set(section,option,handler)
	cf.write(open(conffile,"w"))
	

def decrypt(conffile):
	cf = ConfigParser.ConfigParser()
	cf.read(conffile)
	for section in cf.sections():
		if section != 'global':
			for option in cf.options(section):
				context = cf.get(section,option)
				handler = base64.decodestring(base64.decodestring(base64.decodestring(base64.decodestring(context))))
				cf.set(section,option,handler)
	cf.write(open(conffile,"w"))


def compile(pyfile):
	command = 'cython ' + pyfile
	(status, output) = commands.getstatusoutput(command)
	if status != 0:
		print output
		return False

	command = 'echo ' + pyfile + '|awk -F \'.\' \'{print $1}\''
	(status, output) = commands.getstatusoutput(command)
	if status != 0:
		print output
		return False
	else:
		cfile = output + '.c'
		sofile = output + '.so'

	command = 'gcc -o ' + sofile + ' -shared -fPIC -I /usr/include/python2.6 -l python2.6 ' + cfile 
	(status, output) = commands.getstatusoutput(command)
	if status != 0:
		print output
		return False
	else:
		return True


#get inputer
try:
	operation = sys.argv[1]
	targetfile = sys.argv[2]
except:
	usage()
	exit(1)


#handle the task
if operation == '-e':
	encrypt(targetfile)
	exit(0)
elif operation == '-d':
	decrypt(targetfile)
	exit(0)
elif operation == '-c':
	if compile(targetfile):
		print 'compile success'
		exit(0)
	else:
		print 'compile failed'
		exit(3)
else:
	usage()
	exit(2)
