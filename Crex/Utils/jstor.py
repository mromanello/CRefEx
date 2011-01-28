import os,sys,pprint

def read_jstor_rdf_catalog(file_path):
	from lxml import etree
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
	import csv,re
	indexes = {'JOURNALTITLE':{},'PUBDATE':{},'TYPE':{}}
	ids=[]
	res = list(csv.DictReader(open(file_path,'rb')))
	print len(res)
	for n in range(len(res)):
		i=res[n]
		ids.append(i['ID'])
		#keys =[ 'JOURNALTITLE','TYPE','PUBDATE']
		for key in indexes.keys():
			if(key=="PUBDATE"):
				r=re.compile(r'[A-Za-z0-9\-,.\s]+ \n?([0-9]{4})')
				r2=re.compile(r'([0-9]{4}/[0-9]{4})')
				if(r.match(i[key])):
					i[key] = r.search(i[key]).group(1)
				elif(r2.match(i[key])):
					i[key] = r2.search(i[key]).group(1)
			if(indexes[key].has_key(i[key])):
				indexes[key][i[key]].append(i['ID'])
			else:
				indexes[key][i[key]] = []
				indexes[key][i[key]].append(i['ID'])
	#pprint.pprint(ids)
	for i in indexes:
		for n in indexes[i].keys():
			print "%s: count=%i"%(n,len(indexes[i][n]))
	return ids,indexes

if __name__ == "__main__":
	if(len (sys.argv)>1):
		#res = read_jstor_rdf_catalog(sys.argv[1])
		res=[]
		res = read_jstor_csv_catalog(sys.argv[1])
		ids = res[0]
	else:
		print "Usage: <jstor_dataset_path>"
