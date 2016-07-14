import datetime # datetime, timedelta
import cPickle
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.svm import SVC
import gensim
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import re
import sqlite3
import string
import time

####Analyze Unpopular Tweets

## we will define popular as having at least 5 retweets
# get unpopular tweets
def getUnpop(db, top_table):
	conn = sqlite3.connect(db)
	cursor = conn.cursor() 

	query = "select TopTopic, Zero,  One, Two, Three, Four, Five, Six, Seven, Eight from %s where (RetweetCount_15min is Not Null and RetweetCount_15min < 5) or (RetweetCount_1hour is Not Null and RetweetCount_1hour < 5) or (RetweetCount_1day is Not Null and RetweetCount_1day <  5)or (RetweetCount_2day is Not Null and RetweetCount_2day < 5) or (RetweetCount_1week is Not Null and RetweetCount_1week < 5)"%(top_table)
	
	cursor.execute(query)
	topicModels = cursor.fetchall()
	topTopics = [x[0] for x in topicModels]

	#get frequencies of Topic Models
	tt = []
	for y in range(9):
		tt.append( (y, topTopics.count(y)))
	

	# get averages for topic models
	sums = [0]*9
	
	for (TopTopic, Zero, One, Two, Three, Four, Five, Six, Seven, Eight) in topicModels:
		sums[0] += Zero
		sums[1] += One
		sums[2] += Two
		sums[3] += Three
		sums[4] += Four
		sums[5] += Five
		sums[6] += Six 
		sums[7] += Seven
		sums[8] += Eight
	n = len(topTopics)
	averages = [sums[z]/n for z in range(9)]
	print n 
	print tt
	#print "Sums: ", sums
	print "Averages: ", averages
	conn.close()

getUnpop("rt_tweets.sqlite", "total_topics")


def UpdateRetweetCountsOldDb(db, top_table, table):
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	query = "select Tweet_ID, RetweetCount from %s"%(table)
	cursor.execute(query)
	allTweetsRC =cursor.fetchall()
	i = 0
	for (twe_id, rc) in allTweetsRC:
		query = "update %s set RetweetCount_1week = %d, RetweetCount_2day = %d, RetweetCount_1day = %d, RetweetCount_1week = %d, RetweetCount_1hour = %d, RetweetCount_15min = %d where Tweet_ID = %d"%(top_table, rc, rc, rc, rc, rc, rc, twe_id)
		print query 
		cursor.execute(query)
		conn.commit()
		print i
		i+=1
#UpdateRetweetCountsOldDb("rt_tweets.sqlite", "total_topics", "totalmdabs")
#UpdateRetweetCountsOldDb("rt_tweets.sqlite", "tweets9_topics", "tweets9_mdab")
#UpdateRetweetCountsOldDb("rt_tweets.sqlite", "topics", "posdab_Tweets")


