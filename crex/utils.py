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

def results_to_HTML(results):
	"""
	Tranform the result to a string.
	"""
	out="<html><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/> <style type=\"text/css\">div.result{padding:5px}span.token_B-CRF,span.token_I-CRF{font-weight:bold}</style></head><body>"
	for r in results:
		out+="<div class=\"result\">"
		for i,t in enumerate(r):
			out+="<span class=\"token_%s\">%s</span>"%(t['label'],t['token'])
			if(i<len(r)-1):
				out+=" "
		out+="</div>"
	out+="</body></html>"
	return out
		

def main():
	return
		
		
if __name__ == "__main__":
    main()