"""
Creates a wrapper around the CRF++ implementation
"""

import CRFPP
import sys,logging,os
import pprint

logger = logging.getLogger('CRFPP_WRAP')

def train_crfpp(template_file,train_data_file,model_file):
		cmd="crf_learn -f 10 -t %s %s %s"%(template_file,train_data_file,model_file)
		os.popen(cmd).readlines()
		return

class CRF_classifier:
	def __init__(self,model_file,verb_level=2,best_out_n=2):
		logger = logging.getLogger('CRFPP')
		try:
			self.m,self.v,self.bn=model_file,verb_level,best_out_n
			self.tagger = CRFPP.Tagger("-m %s -v %i -n%i"%(model_file,verb_level,best_out_n))
			logger.info("CRFPP Tagger initialized with command %s"%("-m %s -v %i -n%i"%(self.m,self.v,self.bn)))
		except RuntimeError, e:
			print "RuntimeError: ", e,
			
	def classify(self,l_tokens):
		out=[]
		self.tagger.clear()
		for t in l_tokens:
			self.tagger.add(t)
		self.tagger.parse()
		size = self.tagger.size()
		xsize = self.tagger.xsize()
		ysize = self.tagger.ysize()
		
		for i in range(0, (size)):
		   res={}
		   feats=[]
		   for j in range(0, (xsize)):
			if(j==0):
				res['token']=self.tagger.x(i, j)
			else:
				feats.append(self.tagger.x(i, j))
			res['features']=feats
		   res['label']=self.tagger.y2(i)
		   res['probs']={}
		   for j in range(0, (ysize)):
			tag=self.tagger.yname(j)
			probs={}
			probs['prob']=self.tagger.prob(i,j)
			probs['alpha']=self.tagger.alpha(i, j)
			probs['beta']=self.tagger.beta(i, j)
			res['probs'][tag]=probs
		   out.append(res)
		return out
	
if __name__ == "__main__":
    # crf_learn -t /56k/phd/code/python/crfx.tpl /56k/phd/code/python/doc1.train /56k/phd/code/python/crfx.mdl
    train_crfpp("/56k/phd/code/python/crfx.tpl","/56k/phd/code/python/doc1.train","/56k/phd/code/python/eval/new.mdl")
			