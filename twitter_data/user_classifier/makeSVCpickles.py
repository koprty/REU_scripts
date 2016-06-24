import sqlite3
import numpy as np
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from random import shuffle
import cPickle
import time

############## Retrieve data from DataSet ##############
conn = sqlite3.connect("../tweets.sqlite")
cursor = conn.cursor()
#query = "select screename, Description from users where category = 'individuals';"
query = "select Description from users where category = 'individuals';"
cursor.execute(query)
indi_result = cursor.fetchall()
conn.close()


conn2 = sqlite3.connect("../tweets.sqlite")
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
########### Get data from DataSet

############# Vectorize the Training Data Set ###############
#COUNT VECTORIZER has more accurate results
vectorizer = CountVectorizer(stop_words="english",lowercase=True)
#vectorizer = TfidfVectorizer(stop_words="english",lowercase=True)

#corpus = individuals[-1*len(others):] + others[:]
#Y_train = len(others)*["positive"] + len(others)*["negative"]

corpus = individuals[-300:] + others[-300:]
X_train = vectorizer.fit_transform(corpus)
Y_train = 300*[1] + 300*[]

f = open("count_users.pickle", "wb")
cPickle.dump(vectorizer, f)
f.close()
print "count_vectorizer was made :D"

############### Make SVC pickle ################
clf = SVC(kernel='linear',probability = True)
#clf = SVC ()
#clf = LogisticRegression()
clf.fit(X_train,Y_train)
g = open("SVC_users.pickle", "wb")
cPickle.dump(clf, g)
g.close()
print clf.classes_

############# Testing the accuracy of pickle ##############

test_descripts = individuals[:-300] + others[:-300]
#test_descripts = individuals[:] + others[:] 
X_test = vectorizer.transform(test_descripts)

Y_test = (len(individuals)-300) *[1] + (len(others)-300) *[0]
#Y_test = (len(individuals) *["positive"]) + (len(others) *["negative"])
np.set_printoptions(threshold='nan')

#re =  clf.predict_log_proba(X_test)
#re = clf.predict(X_test)
re =  clf.predict_proba(X_test)
sc = clf.score(X_test, Y_test)
#re = clf.sparsify()
'''
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
'''

