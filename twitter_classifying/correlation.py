from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.svm import SVC
import cPickle
import numpy as np
import scipy
from sklearn.metrics import roc_curve, auc


t1 = cPickle.load(open('new_tf2.pickle','rb'))
SVC = cPickle.load(open('SVC2.pickle','rb'))
vect1 = cPickle.load(open('new_vect2.pickle','rb'))

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
	'''
	if (parts[2] == "positive"):
		t_class_num.append("positive")
	else:
		t_class_num.append(0)
	'''
	t_class.append(parts[2])

v1 = vect1.transform(t_txt)
v2 = t1.transform(v1)

rv1 = vect2.transform(t_txt)
rv2 = t2.transform(rv1)

svr_results = LSVR.predict(rv2)
probs = SVC.predict_proba(v2)
svc_r = []
for p in probs:
	svc_r.append(p[1])

def combine_and_rank(r=[],t=[]):
	combined = []
	index = 0
	for x in r:
		tup = (x, t[index])
		index+=1   
		combined.append(tup)

	combined.sort(key = lambda tup: tup[0])

	index = 1
	rank1 = []
	for c in combined:
		tup = (c[0], index, c[1])
		index += 1
		rank1.append(tup)

	rank1.sort(key = lambda tup: tup[2])

	index = 1
	rank2 = []
	for r1 in rank1:
		tup = (r1[0],r1[1],r1[2],index)
		index +=1
		rank2.append(tup)

	return rank2

ranked = combine_and_rank(svc_r,svr_results)

rarr = []
a = range(1,2501)
for i in range(0,1000):
	#r = range(1,2501)
	a = np.random.permutation(a)
	rarr.append(a)

#sum of squares of difference in ranks
def rank_correlation(r = []):
	s = 0
	for rank in r:
		dif = rank[1]-rank[3]
		sq = dif * dif
		s += sq 
	return s

#print rank_correlation(ranked)
#print rank_correlation(rand_ranked)

#spearman's foot rule
def spearman_corr(r = []):
	s = 0.
	for rank in r:
		dif = abs(rank[1]-rank[3])
		s += dif
	n = 6.0*s
	d = len(r)*(len(r)*len(r) - 1.0)
	return (1. - n/d)

#print spearman_corr(ranked)
#print spearman_corr(rand_ranked)

#kendall's tau coefficient
def kendall_tau(r = []):
	l1 = []
	l2 = []
	for rank in r:
		l1.append(rank[1])
		l2.append(rank[3])
	count = 0
	i = 0
	while(i < len(r)):
		l1r1 = l1[i]
		l2r1 = l2[i]
		j = i + 1
		while (j < len(r)):
			l1r2 = l1[j]
			l2r2 = l2[j]
			if (l1r1<l1r2 and l2r1 >l2r2):
				count += 1
			elif (l1r1>l1r2 and l2r1 < l2r2):
				count += 1
			j += 1
		i += 1
	d = len(r)*(len(r)-1)/2.0
	return count/d
'''
#adapted example from Wikipedia to test kendall-tau function
height = [1,2,3,4,5]
weight = [3,4,1,2,5]
index = 0
test = []
for h in height:
	tup = (0,h,0,weight[index])
	index += 1
	test.append(tup)
print kendall_tau(test)
'''

print rank_correlation(ranked)
print spearman_corr(ranked)
print kendall_tau(ranked)

rank_range = []
sp_range = []
kt_range = []
index = 0
for r in rarr:
	rand_ranked = combine_and_rank(svc_r,r)
	rank_range.append(rank_correlation(rand_ranked))
	sp_range.append(spearman_corr(rand_ranked))
	if index < 100:
		kt_range.append(kendall_tau(rand_ranked))
	index += 1


rank_min = min(rank_range)
sp_min = min(sp_range)
kt_min = min(kt_range)

rank_max = max(rank_range)
sp_max = max(sp_range)
kt_max = max(kt_range)

print "Sum of Squares: " + str(rank_min) + " - " + str(rank_max)
print "Spearman's: " + str(sp_min) + " - " + str(sp_max)
print "Kendall-Tau: " + str(kt_min) + " - " + str(kt_max)









