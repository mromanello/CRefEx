import CRFPP
import sys,pprint,re
from crfpp_wrap import CRF_classifier
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
			error="%s -> %s"%(t['gt_label'],t['label'])
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
		

def main():
	return
		
		
if __name__ == "__main__":
    main()