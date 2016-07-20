from twython import Twython,TwythonError
import sqlite3
import gensim
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import json
import re
import string
import os.path
import datetime
import time

APP_KEYS = ['sLvJemuMr6h526uHjakE9LAft',
'5UITYGUNroPqMvvJzbOUJ6o28','WDe7w0McHLprfa1owenJGyWzh']

APP_SECRETS = ['WEmwARfUxlhAjsNd7qWdBvlfqYTNzoFYlYchpN0cn87TYiNYfz',
'H4LzEoPHRSOJWcg8INiRiv9yWohhpI6VQHsGQ7V0MdkBFQjPqZ','SlCnBgqZOlImqACfzhd49qL2vI8UBskHqLCSVkajLE0g1ijMhB']

OAUTH_TOKENS = ['258508177-3OFSF8YqGShPWrCfvmYqIGk4sRYY8u3m00tyb0EM',
'258508177-GwRxcnsn24gNmvhEWMmr57LKfAmbzk5OC9yHwooZ','258508177-WLuVq4RFfZm8YlFA7W73oYhrdp17Pnrp6fZ6ylcQ']

OAUTH_TOKEN_SECRETS =['nwx1XYjdEOezbtfADKlvIylJQkaIwgHNhG8uJq4FuzEDi',
'G8x6S6XUjxJJfax4qeIxEKbgjxQhzMI2BRF2vbfqb7qpe','njQzQPN8Gp5apOy6hq0hQjRU6XtwKuFbaKathWdRSRw9h']

tokenizer = RegexpTokenizer(r'\w+')
p_stemmer = PorterStemmer()

conn = sqlite3.connect("../tweets.sqlite")
cursor = conn.cursor()
query = "select Usr_ID, Screename, Category from totalusers where Usr_ID not in (select User_ID from timeline_dist)"
cursor.execute(query)
users = cursor.fetchall()




def preprocess(tweet):
	removal_pattern1 = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
	removal_pattern2 = re.compile('//t.co(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
	removal_pattern3 = re.compile('\n')
	removal_pattern4 = re.compile('\r')
	removal_pattern5 = re.compile('@[\w]*')

	htmlentities = ["&quot;","&amp;","&lt;","&gt;","&OElig;","&oelig;","&Scaron;","&scaron;","&Yuml;","&circ;","&tilde;","&ensp;","&emsp;","&thinsp;","&zwnj;","&zwj;","&lrm;","&rlm;","&ndash;","&mdash;","&lsquo;","&rsquo;","&sbquo;","&ldquo;","&rdquo;","&bdquo;","&dagger;","&Dagger;","&permil;","&lsaquo;"]
	
	# preprocess tweet_text
	s = tweet.encode('ascii','ignore')
	s = removal_pattern5.sub('', s)
	s = removal_pattern1.sub('', s)
	s = removal_pattern2.sub('', s)
	s = removal_pattern3.sub(' ', s)
	s = s.translate(None, string.punctuation)
	s = s.lower()
	s = removal_pattern4.sub('',s)
        #s = s.replace("'", "")
	#s = s.replace('"', "")
	
	for h in htmlentities:
		s = s.replace(h, "")
	return tweet

def get_tweet_topics(user_id, index=0):
	APP_KEY = APP_KEYS[index]
	APP_SECRET = APP_SECRETS[index]
	OAUTH_TOKEN = OAUTH_TOKENS[index]
	OAUTH_TOKEN_SECRET = OAUTH_TOKEN_SECRETS[index]
	try:
		twitter = Twython (APP_KEY, APP_SECRET)
		auth = twitter.get_authentication_tokens()
		twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET) 

		timeline = twitter.get_user_timeline(user_id=user[0],count=200)

		sum_prob = [0,0,0,0,0,0,0,0,0]
		for tweet_info in timeline:
			tweet = tweet_info['text']
			tweet = preprocess(tweet)
			en_stop = list(set(get_stop_words('en')) | set(stopwords.words('english'))) + ['u','oh', 'uh', 'im', 'n', 'dont', 'ur']

			raw = tweet.lower()
			tokens =tokenizer.tokenize(raw)
			stopped_tokens = [j for j in tokens if not j in stopwords.words('english')]
			stemmed_tokens = [p_stemmer.stem(j) for j in stopped_tokens]

			d = corpora.Dictionary.load("../topic_modeling/twitter/tweet_dict.dict")
			bow = d.doc2bow(stemmed_tokens)

			lda = models.ldamodel.LdaModel.load("../topic_modeling/twitter/lda_9.ginsem")
			tweet_lda = lda.get_document_topics(bow,minimum_probability = .001)
			for topic in tweet_lda:
				topic_num = topic[0]
				topic_prob = topic[1]
				sum_prob[topic_num] += topic_prob
		i= 0
		for value in sum_prob:
			sum_prob[i] = value/len(timeline)
			i += 1

		return (sum_prob, index)
	except Exception as e:
		print e
		if "429 (Too Many Requests)" in str(e):
			#global index
			index += 1
			#print datetime.datetime.now()
			if index == len(APP_KEYS):
				index = 0
			return get_tweet_topics(user_id,index)
		elif "401 (Unauthorized)" in str(e):
			print "401 error"
			return (0,index)
		elif "404 (Not Found)" in str(e):
			print "404 error"
			return (0,index)
		else:
			print e
			return (0,index)
'''
if os.path.isfile("timeline_topics"):
	with open('timeline_topics') as file:
		di = json.load(file)
else:
	di = {}

for key in di:
	if di[key]['topic_dist'] != 0:
		topic_string = ""
		for topic in di[key]['topic_dist']:
			topic_string += str(topic) + " "
		topic_string = topic_string[:-1]
		query = "INSERT INTO timeline_dist VALUES (%s,'%s','%s','%s');" % (key, di[key]['screename'],di[key]['category'],topic_string)
		cursor.execute(query)

users_to_check = []
for user in users:
	if user[0] not in list_of_keys:
		users_to_check.append(user)
'''

index = 0
for user in users:
	dist_index = get_tweet_topics(user[0],index)
	index = dist_index[1]
	dist = dist_index[0]
	if dist != 0:
		topic_string = ""
		for topic in dist:
			topic_string += str(topic) + " "
		topic_string = topic_string[:-1]
		query = "INSERT INTO timeline_dist VALUES (%s,'%s','%s','%s');" % (user[0],user[1],user[2],topic_string)
		cursor.execute(query)
		conn.commit()
		#print query

conn.commit()
conn.close()




