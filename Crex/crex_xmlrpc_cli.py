#!/usr/bin/python

import sys,xmlrpclib

s = xmlrpclib.ServerProxy('http://127.0.0.1/~56k/cgi-bin/test_xml-rpc.py')
print s.system.listMethods()
for i in s.system.listMethods():
	print i+": "+s.system.methodHelp(i)
	print i+": "+s.system.methodSignature(i)
print s.version()