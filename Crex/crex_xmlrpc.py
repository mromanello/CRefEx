#!/usr/bin/python
# -*- coding: UTF-8 -*-

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from crex import CrexService
import sys

LHOST="localhost"
HOST="137.73.122.221"
PORT=8001
PATH="/rpc/crex"

class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = (PATH)

server = SimpleXMLRPCServer((LHOST, PORT),requestHandler=RequestHandler)
server.register_introspection_functions()
server.register_instance(CrexService())
server.serve_forever()