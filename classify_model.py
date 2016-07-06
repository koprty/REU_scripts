from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
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
from twython import Twython,TwythonError


APP_KEYS = ['TSZyBWKsHZRBlvqrFag7FucuX','SXqFBvQ0ibQxJLzANwYYF1jcN','cNSOzpCmfS730QsIC8AC6fnVv','HEGsXHtuOLUlUNkUcBWMlLqaK',
'OtspVKgnB2UhNJSIXhf8QYIQO',
'7nTuFIXq6QmanfVx20OGXsL6N', 
'PxNDGaWD6hUWLFpYffl8a83ZD', 
'Du77cjeL7Q7hIrg89S62R6scu', 'zssUc5yAchM6TTPs5nRbsMxsQ']

APP_SECRETS = ['NNVeYdE9AICI1a4Ytkm4PHyY9KhwLehZItP0WiZUSLaZG9H2Ml','7Dz4eSTJumYpYnPWdgKitBN60OTFgREsp6OdiNY6C3ihT1OS2l',
'wPwcpAlVTYBWEqzYFWG6vsVi8YRzbY4XMC2Fe8DkD4DkRnIviz','KeiDW2vmHIMUcUN9scHFYqYBlQg7K3LfOPinjtTA6cxbXyEve5', 'fv77emr7170r7uh4vSHLSfrnK4c8ZGmNZ88foysls3L15MRprZ',
'wDL6lXHThz2GubZmFEogZE9ZcDDD6mJBTrSiaonjUZ6J1vGuPa', 

'gwrVjhgXosdQcL5cSXXmlC8QsI29g4vs9bJj6iWmemNyeMcjQe',
'e7cOLH4PDTf3bvgJuXg7xtLiW7M2oPimr2oP4wN8RANdXEP0gF','zealQwvvv5N0r0Olja053Wd19VK59qeyCvTA45dXtq5OLkSFkZ']

OAUTH_TOKENS = ['701759705421639681-nutlNGruF7WZjq0kXZUTcKVbrnXs3vD','701759705421639681-KcNn0T4hdVjVSq2NhiGagdFV5pgUNHa',
'258508177-BqAvmsMCK4vdfBVp5c0wIIyBB6nNrhtOWtbdM82O','258508177-uQDYR2XTlrMpxfjwKYEIAaxarHkhZygl3n44Jz8k', 
'258508177-bHYLjetyZRNsulsFtI8oIBVJsrr3DxHdqhgxWzJ4',
'258508177-KHviBY6zYX7PjVBzKjfCbsDWuXSyBHOcfuo7HzyQ',
'701759705421639681-F84hDkTSfuG7KqJcqzk1rm88Izx1NUG',
'701759705421639681-O9d1FGk2LfGZ5FdR4wwlJpWCqf914MM', '701759705421639681-xYAlZAI4x0dJhUEOe6hawOea1MbQc8o']

OAUTH_TOKEN_SECRETS =['3hhidOQwxTMyc5MTDsmhaplfGcK5xVzB83hFb07OMALXh','HPmY0P8q23KVYx8AKS8tuWpCOAj8TMxQ3BYD1nb7sVF5s',
'NWvnPLNLFrePW9dg9dYC9U0dhilZpbuI3TvkFdL8LrUgw','jBItJWaPly3P8QUmCAbeix6n9JLjqEV4fNQkkrnYe4UJk', 'A7iKPr6haM4P5kbGTVzEmID4tyjm1tYCsUc8R8b61B6BR',
'2GyQgJizM5ipjr5OVC8iYEav7DlPWMjvwLTSKqVIPAMFI','4qVZZVzlayIHuXNb69yysjKZbR2Pg1z5gd7ItSfnbjgdE', 
'J4ma0LYo1iQexcivSzuQcYUmtDteYYAzni5bT7hz5MSk4', 'vdsE88d7ptFvmH1yEZorLwnr7JQLvGz9dlAEETUJ4kdAH']

index = 0

# preprocess an array of tweets 
# Returns a tuple (preprocessed tweets, space-separated hashtags)
def preprocess(twe):
	removal_pattern1 = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
	removal_pattern2 = re.compile('//t.co(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
	removal_pattern3 = re.compile('\n')
	removal_pattern4 = re.compile('\r')
	removal_pattern5 = re.compile('@[\w]*')

	htmlentities = ["&quot;","&amp;","&lt;","&gt;","&OElig;","&oelig;","&Scaron;","&scaron;","&Yuml;","&circ;","&tilde;","&ensp;","&emsp;","&thinsp;","&zwnj;","&zwj;","&lrm;","&rlm;","&ndash;","&mdash;","&lsquo;","&rsquo;","&sbquo;","&ldquo;","&rdquo;","&bdquo;","&dagger;","&Dagger;","&permil;","&lsaquo;"]
	tweets = []
	for x in twe:
		tweet = x [0]
		# preprocess tweet_text
		s = tweet.encode('ascii','ignore')
		words = s.split(" ") 
		hashtags = []
		i = 0
		while i < len(words):
			x = words[i]
			if "#" in x:
				hashie = x.strip(",").strip().split("#")
				y = "#" + hashie[-1]
				hashtags.append(y.strip())
			i+=1
		s = " ".join(words)
		hashtags = " ".join(hashtags)
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
		tweets.append((s.strip(), hashtags))
	return tweets
	
def classify_mdab(tweet = []):
	tf = cPickle.load(open('twitter_data/tweet_classifier/new_tf2.pickle','rb'))
	SVC = cPickle.load(open('twitter_data/tweet_classifier/SVC2.pickle','rb'))
	vect = cPickle.load(open('twitter_data/tweet_classifier/new_vect2.pickle','rb'))

	v1 = vect.transform(tweet)
	v2 = tf.transform(v1)

	result = SVC.predict_proba(v2)

	return result[0][1]> 0.830430012805

def run_topic_model(tweet = ""):
	tokenizer = RegexpTokenizer(r'\w+')
	p_stemmer = PorterStemmer()
	en_stop = list(set(get_stop_words('en')) | set(stopwords.words('english'))) + ['u','oh', 'uh', 'im', 'n', 'dont', 'ur']

	raw = tweet.lower()
	tokens =tokenizer.tokenize(raw)
	stopped_tokens = [j for j in tokens if not j in stopwords.words('english')]
	stemmed_tokens = [p_stemmer.stem(j) for j in stopped_tokens]

	d = corpora.Dictionary.load("topic_modeling/twitter/tweet_dict.dict")
	bow = d.doc2bow(stemmed_tokens)

	lda = models.ldamodel.LdaModel.load("topic_modeling/twitter/lda_9.ginsem")
	tweet_lda = lda.get_document_topics(bow,minimum_probability = .001)
	return tweet_lda

def classify_user(user_desc= []):
	user_SVC = cPickle.load(open("twitter_data/user_classifier/SVC_users.pickle", 'rb'))
	user_vect = cPickle.load(open("twitter_data/user_classifier/count_users.pickle", 'rb'))

	v1 = user_vect.transform(user_desc)

	result = user_SVC.predict_proba(v1)

	return result[0][1] > .58257648005

def get_followers_following(usr_id):
	friend_cursor = -1
	follower_cursor = -1

	APP_KEY = APP_KEYS[index]
	APP_SECRET = APP_SECRETS[index]
	OAUTH_TOKEN = OAUTH_TOKENS[index]
	OAUTH_TOKEN_SECRET = OAUTH_TOKEN_SECRETS[index]

	try:
		twitter = Twython (APP_KEY, APP_SECRET)
		auth = twitter.get_authentication_tokens()
		twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET) 

		friends = ""
		while (friend_cursor != 0):
			following = twitter.get_friends_ids(id = usr_id, cursor = friend_cursor)
			for ID in following['ids']:
				friends += str(ID) + " " 
				friend_cursor =  following["next_cursor"]
		friends = friends[:-1]
		if len(friends) == 0:
			friends = "null"

		follow = ""
		while (follower_cursor != 0):
			followers = twitter.get_followers_ids(id = i,cursor= follower_cursor)
			for ID in followers['ids']:
				follow += str(ID) + " " 
			follower_cursor =  followers["next_cursor"]
		follow= follow[:-1]
		if len(follow) == 0:
			follow = "null"

		return (friends,follow)

	except Exception as e:
		print e
		if "429 (Too Many Requests)" in str(e):
			global index
			index += 1
			if index == len(APP_KEYS):
				index = 0
				print "sleepy time - 15 minutes"
				print datetime.datetime.now()
				time.sleep(870)
				return get_followers_following(usr_id)
		elif "401 (Unauthorized)" in str(e):
			print "401 error"
			return ("null","null")
		elif "404 (Not Found)" in str(e):
			print "404 error"
			return ("null","null")
		else:
			print e
			return ("null","null")

def classify_and_model():
	#Pulling Tweet_ID, Usr_ID, Screename, CreatedAt, Tweet_Text, and Usr_Description
	# other script doesnt get hashtags... :/ 
	# we will get hashtags from preprocess function
	'''
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	query = "select Tweet_ID, Usr_ID, Scrrename, CreatedAt, Tweet_Text, Usr_Description from %s"%(table)
	#should we add a where statement to check if datechecked is null??
	cursor.execute(query)
	twe = cursor.fetchall()
	conn.close() 
	'''

        #preprocess	
	preprocess =  preprocess()
	tweet_text = [x[0] for x in preprocess]
	htags = [h[1] for h in preprocess]

	### while loop for tweets
	'''
	i = 0
       	while i < len(preprocess):
		
		#classify one tweet and other stuff here 

		i +=1
	'''

	#classify as positive or negative (MAKE SURE TWEET IS IN LIST, e.g. ["this is the tweet"])

	if classify_mdab([tweet_text]):
		#run topic_model
		tweet_topic_dist = run_topic_model(tweet_txt)
		top_topic = sorted(tweet_topic_dist,key=lambda x: x[1], reverse = True)[0]
		spaced_topics = ""

		for top in tweet_topic_dist:
			space_topics += top[1]
			if (top[0]!=8):
				space_topics += " "
		#update database with new tweet
		query = "INSERT INTO TABLE_NAME " + \
				 "(Tweet_ID, Usr_ID, Screename, hashtags, Tweet_Text, CreatedAt, DateChecked, "  +\
				 "TopTopic, SpaceTopic, Zero, One, Two, Three, Four, Five, Six, Seven, Eight) " +\
				 "values (" + tweet_id + ", " + usr_id + ", '" + screename + "', '" + hashtags + "',"+ \
				 " '" + tweet_text + "', '" + creationDate + "', '" + datetime.datetime.now() + "'," + \
				 " " + top_topic[0] + ", '" + space_topics + "', "
		for top in tweet_topic_dist:
			query += top[1]
			if (top[0]!=8):
				query += ", "
			else:
				query += ");"
		cursor.execute(query)
		conn.commit()

		#see if user already in previous databases
		query = "select Usr_ID from users"
		cursor.execute(query)
		old_users = cursor.fetchall()
		old_users = [user[0] for user in old_users]
		query = "select Usr_ID from tweets9_users"
		cursor.execute(query)
		t9_users = cursor.fetchall()
		t9_users = [user[0] for user in t9_users]

		if (usr_id not in old_users) and (usr_id not in t9_users):
			#if not, run user classification (like tweet classifier, put description in list, [])
			if classify_user([usr_desc]):
				#positive for individual, write to individuals table
				#get following and followers
				friends_follow = get_followers_following(usr_id)
				friends = friends_follow[0]
				follow = friends_follow[1]
				follow_count = len(follow.split(" "))
				friend_count = len(friends.split(" "))

				conn = sqlite3.connect(db)
				cursor = conn.cursor()
				query = "INSERT INTO individuals (Usr_ID, Screename, NumFollowers, NumFollowing, Followers, Following, Description) " +\
						"values ('%s', '%s', %s, %s, '%s', '%s','%s');" % (usr_id, screename, follow_count, friend_count, follow, friends, usr_desc)

			else:
				#negative for individual, write to non-individuals table
				#get following and followers
				friends_follow = get_followers_following(usr_id)
				friends = friends_follow[0]
				follow = friends_follow[1]
				follow_count = len(follow.split(" "))
				friend_count = len(friends.split(" "))

				conn = sqlite3.connect(db)
				cursor = conn.cursor()
				query = "INSERT INTO non_individuals (Usr_ID, Screename, NumFollowers, NumFollowing, Followers, Following, Description) " +\
						"values ('%s', '%s', %s, %s, '%s', '%s','%s');" % (usr_id, screename, follow_count, friend_count, follow, friends, usr_desc)
	return	


#sched = BlockingScheduler()
#sched.add_job(classify_and_model, 'interval', minutes = 15)
#sched.start()

'''
####### Example of using preprocess function ####
db = "twitter_data/tweets.sqlite"
table = "tweets9_streaming"
conn = sqlite3.connect(db)
cursor = conn.cursor()
query = "select Tweet_Text from %s"%(table)
cursor.execute(query)
twe = cursor.fetchall()
conn.close()

preprocess_streaming =  preprocess(twe)
#print len(preprocess_streaming)
print preprocess_streaming
'''
#################################################

sample_tweet = "im high dab bout to smoke some hash oil" # should be positive
sample_shop_description = "smokeshop, we sell medical marijuana bongs glass rigs" #should be false for user classification
sample_ind_description = "living in arizona loving life" # should be true for user classification

#### Example of using classification function ####
result = classify_mdab([sample_tweet])
print result #TRUE

#################################################

#### Example of using topic model function ####
tm = run_topic_model(sample_tweet)
print tm 

#################################################

#### Example of user classification function ####
suc = classify_user([sample_shop_description])
print suc #FALSE 
iuc = classify_user([sample_ind_description])
print iuc #TRUE



