import CRFPP
import sys,pprint,re,string
from Crex.crfpp_wrap import CRF_classifier
from partitioner import *
from random import *
	
def read_instances(inp_text):
	out=[]
	comment=re.compile(r'#.*?')
	for i in inp_text.split("\n\n"):
		inst=[]
		for j in i.split("\n"):
			if(not comment.match(j)):
				inst.append(j.split("\t"))
		if(inst):
			out.append(inst)
	return out
	
def read_IOB_file(file):
	# instances is a list of lists
	instances=[]
	inp_text = open(file,'r').read()
	comment=re.compile(r'#.*?')
	for n,i in enumerate(inp_text.split("\n\n")):
		# each instance is a list of tuples: [0] id, [1] token, [2] tag
		instance=[]
		for j in i.split("\n"):
			if(not comment.match(j)):
				t= j.split("\t")
				temp=(n+1,t[0],t[1]) 
				instance.append(temp)
		if(instance):
			instances.append(instance)
	return instances
	
def instance_contains_label(instance,neg_label="O"):
	temp=[]
	for token in instance:
		temp.append(neg_label in [tag for i,tag in enumerate(token) if(i==len(token)-1)])
	return True in temp
	
def token_tostring(token):
	string=""
	for count,t in enumerate(token):
			if(count<len(token)-1):
				string+="%s\t"%t
			else:
				string+="%s"%t
	return string
	
def filter_IOB(instances,tag_name):
	"""docstring for filter_IOB"""
	out=[]
	res=[]
	temp = []
	count = 0
	for instance in instances:
		temp = []
		open = False
		for i in instance:
				#print "%s:%s"%(i[1],i[2])
				if(i[2]=='B-%s'%tag_name):
					temp.append(i[1])
					open = True
				elif(i[2]=='I-%s'%tag_name):
					if(open):
						temp.append(i[1])
				elif(i[2]=='O'):
					if(open):
						out.append(temp)
						temp = []
						open = False
					else:
						pass
		if(len(temp) > 0 and open):
			out.append(temp)
	for r in out:
		res.append(' '.join(r))	
	return res

def instance_tostring(instance):
	string=""
	for count,t in enumerate(instance):
			if(count!=len(t)):
				string+="%s "%t[0]
			else:
				string+="%s"%t[0]
	return string
	
def result_to_string(result):
	"""
	Tranform the result to a string.
	"""
	out=''
	for i,t in enumerate(result):
		out+=t['token']+"/"+t['label']
		if(i<len(result)-1):
			out+=" "
	return out

def eval_results_to_HTML(results,labels=[]):
	"""
	Tranform the result to a string.
	"""
	out="<html><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/> <style type=\"text/css\">div.result{padding:5px}span.token_B-CRF,span.tp{font-weight:bold} span.fn{color:red} span.fp{color:orange}</style></head><body>"
	for n,r in enumerate(results):
		out+="<div class=\"result\">[%s] "%str(n+1)
		for i,t in enumerate(r):
			value=""
			if(t['gt_label']==t['label']):
				if(t['gt_label']=="O"):
				   value='tn'
				else:
				   value='tp'
			else:
				if(t['gt_label']=="O"):
				   value='fp'
				else:
				   value='fn'
			error="%s -&gt; %s"%(t['gt_label'],t['label'])
			out+="<span title=\"%s\" class=\"%s\">%s</span>"%(error,value,t['token'])
			if(i<len(r)-1):
				out+=" "
		out+="</div>"
	out+="</body></html>"
	return out
	
def results_to_HTML(results,labels=[]):
	"""
	Tranform the result to a string.
	"""
	#out="<html><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/> <style type=\"text/css\">div.result{padding:5px}span.token_B-CRF,span.tp{font-weight:bold} span.fn{color:red} span.fp{color:orange}</style></head><body>"
	out="<div class=\"results\">"
	for n,r in enumerate(results):
		out+="<span title=\"%s\">%s</span>"%(str(r['label']),str(r['token']))
	out+="</div></body>"
	#out+="</html>"
	return out
	
def parse_jstordfr_XML(inp):
	"""
	Describe what the function does.
	"""
	out=[]
	xml_exp=re.compile(r'(?:<citation>)(.*?)(?:</citation>)')
	cdata_exp=re.compile(r'(?:<!\[CDATA\[)(.*?)(\]\]>)')
	if(xml_exp.search(inp) is not None):
		res2=xml_exp.findall(inp)
		for item in res2:
			res1=cdata_exp.match(item)
			out.append(res1.groups()[0])
	return out

def tag_IOB_file(train_file_name,to_tag_file_name):
	"""
	Takes as input a IOB file and tags it according to a given CRF model
	"""
	dir="data/"
	path,fn = os.path.split(train_file_name)
	out=open(dir+fn+'.train','w').write(prepare_for_training(train_file_name))
	train_fname=dir+fn+'.train'
	model_fname=dir+fn+'.mdl'
	train_crfpp("data/crex.tpl",train_fname,model_fname)
	cl=CRF_classifier(model_fname)
	instances=read_instances(prepare_for_testing(to_tag_file_name))
	for i in instances:
		tokens=[token_tostring(t) for t in i]
		out=""
		for r in cl.classify(tokens):
			out+="%s\t%s\n"%(r['token'],r['label'])
		print "%s"%out
	logger.info('Tagged %i instances'%len(instances))
	return

def concat(strings,concat_string,last_char=None):
	"""
	Utility function to concatenate strings.
	"""
	out=""
	count=0
	for s in strings:
		out+=str(s)
		count+=1
		if(count<len(strings)):
			out+=concat_string
		if(not count<len(strings) and last_char is not None):
			out+=last_char
	return out

def prepare_for_tagging(file_name):
	"""

	"""
	inp=open(file_name).read()
	prolog="""
# File generated from %s
# The tag to be used to mark up Canonical References are: B-CRF, I-CRF and O (according to the
# classical IOB format for NER)
	"""%(file_name)
	out=""
	out+=prolog
	for i in parse_jstordfr_XML(inp):
		out+=("\n# Original line: %s\n"%i)
		for t in i.split(' '):
			out+="%s\tO\n"%t
		out+="\n"
	return out
		

def main():
	insts = read_IOB_file(sys.argv[1])
	tag_name = 'CRF'
	print "The file contains %i instances"%len(insts)
	res=filter_IOB(insts,tag_name)
	print "%i of them have tag %s"%(len(res),tag_name)
	for i in res:
		print i
		print re.sub(r'[^\w]','',i)
	
		
if __name__ == "__main__":
    main()