import cPickle
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
import sqlite3

transformer = cPickle.load(open('transformer.pickle','rb'))
LSVR = cPickle.load(open('LSVR.pickle','rb'))
vectorizer = cPickle.load(open('vectorizer.pickle','rb'))

conn= sqlite3.connect("tweetDB9.sqlite")
cursor = conn.cursor()
query = "select Tweet_Text, Usr_Screename, Tweet_ID from tweets9_streaming";
cursor.execute(query)
r = cursor.fetchall()

tweet_tuples = r 

tweet_text = []

for x in tweet_tuples:
	tweet_text.append(x[0])

v1 = vectorizer.transform(tweet_text)
v2 = transformer.transform(v1)

results = LSVR.predict(v2)

tweet_results = []
index = 0
for r in results:
	tup = (tweet_text[index],tweet_tuples[index][1], tweet_tuples[index][2],r)
	index+=1
	tweet_results.append(tup)

tweet_results.sort(key = lambda tup: tup[3])

fout = open("results.txt", "w")
for tr in tweet_results:
	fout.write(str(tr))
	fout.write("\n")
fout.close()

