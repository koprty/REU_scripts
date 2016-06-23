import sqlite3
import numpy as np
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import time
from random import shuffle

conn = sqlite3.connect("tweets.sqlite")
cursor = conn.cursor()
#query = "select screename, Description from users where category = 'individuals';"
query = "select Description from users where category = 'individuals';"
cursor.execute(query)
indi_result = cursor.fetchall()
conn.close()


conn2 = sqlite3.connect("tweets.sqlite")
cursor = conn2.cursor()
#query = "select screename, Description from users where not category = 'individuals';"
query = "select Description from users where not category = 'individuals';"
cursor.execute(query)
notindi_result = cursor.fetchall()
conn2.close()

print len(indi_result) #2324
print len(notindi_result) #336

#values = []
individuals = [] 
for ind in indi_result:
	individuals.append(ind[0])
#	values.append(1)
others = [] 
for o in notindi_result:
	others.append(o[0])
#	values.append(0)

shuffle(individuals)
shuffle(others)

#COUNT VECTORIZER has more accurate results
vectorizer = CountVectorizer(stop_words="english",lowercase=True)
#vectorizer = TfidfVectorizer(stop_words="english",lowercase=True)
corpus = individuals[-300:] + others[-300:]
X_train = vectorizer.fit_transform(corpus)
#Y_train = (len(individuals)-100) *["positive"] + (len(others)-100) *["negative"]
Y_train = 300*["positive"] + 300*["negative"]
'''
vectorizer = HashingVectorizer(stop_words='english', non_negative=True,
                                   n_features=opts.n_features)
X_train = vectorizer.transform(data_train.data)
'''
clf = SVC(probability = True)
#clf = SVC ()
#clf = LogisticRegression()
clf.fit(X_train,Y_train)


test_descripts = individuals[:-300] + others[:-300]
#test_descripts = np.random.permutation(test_descripts)
X_test = vectorizer.transform(test_descripts)

Y_test = (len(individuals)-300) *["positive"] + (len(others)-300) *["negative"]
#Y_test = 300*["positive"] + 300*["negative"]



np.set_printoptions(threshold='nan')

#re =  clf.predict_log_proba(X_test)
re =  clf.predict_proba(X_test)
#re = clf.predict(X_test)
sc = clf.score(X_test, Y_test)
#re = clf.sparsify()
print sc
print clf
#print re
#print re

L = []
i = 0
while i < len(re):
	#L.append ( (re[i], Y_test[i]))
	L.append(    (list(re[i]), Y_test[i]))
	i+=1
L.sort(key = lambda tuple: tuple[1])
#print L

z = 0
p=0
wrong = 0
for x in L:
	if x[0][0] > x[0][1]:
		z+=1
	else:
		p += 1
	expected = "positive"
	if x[0][0] > x[0][1]:
		expected = "negative"
	if expected != x[1]:
		wrong+=1
print 
print "negatives = %d"%z
print "positives = %d"%p
print "wrong = %d"%wrong
print
print clf.classes_
#print re


# Test 1:
'''
corpus = 300 individuals 300 non_negative

test_descripts = rest of dataset

score = 0..779126213592
'''

exit()
