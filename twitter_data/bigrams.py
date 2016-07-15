import nltk
from nltk.collocations import *
from nltk.tokenize import TweetTokenizer
import sqlite3


def bigrams_trigrams(rt_num = 0, symbol = ">="):
	print "Most Frequent Bi/Trigrams for Tweets with " + symbol  + str(rt_num) + " Retweets"

	conn = sqlite3.connect("../tweets.sqlite")
	cursor = conn.cursor()
	query = "select Tweet_Text from totalmdabs where RetweetCount" + symbol + "%s" % rt_num
	cursor.execute(query)
	tweets = cursor.fetchall()

	tweets = [tweet[0] for tweet in tweets]
	print len(tweets)

	tknzr = TweetTokenizer()

	tokenized_tweets = []
	for tweet in tweets:
		tk = tknzr.tokenize(tweet)
		tokenized_tweets.extend(tk)

	bigram_measures = nltk.collocations.BigramAssocMeasures()
	finder = BigramCollocationFinder.from_words(tokenized_tweets)
	arr= finder.nbest(bigram_measures.raw_freq,10) # doctext: +NORMALIZE_WHITESPACE
	#print arr
	print "------Ten Most Frequent Bigrams------"
	for a in arr:
		s = str(a[0]) + " " +str(a[1])
		print s
		query = "select count(*) from totalmdabs where Tweet_Text LIKE '%" +s + "%' and RetweetCount" + symbol + str(rt_num)+ ";"
		cursor.execute(query)
		num = cursor.fetchall()[0][0]
		print num

	#trigrams?
	print "------Ten Most Frequent Trigrams------"
	trigram_measures = nltk.collocations.TrigramAssocMeasures()
	finder2 = TrigramCollocationFinder.from_words(tokenized_tweets)
	arr2 = finder2.nbest(trigram_measures.raw_freq,10)
	for a in arr2:
		s = str(a[0]) + " " +str(a[1]) + " " + str(a[2])
		print s
		query = "select count(*) from totalmdabs where Tweet_Text LIKE '%" +s + "%' and RetweetCount" + symbol + str(rt_num)+ ";"
		cursor.execute(query)
		num = cursor.fetchall()[0][0]
		print num
	conn.close()
bigrams_trigrams(-1, ">")