#!/usr/bin/python
# -*- coding: UTF-8 -*-

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from core import CrexService
import sys

class CRefEx_XMLRPC_server:
	"""docstring for CRefEx_XMLRPC_server"""
	class RequestHandler(SimpleXMLRPCRequestHandler):
		PATH=["/rpc/crex"]
		rpc_paths = PATH
		
	def __init__(self, host="localhost",port=8001,path="/rpc/crex"):
		LHOST="localhost"
		HOST="137.73.122.221"
		PORT=8001
		PATH="/rpc/crex"
		try:
			server = SimpleXMLRPCServer((host, port),requestHandler=CRefEx_XMLRPC_server.RequestHandler)
			server.register_introspection_functions()
			server.register_instance(CrexService())
			server.serve_forever()
			print "Service started!"
		except Exception, e:
			raise e
			
def main():
	s = CRefEx_XMLRPC_server()
if __name__ == "__main__":
	main()