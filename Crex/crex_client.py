#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xmlrpclib,pprint
import simplejson as json
from Crex import clients
from nltk import regexp_tokenize
from Crex.Utils.IO import *
from Crex.core import *
pp = pprint.PrettyPrinter(indent=5)

LHOST="localhost"
HOST="137.73.122.221"
PORT=8001
PATH="/rpc/crex"

s1=u"this is a string è Hom. Il. 1.125"
s2="""Eschilo interprete di se è stesso (Ar. Ran. 1126s. e 1138-1150)"""
s3=u"""Thucydides' account of the Spartan-Athenian conflict at Pylos (4, 8, 3-9) contains topographical inaccuracies that demonstrate that the historian had not visited the site. Emendation is unwarranted, in part because Thucydides' erroneous account of the topography harmonizes with his account of the Spartans' plan to block the entrances to Navarino Bay. The actual topography, however, makes the reported plan impossible. The Spartans apparently intended to fight a naumachia with the Athenians inside the bay and therefore stationed hoplites on the island of Sphakteria. Thucydides' misconceptions stem from his failure to visit the site and his reliance on tendentious Peloponnesian sources"""
s4=u"è Hom. Il. 1.125 Lendon, Jon E. -Xenophon and the alternative to realist foreign policy : Cyropaedia 3.1.14-31. JHS 2006 126 : 82-98. The dialogue Xenophon stages at Cyr. 3, 1, 14-31 constitutes a sophisticated theoretical treatment of Greek foreign-policy motivations and methods, and offers an implicit rebuttal to Thucydides' realist theses about foreign relations. Comparison of this passage to the historians and Attic orators suggests that Xenophon was attempting to systematize conventional Greek conceptions : the resulting theoretical system, in which hubris is regarded as the main obstacle to interstate quiet, and control of other states depends not only upon fear but upon superior excellence and the management of reciprocity, is likely to approach closer than Thucydides' theses to mainstream classical Greek thinking about foreign relations."
			
def main():
	"""docstring for main"""
	print("%s:%i%s"%(LHOST,PORT,PATH))
	cl = clients.CRefEx_XMLRPC_client(LHOST,PORT,PATH)
	b = xmlrpclib.Binary(s1.encode("utf-8"))
	b = xmlrpclib.Binary(s3.encode("utf-8"))
	print s2
	print cl.proxy.test_unicode(b,"json")
	
	
if __name__ == "__main__":
	main()