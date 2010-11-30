#!/usr/bin/python
# -*- coding: UTF-8 -*-

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from core import CrexService
import sys

		
def main():
	LHOST="localhost"
	HOST="137.73.122.221"
	PORT=8001
	PATH="/rpc/crex"
	CRefEx_XMLRPC_server(LHOST,PORT,PATH)

if __name__ == "__main__":
	main()
