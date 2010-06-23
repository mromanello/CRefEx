import CRFPP
import sys,pprint,re
from crfpp_wrap import CRF_classifier
import partitioner
from partitioner import Partitioner
from crossvalidationdataconstructor import CrossValidationDataConstructor
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

def main():
	return
		
		
if __name__ == "__main__":
    main()
    #test_cross(range(0,1000))