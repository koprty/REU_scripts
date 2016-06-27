from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.svm import SVC
import cPickle
import numpy as np
import scipy
<<<<<<< HEAD
from sklearn.metrics import roc_curve, auc
=======
from sklearn.metrics import roc_curve, auc, roc_auc_score
>>>>>>> 2adc7eaec182bde5f7847bb0e3f860d64ff50950

transformer = cPickle.load(open('new_tf2.pickle','rb'))
SVC = cPickle.load(open('SVC2.pickle','rb'))
vectorizer = cPickle.load(open('new_vect2.pickle','rb'))

t2 = cPickle.load(open("transformer.pickle", 'rb'))
LSVR = cPickle.load(open('LSVR.pickle','rb'))
vect2 = cPickle.load(open('vectorizer.pickle','rb'))


fname = "test_set_new_corrected.txt"
t = open(fname, "r")
data = t.read()
arr = data.split("\r")
t_txt = []
t_class_num = []
t_class = []
for line in arr:
	parts = line.split("\t")
	t_txt.append(parts[3])
	if (parts[2] == "positive"):
		t_class_num.append(1)
	else:
		t_class_num.append(0)
	t_class.append(parts[2])

v1 = vectorizer.transform(t_txt)
v2 = transformer.transform(v1)

rv1 = vect2.transform(t_txt)
rv2 = t2.transform(rv1)

svr_results = LSVR.predict(rv2)


results = SVC.predict(v2)
probs = SVC.predict_proba(v2)


'''
index = 0
for t in t_txt:
	print t 
	print "\t" + t_class[]
	print "\t" + str(results[index])
	index += 1

'''
max_svr = max(svr_results)
min_svr = min(svr_results)
dist = max_svr - min_svr

tweet_results = []
index = 0
for r in results:
	#normalized_svr = (svr_results[index]-min_svr)/dist
	#svr_results[index] = normalized_svr
	tup = (t_class[index], r, probs[index][1], svr_results[index], t_txt[index][0:18])
	index+=1   
	tweet_results.append(tup)


tweet_results.sort(key = lambda tup: tup[3])

print np.correlate(results,svr_results)
print scipy.stats.stats.pearsonr(results,svr_results)


'''
tweet_probs = []
index = 0
for p in probs:
	tup = (t_class[index],p[1])
	index+=1   
	tweet_probs.append(tup)

tweet_probs.sort(key = lambda tup: tup[1])
'''

#for tr in tweet_results:
	#print tr

<<<<<<< HEAD
print SVC.score(v2,t_class_num)
n_classes =  t_class.shape[1]
=======
#probs
scores = [x[1] for x in list(probs)]
>>>>>>> 2adc7eaec182bde5f7847bb0e3f860d64ff50950

print SVC.score(v2,t_class_num)
print roc_auc_score ( t_class_num,scores)

fpr = dict()
tpr = dict()
roc_auc = dict()
for i in range(n_classes):
    fpr[i], tpr[i], _ = roc_curve(y_test[:, i], y_score[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

# Compute micro-average ROC curve and ROC area
fpr["micro"], tpr["micro"], _ = roc_curve(y_test.ravel(), y_score.ravel())
roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])




def find_threshold(tr = [], desired_perc = 0, threshold = .66743001280481029):
	th = threshold + .001
	current = []
	for t in tr:
		if t[2] > th:
			current.append(t)
	pos = 0.
	total = 0.
	for c in current:
		if (c[0] == "positive"):
			pos += 1
		total += 1
	percent = pos/total
	if percent < desired_perc:
		find_threshold(current,desired_perc,th)
	else:
		print "Threshold for " +str(int(desired_perc*100)) + "% m-dab tweets: " + str(th)
		return th

find_threshold(tweet_results,.90)
find_threshold(tweet_results,.95)





#fout = open("results.txt", "w")
incorrect = 0.
total = 0.
for tr in tweet_results:
	if (tr[0] == "positive" and tr[3] < .49551773534676913):
		incorrect += 1
	if (tr[0] == "negative" and tr[3] >= .49551773534676913):
		incorrect += 1
	total += 1

error = incorrect / total
#print 1 - error 
#	fout.write(str(tr))
#	fout.write("\n")
##fout.close()
