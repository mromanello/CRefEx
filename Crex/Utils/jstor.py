import os,sys
from lxml import etree

def read_jstor_rdf_catalog(file_path):
	print file_path
	file=open(file_path)
	fcont=file.read()
	file.close()
	res = etree.fromstring(fcont)
	children = list(res)
	res = []
	for el in children:
		el_children = list(el)
		dcns = "http://purl.org/dc/elements/1.1/"
		el_res = {}
		for n in el.getchildren():
			if(n.tag=="{%s}identifier"%dcns):
				print "%s: %s"%(n.tag,n.text)
				el_res["urn"]=n.text
			elif(n.tag=="{%s}title"%dcns):
				print "%s: %s"%(n.tag,n.text)
				el_res["title"]=n.text
			elif(n.tag=="{%s}identifer"%dcns):
				print "%s: %s"%(n.tag,n.text)
				el_res["id"]=n.text
			elif(n.tag=="{%s}relation"%dcns):
				print "%s: %s"%(n.tag,n.text)
				el_res["relation"]=n.text
			elif(n.tag=="{%s}creator"%dcns):
				print "%s: %s"%(n.tag,n.text)
				el_res["author"]=n.text
			elif(n.tag=="{%s}publisher"%dcns):
				print "%s: %s"%(n.tag,n.text)
				el_res["publisher"]=n.text
			elif(n.tag=="{%s}date"%dcns):
				print "%s: %s"%(n.tag,n.text)
				el_res["date"]=n.text
			elif(n.tag=="{%s}type"%dcns):
				print "%s: %s"%(n.tag,n.text)
				el_res["type"]=n.text
	
def read_jstor_csv_catalog(file_path):
	import csv
	indexes = {'journal':{},'date':{},'type':{}}
	res = list(csv.DictReader(open(file_path,'rb')))
	for n in range(len(res)):
		i=res[n]
		title = i['JOURNALTITLE']
		if(indexes['journal'].has_key(title)):
			indexes['journal'][title].append(n)
		else:
			indexes['journal'][title] = []
			indexes['journal'][title].append(n)
			print len(indexes['journal'][title]doc)
	print indexes

if __name__ == "__main__":
	if(len (sys.argv)>1):
		#res = read_jstor_rdf_catalog(sys.argv[1])
		read_jstor_csv_catalog(sys.argv[1])
	else:
		"Usage: <jstor_dataset_path>"