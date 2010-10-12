#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xmlrpclib,pprint
import simplejson as json
from nltk import regexp_tokenize
from Crex.Utils.IO import *
from Crex.crex import *
pp = pprint.PrettyPrinter(indent=5)

LHOST="localhost"
HOST="137.73.122.221"
PORT=8001
PATH="/rpc/crex"
# connection to the CREX server
print("%s:%i%s"%(LHOST,PORT,PATH))
file = open('/56k/DEV/test_json.js','w')
s = xmlrpclib.ServerProxy("http://%s:%i%s"%(LHOST,PORT,PATH))
# printing a test
s1="""this is a string Hom. Il. 1.125"""
s2="""Eschilo interprete di se stesso (Ar. Ran. 1126s. e 1138-1150)"""
s3="""Thucydides' account of the Spartan-Athenian conflict at Pylos (4, 8, 3-9) contains topographical inaccuracies that demonstrate that the historian had not visited the site. Emendation is unwarranted, in part because Thucydides' erroneous account of the topography harmonizes with his account of the Spartans' plan to block the entrances to Navarino Bay. The actual topography, however, makes the reported plan impossible. The Spartans apparently intended to fight a naumachia with the Athenians inside the bay and therefore stationed hoplites on the island of Sphakteria. Thucydides' misconceptions stem from his failure to visit the site and his reliance on tendentious Peloponnesian sources"""
s4="""Lendon, Jon E. -Xenophon and the alternative to realist foreign policy : Cyropaedia 3.1.14-31. JHS 2006 126 : 82-98. The dialogue Xenophon stages at Cyr. 3, 1, 14-31 constitutes a sophisticated theoretical treatment of Greek foreign-policy motivations and methods, and offers an implicit rebuttal to Thucydides' realist theses about foreign relations. Comparison of this passage to the historians and Attic orators suggests that Xenophon was attempting to systematize conventional Greek conceptions : the resulting theoretical system, in which hubris is regarded as the main obstacle to interstate quiet, and control of other states depends not only upon fear but upon superior excellence and the management of reciprocity, is likely to approach closer than Thucydides' theses to mainstream classical Greek thinking about foreign relations."""
#test="%s %s"%(s3,s4)

res=s.test([s2.split(" "),s4.split(" ")])

pprint.pprint(res)
	
#sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
#print "\n$".join(sent_detector.tokenize(test.strip(), realign_boundaries=False))
#print "\n\n".join(regexp_tokenize(test, pattern=r'\.(\s+|$)', gaps=True))
	

#pp.pprint(s.version())
#print s.system.listMethods()