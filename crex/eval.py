import sys,logging
from crex import *
from crfpp_wrap import *
from partitioner import *
from crossvalidationdataconstructor import *
from utils import *
import pprint

logger=logging.getLogger('EVAL')

EVAL_PATH="/home/ngs0554/eval/"
DATA_PATH="/home/ngs0554/crex_data/"

def eval(fname,n_folds):
	valid_res=[]
	try:
		instances=read_instances(prepare_for_testing(fname))
		pos_inst=[ins for ins in instances if not instance_contains_label(ins,'O')]
		neg_inst=[ins for ins in instances if instance_contains_label(ins,'O')]
		shuffle(neg_inst)
		max=0
		logger.debug('# of negative instances: %i'%len(neg_inst))
		logger.debug('# of positive instances: %i'%len(pos_inst))
		if(len(pos_inst)>len(neg_inst)):
			max=len(neg_inst)
		else:
			max=len(pos_inst)
		print("Toal instances: %i (Test set plus training set)"%(len(neg_inst)+len(pos_inst)))
		iterations_num=n_folds
		c = CrossValidationDataConstructor(pos_inst, neg_inst, numPartitions=iterations_num, randomize=False)
		dataSets_iterator = c.getDataSets()
		iterations=[]
		tot_acc=0.0
		tot_prec=0.0
		tot_fscore=0.0
		tot_rec=0.0
		html=""
		for x,iter in enumerate(dataSets_iterator):
			print "Iteration %i"%(x+1)
			train_set=[]
			test_set=[]
			for y,set in enumerate(iter):
				for n,group in enumerate(set):
					if(y==0):
						train_set+=group
					else:
						test_set+=group
			iterations.append((train_set,test_set))
			
			print"\tFirst 10 random instances of training (out of %i)"%len(train_set)
			shuffle(train_set)
			for n in range(0,10):
				print "\t\t%s"%instance_tostring(train_set[n])
			print"\t\t..."
			print"\tFirst 10 random instances of testing (out of %i)"%len(test_set)
			shuffle(test_set)
			for n in range(0,10):
				print "\t\t%s"%instance_tostring(test_set[n])
			print"\t\t..."
		logger.debug('# of instances in training set: %i'%len(train_set))
		logger.debug('# of instances in test set: %i'%len(test_set))
			
				
		for y,i in enumerate(iterations):
			out=""
			out2=""
			train=i[0]
			test=i[1]
			
			for c,ins in enumerate(train):
				if(c!=0):
					out+="\n"
				for z,t in enumerate(ins):
					out+=token_tostring(t)
					if(z<len(ins)-1):
						out+="\n"
				if(c<len(train)-1):
					out+="\n"
			for c,ins in enumerate(test):
				if(c!=0):
					out2+="\n"
				for z,t in enumerate(ins):
					out2+=token_tostring(t)
					if(z<len(ins)-1):
						out2+="\n"
				if(c<len(test)-1):
					out2+="\n"
			train_file="%sfold_%i.train"%(EVAL_PATH,y+1)
			test_file="%sfold_%i.test"%(EVAL_PATH,y+1)
			model_file="%sfold_%i.mdl"%(EVAL_PATH,y+1)
			file=open(train_file,"w").write(out)
			open(test_file,"w").write(out2)
			train_crfpp("%screx.tpl"%DATA_PATH,train_file,model_file)
			crf=CRF_classifier(model_file)
			errors=0
			fp=0
			tp=0
			fn=0
			tn=0
			prec=0.0
			acc=0.0
			tot_tokens=0
			results=[]
			print "Processing #Fold %i..."%(y+1)
			for ex in test:
				tokens=[]
				for t in ex: 
					tokens.append(token_tostring(t))
					tot_tokens+=1
				# classify the instance
				res=crf.classify(tokens)
				logger.debug(instance_tostring(ex))
				for i in range(0,len(tokens)):
					try:
						gt_label=tokens[i].split('\t')[len(tokens[i].split('\t'))-1]
						token=tokens[i].split('\t')[0]
						class_label=res[i]['label']
						alpha=res[i]['probs'][class_label]['alpha']
						beta=res[i]['probs'][class_label]['beta']
						p=res[i]['probs'][class_label]['prob']
						if(gt_label==class_label):
							if(gt_label=="O"):
								tn+=1
							else:
								tp+=1
						else:
							if(gt_label=="O"):
								fp+=1
							else:
								fn+=1
						logger.debug("%s -> GT_Label \"%s\" : Classified_Label \"%s\"\talpha: %f\tbeta: %f\tp: %f"%(token,gt_label,class_label,alpha,beta,p))
						try:
							assert (gt_label==class_label)
						except AssertionError:
							errors+=1
					except RuntimeError,e:
						print "Something went wrong"
				logger.debug(result_to_string(res))
				results.append(res)
			prec=tp/float(tp+fp)
			acc=(tp+tn)/float(tp+fp+tn+fn)
			rec=tp/float(tp+fn)
			fscore=2*((prec*rec)/float(prec+rec))
			tot_acc+=acc
			tot_prec+=prec
			tot_rec+=rec
			tot_fscore+=fscore
			logger.debug("%i Errors out of %i tokens (in %i testing instances)"%(errors,tot_tokens,len(test)))
			logger.debug("FOLD#%i: TP:%i\tFP:%i\tTN:%i\tFN:%i\tACC:%f\tPREC:%f\tRECALL:%f\tFSCORE:%f"%((y+1),tp,fp,tn,fn,acc,prec,rec,fscore))
			res={
				'accuracy':acc
				,'precision':prec
				,'recall':rec
				,'fscore':fscore
				,'true_pos':tp
				,'true_neg':tn
				,'false_pos':fp
				,'false_neg':fn
				,'test_set_size':0
				,'train_set_size':0
				}
			valid_res.append(res)
		print "Average fscore: %f"%(tot_fscore/float(iterations_num))
		print "Average accuracy: %f"%(tot_acc/float(iterations_num))
		print "Average precision: %f"%(tot_prec/float(iterations_num))
		print "Average recall: %f"%(tot_fscore/float(iterations_num))
		print "Output in HTML format written to output.html"
		open('output.html','w').write(results_to_HTML(results))
			
		
	except RuntimeError,e:
		"Not able to prepare %s for training!"%fname	

def run_example():
	DATA_DIR="/home/ngs0554/crex_data"
	#eval("data/test.txt",5)
	eval("%s/test.txt"%DATA_DIR,10)
	#eval("data/test.txt",20)

if __name__ == "__main__":
    main()
