# -*- coding: UTF-8 -*-
# author: 56k
import os,re,string,logging,pprint
from Crex.crfpp_wrap import *
from Crex.Utils.IO import *

"""
Description
"""

__version__='1.0.0'

LOG_FILE="/56k/phd/code/python_crex/crfx.log"
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - [%(levelname)s] %(message)s',filename=LOG_FILE,datefmt='%a, %d %b %Y %H:%M:%S',filemode='w')
logger = logging.getLogger('CREX')

pp = pprint.PrettyPrinter(indent=5)

class CrexService:
	def __init__(self):
		self.core = CRefEx()
		
	def test(self,arg):
		res = self.core.classify(arg)
		out=[]
		for inst in res:
			count = 0
			t = []
			for i in inst:
				count+=1
				temp=(count,i['token'],i['label'])
				t.append(temp)
			out.append(t)
		return {'short':out,'verbose':res}
		
		
	def version(self): 
		"""
		Return the version of CRefEx
		"""
		logger.debug("Printing version")
		return __version__
	
# this class should extend an abstract classifier˝	
class CRFPP_Classifier:
	def __init__(self,train_file_name):
		dir="/56k/phd/code/python_crex/data/"
		fe = FeatureExtractor()
		path,fn = os.path.split(train_file_name)
		train_fname=dir+fn+'.train'
		out=open(train_fname,'w').write(fe.prepare_for_training(train_file_name))
		model_fname=dir+fn+'.mdl'
		train_crfpp(dir+"crex.tpl",train_fname,model_fname)
		self.crf_model=CRF_classifier(model_fname)
		return
	
	def classify(self,tagged_tokens_list):
		return self.crf_model.classify(tagged_tokens_list)
		
class CRefEx:
	"""Canonical Reference Extractor"""
	def __init__(self,training_model=None,training_file=None):
		self.training_model=training_model
		self.classifier=None
		self._default_training_dir="/56k/phd/code/python_crex/data/"
		self._default_training_file="test.txt"
		self.fe = FeatureExtractor()
		
		if(training_model=="CRF" or training_model is None):
			if(training_file is not None):
				self.classifier=CRFPP_Classifier(training_file)
			else:
				# read the default value
				self.classifier=CRFPP_Classifier("%s%s"%(self._default_training_dir,self._default_training_file))
				
	def tokenize(self, arg):
		pass
				
	# actually it's a proxy method
	def classify(self, instances,input="text"):
		res = []
		for i in instances:
			features=self.fe.get_features(i,[],False).split('\n')
			res.append(self.classifier.classify([token_tostring(f.split('\t')) for f in features]))
		return res
		
class FeatureExtractor:
	"""
	...
	"""
	def __init__(self):
		# brackets
		self.PAIRED_ROUND_BRACKETS=1
		self.UNPAIRED_ROUND_BRACKETS=2
		self.PAIRED_SQUARE_BRACKETS=3
		self.UNPAIRED_SQUARE_BRACKETS=4
		# case
		self.MIXED_CAPS=5
		self.ALL_CAPS=6
		self.INIT_CAPS=7
		self.ALL_LOWER=8
		self.OTHERS=0
		# punctuation
		self.FINAL_DOT=10
		self.CONTINUING_PUNCTUATION=11
		self.STOPPING_PUNCTUATION=12
		self.QUOTATION_MARK=13
		self.HAS_HYPHEN=14
		self.NO_PUNCTUATION=15
		# number
		self.YEAR=16
		self.RANGE=17
		self.DOT_SEPARATED_NUMBER=18
		self.DOT_SEPARATED_PLUS_RANGE=19
		self.NUMBER=20
		self.ROMAN_NUMBER=21
		self.NO_DIGITS=9
		self.MIXED_ALPHANUM=22
		self.feat_labels=['i']*30
		# brackets
		self.feat_labels[1]="PAIRED_ROUND_BRACKETS"
		self.feat_labels[2]="UNPAIRED_ROUND_BRACKETS"
		self.feat_labels[3]="PAIRED_SQUARE_BRACKETS"
		self.feat_labels[4]="UNPAIRED_SQUARE_BRACKETS"
		# case
		self.feat_labels[5]="MIXED_CAPS"
		self.feat_labels[6]="ALL_CAPS"
		self.feat_labels[7]="INIT_CAPS"
		self.feat_labels[8]="ALL_LOWER"
		# punctuation
		self.feat_labels[10]="FINAL_DOT"
		self.feat_labels[11]="CONTINUING_PUNCTUATION"
		self.feat_labels[12]="STOPPING_PUNCTUATION"
		self.feat_labels[13]="QUOTATION_MARK"
		self.feat_labels[14]="HAS_HYPHEN"
		self.feat_labels[15]="NO_PUNCTUATION"
		# number
		self.feat_labels[9]="NO_DIGITS"
		self.feat_labels[16]="YEAR"
		self.feat_labels[17]="RANGE"
		self.feat_labels[18]="DOT_SEPARATED_NUMBER"
		self.feat_labels[19]="DOT_SEPARATED_PLUS_RANGE"
		self.feat_labels[20]="NUMBER"
		self.feat_labels[21]="ROMAN_NUMBER"
		self.feat_labels[22]="MIXED_ALPHANUM"
		self.feat_labels[0]="OTHERS"
		
	def extract_bracket_feature(self,check_str):
		# define check regexps
		pair_sq_bra=re.compile(r'\[.*?\]')
		unpair_sq_bra=re.compile(r'[\[\]]')
		pair_rd_bra=re.compile(r'\(.*?\)')
		unpair_rd_bra=re.compile(r'[\(\)]')
		# execute checks
		if(pair_sq_bra.search(check_str)):
			return self.PAIRED_SQUARE_BRACKETS
		elif(unpair_sq_bra.search(check_str)):
			return self.UNPAIRED_SQUARE_BRACKETS
		elif(pair_rd_bra.search(check_str)):
			return self.PAIRED_ROUND_BRACKETS
		elif(unpair_rd_bra.search(check_str)):
			return self.UNPAIRED_ROUND_BRACKETS
		else:
			return self.OTHERS
	def extract_case_feature(self,check_str):
		naked = re.sub('[%s]' % re.escape(string.punctuation), '', check_str)
		if(naked.isalpha()):
			if(naked.isupper()):
				return self.ALL_CAPS
			elif(naked.islower()):
				return self.ALL_LOWER
			elif(naked[0].isupper()):
				return self.INIT_CAPS
	def extract_punctuation_feature(self,check_str):
		punct_exp=re.compile('[%s]' % re.escape(string.punctuation))
		# TODO
		final_dot=re.compile(r'.*?\.$')
		three_dots=re.compile(r'.*?\.\.\.$')
		cont_punct=re.compile(r'.*?[,;:]$')
		if(three_dots.match(check_str)):
			return
		elif(final_dot.match(check_str)):
			return self.FINAL_DOT
		elif(cont_punct.match(check_str)):
			return self.CONTINUING_PUNCTUATION
	def extract_number_feature(self,check_str):
		naked = re.sub('[%s]' % re.escape(string.punctuation), '', check_str).lower()
		if(naked.isdigit()):
			return self.NUMBER
		elif(naked.isalpha()):
			return self.NO_DIGITS
		elif(naked.isalnum()):
			return self.MIXED_ALPHANUM
	def extract_char_ngrams(self,string):
		size=4
		out=[]
		for i in range(0,4):
			i+=1
			out.append(string[0:i])
		for i in range(0,4):
			i+=1
			out.append(string[len(string)-i:])
		return out
	
	def extract_string_features(self,check_str):
		"""
		Extract string length and text only string lowercase
		"""
		out = re.sub('[%s]' % re.escape(string.punctuation), '', check_str)
		if(not out==""):
			return [out.lower(),str(len(out))]
		else:
			return ["_",str(len(out))]
	
	def extract_features(self,inp):
		feature_set=[]
		feat_funcs=[self.extract_punctuation_feature,self.extract_bracket_feature,self.extract_case_feature,self.extract_number_feature]
		for f in feat_funcs:
			feature_set.append(f(inp))
		return feature_set
	def get_features(self,tokens,labels=[],outp_label=True):
		out=""
		count=0
		for t in tokens:
			if(t!="\n"):
				logger.debug("Extracting features for token \"%s\""%t)
				tags=self.extract_features(t)
				tags+=self.extract_string_features(t)
				for i in range(len(tags)):	
					if(tags[i] is not None and type(tags[i]) is not type('string')):
						tags[i]=self.feat_labels[tags[i]]
					elif(type(tags[i]) is type('string')):
						tags[i]
					else:	
						tags[i]=self.feat_labels[0]
				if(outp_label):
					temp=concat([t]+tags+self.extract_char_ngrams(t)+[labels[count]],'\t')
					logger.debug(temp)
					out+=temp
				else:
					temp=concat([t]+tags+self.extract_char_ngrams(t),'\t')+"\n"
					logger.debug(temp)
					out+=temp
				count+=1
			else:
				out+=t	
		return out		
	def prepare_for_training(self,file_name):
		file=open(file_name)
		out=""
		lines=file.readlines()
		tokens=[]
		labels=[]
		for l in lines:
			comment=re.compile(r'#.*?')
			if(l=="\n"):
				tokens.append(l)
			elif(not comment.match(l)):
				tokens.append(l.split('\t')[0])
				labels.append(l.split('\t')[1])	
		return self.get_features(tokens,labels)
	def prepare_for_testing(self,file_name):
		file=open(file_name)
		out=""
		lines=file.readlines()
		tokens=[]
		labels=[]
		for l in lines:
			comment=re.compile(r'#.*?')
			if(l=="\n"):
				tokens.append(l)
			elif(not comment.match(l)):
				tokens.append(l.split('\t')[0])
				labels.append(l.split('\t')[1])	
		return self.get_features(tokens,labels)
	
def main():
	fname=sys.argv[2]
	if(sys.argv[1]=="prep_train"):
		print prepare_for_training(fname)
		return
	elif(sys.argv[1]=="prep_tag"):
		print prepare_for_tagging(fname)
		return
	elif(sys.argv[1]=="prep_test"):
		print prepare_for_testing(fname)
		return
	elif(sys.argv[1]=="tag"):
		tag_IOB_file(fname,sys.argv[3])
		return

if __name__ == "__main__":
	#main()
	#exp("A")
	c=CRefEx()
	s1="this is a string Il. 1.125"
	s="Eschilo interprete di se stesso (Ar. Ran. 1126s. e 1138-1150)"
	#print result_to_HTML(c.classify([token_tostring(t.split('\t')) for t in temp]))
	pp.pprint(c.classify([s.split(" ")]))
