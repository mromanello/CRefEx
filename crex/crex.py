# author: 56k
import re,string
from crfpp_wrap import *
from utils import *

"""
Description
"""

__version__='1.0.0'

LOG_FILE="/56k/phd/code/python_crex/crfx.log"
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s - %(name)s - [%(levelname)s] %(message)s',filename=LOG_FILE,datefmt='%a, %d %b %Y %H:%M:%S',filemode='w')
logger = logging.getLogger('CREX')

pp = pprint.PrettyPrinter(indent=5)

# brackets
PAIRED_ROUND_BRACKETS=1
UNPAIRED_ROUND_BRACKETS=2
PAIRED_SQUARE_BRACKETS=3
UNPAIRED_SQUARE_BRACKETS=4
# case
MIXED_CAPS=5
ALL_CAPS=6
INIT_CAPS=7
ALL_LOWER=8
OTHERS=0
# punctuation
FINAL_DOT=10
CONTINUING_PUNCTUATION=11
STOPPING_PUNCTUATION=12
QUOTATION_MARK=13
HAS_HYPHEN=14
NO_PUNCTUATION=15
# number
YEAR=16
RANGE=17
DOT_SEPARATED_NUMBER=18
DOT_SEPARATED_PLUS_RANGE=19
NUMBER=20
ROMAN_NUMBER=21
NO_DIGITS=9
MIXED_ALPHANUM=22

feat_labels=['i']*30
# brackets
feat_labels[1]="PAIRED_ROUND_BRACKETS"
feat_labels[2]="UNPAIRED_ROUND_BRACKETS"
feat_labels[3]="PAIRED_SQUARE_BRACKETS"
feat_labels[4]="UNPAIRED_SQUARE_BRACKETS"
# case
feat_labels[5]="MIXED_CAPS"
feat_labels[6]="ALL_CAPS"
feat_labels[7]="INIT_CAPS"
feat_labels[8]="ALL_LOWER"
feat_labels[0]="OTHERS"
# punctuation
feat_labels[10]="FINAL_DOT"
feat_labels[11]="CONTINUING_PUNCTUATION"
feat_labels[12]="STOPPING_PUNCTUATION"
feat_labels[13]="QUOTATION_MARK"
feat_labels[14]="HAS_HYPHEN"
feat_labels[15]="NO_PUNCTUATION"
# number
feat_labels[16]="YEAR"
feat_labels[17]="RANGE"
feat_labels[18]="DOT_SEPARATED_NUMBER"
feat_labels[19]="DOT_SEPARATED_PLUS_RANGE"
feat_labels[20]="NUMBER"
feat_labels[21]="ROMAN_NUMBER"
feat_labels[9]="NO_DIGITS"
feat_labels[22]="MIXED_ALPHANUM"


# this class seems useless to me now!

class Classifier:
	def __init__(self,train_file_name):
		dir="/56k/phd/code/python_crex/data/"
		path,fn = os.path.split(train_file_name)
		train_fname=dir+fn+'.train'
		out=open(train_fname,'w').write(prepare_for_training(train_file_name))
		model_fname=dir+fn+'.mdl'
		train_crfpp(dir+"crex.tpl",train_fname,model_fname)
		self.crf_model=CRF_classifier(model_fname)
		return
	
	def classify(self,tagged_tokens_list):
		return self.crf_model.classify(tagged_tokens_list)


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
	
def prepare_for_training(file_name):
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
	return get_features(tokens,labels)
	
def prepare_for_testing(file_name):
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
	return get_features(tokens,labels)
	
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
	
def extract_bracket_feature(check_str):
	# define check regexps
	pair_sq_bra=re.compile(r'\[.*?\]')
	unpair_sq_bra=re.compile(r'[\[\]]')
	pair_rd_bra=re.compile(r'\(.*?\)')
	unpair_rd_bra=re.compile(r'[\(\)]')
	# execute checks
	if(pair_sq_bra.search(check_str)):
		return PAIRED_SQUARE_BRACKETS
	elif(unpair_sq_bra.search(check_str)):
		return UNPAIRED_SQUARE_BRACKETS
	elif(pair_rd_bra.search(check_str)):
		return PAIRED_ROUND_BRACKETS
	elif(unpair_rd_bra.search(check_str)):
		return UNPAIRED_ROUND_BRACKETS
	else:
		return OTHERS
	
def extract_case_feature(check_str):
	naked = re.sub('[%s]' % re.escape(string.punctuation), '', check_str)
	if(naked.isalpha()):
		if(naked.isupper()):
			return ALL_CAPS
		elif(naked.islower()):
			return ALL_LOWER
		elif(naked[0].isupper()):
			return INIT_CAPS
	
def extract_punctuation_feature(check_str):
	punct_exp=re.compile('[%s]' % re.escape(string.punctuation))
	# TODO
	final_dot=re.compile(r'.*?\.$')
	three_dots=re.compile(r'.*?\.\.\.$')
	cont_punct=re.compile(r'.*?[,;:]$')
	if(three_dots.match(check_str)):
		return
	elif(final_dot.match(check_str)):
		return FINAL_DOT
	elif(cont_punct.match(check_str)):
		return CONTINUING_PUNCTUATION
	
def extract_number_feature(check_str):
	naked = re.sub('[%s]' % re.escape(string.punctuation), '', check_str).lower()
	if(naked.isdigit()):
		return NUMBER
	elif(naked.isalpha()):
		return NO_DIGITS
	elif(naked.isalnum()):
		return MIXED_ALPHANUM
		
def extract_char_ngrams(string):
	size=4
	out=[]
	for i in range(0,4):
		i+=1
		out.append(string[0:i])
	for i in range(0,4):
		i+=1
		out.append(string[len(string)-i:])
	return out
	
def extract_string_features(check_str):
	"""
	Extract string length and text only string lowercase
	"""
	out = re.sub('[%s]' % re.escape(string.punctuation), '', check_str)
	if(not out==""):
		return [out.lower(),str(len(out))]
	else:
		return ["_",str(len(out))]
	
def extract_features(inp):
	out=[]
	feat_funcs=[extract_punctuation_feature,extract_bracket_feature,extract_case_feature,extract_number_feature]
	for f in feat_funcs:
		out.append(f(inp))
	return out

def get_features(tokens,labels,outp_label=True):
	out=""
	count=0
	for t in tokens:
		if(t!="\n"):
			logger.debug("Extracting features for token \"%s\""%t)
			tags=extract_features(t)
			tags+=extract_string_features(t)
			for i in range(len(tags)):	
				if(tags[i] is not None and type(tags[i]) is not type('string')):
					tags[i]=feat_labels[tags[i]]
				elif(type(tags[i]) is type('string')):
					tags[i]
				else:	
					tags[i]=feat_labels[0]
			if(outp_label):
				temp=concat([t]+tags+extract_char_ngrams(t)+[labels[count]],'\t')
				logger.debug(temp)
				out+=temp
			else:
				temp=concat([t]+tags+extract_char_ngrams(t),'\t')+"\n"
				logger.debug(temp)
				out+=temp
			count+=1
		else:
			out+=t	
	return out
	
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
    c=Classifier('data/test.txt')
    s1="this is a string Il. 1.125"
    s="Eschilo interprete di se stesso (Ar. Ran. 1126s. e 1138-1150)"
    temp=get_features(s.split(" "),[],False)
    temp=temp.split('\n')
    print result_to_HTML(c.classify([token_tostring(t.split('\t')) for t in temp]))
