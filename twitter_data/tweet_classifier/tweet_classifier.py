from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.svm import SVC
import cPickle
import numpy as np
import scipy
import sqlite3
import re 
import string 
import datetime

conn = sqlite3.connect("../tweets.sqlite")
cursor = conn.cursor()
query= "select Tweet_Text, * from tweets9_Streaming;"
cursor.execute(query)
alltweets = cursor.fetchall()
conn.close()
print datetime.datetime.now()
names = [description[0] for description in cursor.description]




#these will be used to cleanse the tweets
removal_pattern1 = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
removal_pattern2 = re.compile('//t.co(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
removal_pattern3 = re.compile('\n')
removal_pattern4 = re.compile(' amp ')
removal_pattern5 = re.compile('@[\w]* ')

numtweets = len(alltweets)
list_tweets = []
i = 0
dd = 0

while dd < numtweets:
	d = list(alltweets[dd])
	s = d[0].encode('ascii','ignore')
	s = s+" "
	s = removal_pattern5.sub('', s)
	s = removal_pattern1.sub('', s)
	s = removal_pattern2.sub('', s)
	s = removal_pattern3.sub(' ', s)
	s = s.translate(None, string.punctuation)
	s = s.lower()
	s = removal_pattern4.sub('',s)

	d[0] = s
	d[8] = s

	list_tweets.append(d)

	dd+=1


#t_txt = [x[0] for x in alltweets]
t_txt = [x[0] for x in list_tweets]

transformer = cPickle.load(open('new_tf2.pickle','rb'))
SVC = cPickle.load(open('SVC2.pickle','rb'))
vectorizer = cPickle.load(open('new_vect2.pickle','rb'))

v1 = vectorizer.transform(t_txt)
v2 = transformer.transform(v1)


#rv1 = vect2.transform(t_txt)
#rv2 = t2.transform(rv1)

results = SVC.predict(v2)
#svr_results = LSVR.predict(rv2)
probs = SVC.predict_proba(v2)
print len(alltweets)
print len(results)

print results
#L =  list(results) 
L = []


#print t_txt[:5]
i=0
j=0
probabilities = list(probs)
ind = 0
while ind < len(probabilities):
	x = probabilities[ind]
	if x[1]>x[0]:
		i += 1

		#print x
	if x[1] > 0.830430012805:
		#0.980430012805
		#0.830430012805
		L.append(1)
		j+=1
	else:
		L.append(0)
	ind+=1



print
print len(L)
print i
print j
print L.count(0)
print L.count(1)





# insert the positively classified tweets into the database
column_names = ", ".join(names[1:]+ ["hashtags"])

print 
count = 0
index = 0
while index < len(alltweets):
	if L[index] == 1 and "dj dabs by on soundcloud" not in list_tweets[index][0]:
		#push to db
		#696584208060452864|||en|2016-02-08 06:39:51|0|0|whenever i hear that dab song i honestly do not think about the dance bc dabs came first  sorrynotsorry lol|||51563725|Alex Vasquez|||||False||en||||#sorrynotsorry||1|77
		conn2 = sqlite3.connect("../tweets.sqlite")
		cursor = conn2.cursor()
		tt = list_tweets[index][1:]
		t = 0
		while t < len(tt):
			if t !=  7 and t!= 19 and t!= 17 and t != 11:
				tt[t] = "'" + str(tt[t]) + "'"
			else:
				tt[t] = '"' + str(tt[t]) + '"'
			t+=1

		
		s = alltweets[index][0]

		words = s.split(" ") 


		formated_words = []
		#mentions = []

		hashtags = []

		for x in words:
			if "#" in x: 
				y = "#" + x.strip(",").strip().split("#")[-1]
				hashtags.append(y)
		hashtags = " ".join(hashtags)
		tt.append("'"+str(hashtags)+"'")
		values = ", ".join(tt)
		
		values = ", ".join(tt)
		#print list_tweets[index][0]
		#print values


		dbname = "tweets9_mdab"
		query = "INSERT INTO %s (%s) VALUES (%s) " % (dbname,column_names, values) 
		print query
		print 
		cursor.execute(query)
		conn2.commit()
		conn2.close()
		count += 1
	index +=1

print 
print L.count(1), "with 'dj dabs by on soundcloud'"
print count

print datetime.datetime.now()


conn = sqlite3.connect("../tweets.sqlite")
cursor = conn.cursor()
query = "Select Tweet_ID from tweets9_mdab where Tweet_ID in (select Tweet_ID from oldtweets9_mdab)"
cursor.execute(query)
results = cursor.fetchall()
print len(results)
i = 0
for y in results:
	x = y[0]
	query = "select FavoriteCount, RetweetCount from oldtweets9_mdab where Tweet_ID = '%d'"%(x)
	cursor.execute(query)
	r = cursor.fetchall()[0]
	fc = r[0]
	rc = r[1]
	query = "Update %s set FavoriteCount = %d, RetweetCount = %d where Tweet_ID = '%s'" % ("tweets9_mdab", fc, rc, x)
	print query
	cursor.execute(query)
	conn.commit()
	i+=1
conn.close()
exit()