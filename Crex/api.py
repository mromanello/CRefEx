#!/usr/bin/python

import xmlrpclib,sys,json
import cgi
import cgitb; cgitb.enable()
sys.path.insert(0, "/56k/phd/code/python_crex/")
from Crex.Utils.IO import *
s = xmlrpclib.ServerProxy('http://127.0.0.1/~56k/cgi-bin/crex_xmlrpc_service.py')


form = cgi.FieldStorage()
inp = form.getvalue("in", None)
out = form.getvalue("out", None)
api = form.getvalue("api", None)

def print_docu():
	"""docstring for print_docu"""
	content="""
	<h1>CRefEx API documentation v%s</h1>
	<table border="1" cellspacing="0" cellpadding="10"> 
        <tr> 
            <th>key</th> 
            <th>allowed values</th> 
            <th>description</th> 
        </tr> 
        <tr> 
            <td> 
                <code>input_type</code> 
            </td> 
            <td>
				<ul>
					<li><code>jstor/xml</code></li>
					<li><code>text</code></li>
					<li><code>onepline</code></li>
				</ul>
            </td> 
            <td> 
                The default value is <code>text</code>. If the value of this property is <code>jstor/xml</code> an XML doc in the format specified by JSTOR is expected.
            </td> 
        </tr> 
		<tr> 
            <td> 
                <code>lang</code> 
            </td> 
            <td>
				<ul>
					<code>en</code>
				</ul>
            </td> 
            <td> 
                TBD
            </td> 
        </tr>
    </table>
	"""%s.version()
	print content

if(api == "doc"):
	print "Content-type: text/html"
	print
	print_docu()

if(inp is not None):
	res = s.test([inp.split(" ")])
	if(out is not None):
		if(out == "xml"):
			print "Content-type: text/xml"
			print
			print """%s""" %verbose_to_XML(res['verbose'])
		elif(out == "json"):
			print "Content-type: text/javascript"
			print
			print """%s""" %str(json.dumps(res['verbose']))
		elif(out == "html"):
			print "Content-type: text/html"
			print
			print """%s""" %str(res['verbose'])