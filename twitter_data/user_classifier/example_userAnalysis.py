'''
example of using SVC and vectorizer without pickle files
Has some Log Regression in the comments
'''

import sqlite3
import numpy as np
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, auc, roc_auc_score
import matplotlib.pyplot as plt
import time
from random import shuffle as shuffie
from sklearn.utils import shuffle

conn = sqlite3.connect("../tweets.sqlite")
cursor = conn.cursor()
#query = "select screename, Description from users where category = 'individuals';"
query = "select Description, Screename from users where category = 'individuals';"
cursor.execute(query)
indi_result = cursor.fetchall()
conn.close()


conn2 = sqlite3.connect("../tweets.sqlite")
cursor = conn2.cursor()
#query = "select screename, Description from users where not category = 'individuals';"
query = "select Description, Screename from users where not category = 'individuals';"
cursor.execute(query)
notindi_result = cursor.fetchall()
conn2.close()

print len(indi_result) #2324
print len(notindi_result) #336

shuffie(indi_result)
shuffie(notindi_result)

#values = []
individuals = [] 
for ind in indi_result:
	individuals.append(ind[0])
#	values.append(1)
others = [] 
for o in notindi_result:
	others.append(o[0])
#	values.append(0)



#COUNT VECTORIZER has more accurate results
vectorizer = CountVectorizer(stop_words="english",lowercase=True)
vectorizer = TfidfVectorizer(stop_words="english",lowercase=True)
corpus = individuals[-300:] + others[-300:]
X_train = vectorizer.fit_transform(corpus)
#Y_train = (len(individuals)-100) *["positive"] + (len(others)-100) *["negative"]
Y_train = 300*["positive"] + 300*["negative"]
Y_train = 300*[1] + 300*[0]

#X_train, Y_train = shuffle(X_train, Y_train)

'''
vectorizer = HashingVectorizer(stop_words='english', non_negative=True,
                                   n_features=opts.n_features)
X_train = vectorizer.transform(data_train.data)
'''
clf = SVC(kernel='linear',probability = True)
#clf = SVC ()
#clf = LogisticRegression()
clf.fit(X_train,Y_train)

##### Testing Data #######
test_descripts = individuals[:-300] + others[:-300]
#test_descripts = np.random.permutation(test_descripts)
X_test = vectorizer.transform(test_descripts)

Y_test = (len(individuals)-300) *["positive"] + (len(others)-300) *["negative"]
Y_test = (len(individuals)-300) *[1] + (len(others)-300) *[0]
#Y_test = 300*["positive"] + 300*["negative"]

np.set_printoptions(threshold='nan')

#re =  clf.predict_log_proba(X_test)
re =  clf.predict_proba(X_test)
y = clf.predict(X_test)


#using roc instead of score
######################### ROC CURVE #####################


######### Just counting some numbers ########




scores = [x[1] for x in list(re)]
neg_scores = [x[0] for x in list(re)]


FPR, TPR, thresholds = roc_curve( Y_test, scores, pos_label=1)
FFR, TFR, thresholds = roc_curve( Y_test, scores, pos_label=0)
roc_auc = auc(FPR, TPR)
#print FPR
#print TPR
#print thresholds
print roc_auc
print roc_auc_score(Y_test, scores) 
exit()
print "neg " + str(roc_auc_score(Y_test, neg_scores))
roc_aucN= auc(FFR, TFR)
print roc_aucN
#print FPR

c=0
ind = 0
while ind < len(list(re)):
	re = list(re)
	if Y_test[ind] == 0 and float(re[ind][1] - re[ind][0]) <= 0.1651529601:
		#0.38351529601
		y[ind] = 0
		print re[ind]
		print re[ind][1] - re[ind][0], "__"
	#if (re[ind][0] > re[ind][1] and (Y_test[ind] !=0) ):
	if (y[ind] == 0 and (Y_test[ind] !=0) ):
		print "false negative: ", str(re[ind]) + "   ", y[ind], "     ", Y_test[ind], "   " + str(test_descripts[ind])
		print  list(re)[ind][0] - list(re)[ind][1]
		print 
		#c+=1
	#elif (re[ind][0] <= re[ind][1] and (Y_test[ind] ==0) ):
	elif (y[ind] == 1 and (Y_test[ind] ==0) ):
		print "false positive: ",str(re[ind]) + "   ", y[ind], "     ", Y_test[ind], "   " + str(test_descripts[ind])
		print  list(re)[ind][1] - list(re)[ind][0]
		print
		c+=1
	ind+=1


#############################

print c
print c*1.0/2060
print (2060-c*1.0)/2060

L = []
i = 0
while i < len(re):
	#L.append ( (re[i], Y_test[i]))
	L.append(    (list(re[i]), y[i],  Y_test[i]))
	i+=1


z=0
p=0
wrong = 0
index = 0
while index < len(L):
	x = L[index]
	#expected = "positive"
	expected = 1
	if y[index] == 0:
		#expected = "negative"
		expected = 0
		z+=1
	#if x[0][0] >= x[0][1]:
	else:
		p += 1

	if expected != int(x[1]) or expected != int(x[2]):
		wrong+=1
	index+=1


print "negatives = %d"%z
print "positives = %d"%p
print "wrong = %d"%wrong
print len(re)
#######################################

sc = clf.score(X_test, Y_test)
#re = clf.sparsify()
print "Score: " + str(sc)
print clf

#print clf.classes_


#### let's plot some stuff ####
plt.figure()
plt.plot(FPR, TPR, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot(FFR, TFR, label='ROC False curve (area = %0.2f)' % roc_aucN)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])


plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
#plt.show()
