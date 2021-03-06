from apscheduler.schedulers.blocking import BlockingScheduler
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
from twython import Twython,TwythonError
import time


index = 0

# preprocess an array of tweets 
# Returns a tuple (preprocessed tweets, space-separated hashtags)
def preprocess(twe):
	print "PREPROCESSING"
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
	
#returns true if first tweet in array has a high enough probability of being positive 
#the passed in array is only meant to have one tweet in it
def classify_mdab(tweet = []):
	print "CLASSIFYING TWEET: " + tweet[0]
	tf = cPickle.load(open('new_tf2.pickle','rb'))
	SVC = cPickle.load(open('SVC2.pickle','rb'))
	vect = cPickle.load(open('new_vect2.pickle','rb'))

	v1 = vect.transform(tweet)
	v2 = tf.transform(v1)

	result = SVC.predict_proba(v2)

	return result[0][1]> 0.830430012805

#returns topic distribution of a tweet passed in 
#returns list of tuples, each tuple having the topic number as its first element 
#and the probability of that topic as its second element
def run_topic_model(tweet = ""):
	print "RUNNING TOPIC MODEL ON TWEET"
	tokenizer = RegexpTokenizer(r'\w+')
	p_stemmer = PorterStemmer()
	en_stop = list(set(get_stop_words('en')) | set(stopwords.words('english'))) + ['u','oh', 'uh', 'im', 'n', 'dont', 'ur']

	raw = tweet.lower()
	tokens =tokenizer.tokenize(raw)
	stopped_tokens = [j for j in tokens if not j in stopwords.words('english')]
	stemmed_tokens = [p_stemmer.stem(j) for j in stopped_tokens]

	d = corpora.Dictionary.load("tweet_dict.dict")
	bow = d.doc2bow(stemmed_tokens)

	lda = models.ldamodel.LdaModel.load("lda_9.ginsem")
	tweet_lda = lda.get_document_topics(bow,minimum_probability = .001)
	return tweet_lda

#runs user classifier on description passed in 
#returns true if probability is high enough to be classified as individual
#description should be passed in using a list with it as the only element
def classify_user(user_desc= []):
	if len(user_desc) > 0 and not user_desc[0] is  None:
		print "CLASSIFYING USER: " + user_desc[0] # breaks when Nonetype
		user_SVC = cPickle.load(open("SVC_users.pickle", 'rb'))
		user_vect = cPickle.load(open("count_users.pickle", 'rb'))

		v1 = user_vect.transform(user_desc)

		result = user_SVC.predict_proba(v1)

		return result[0][1] > .58257648005
	return False


def classify_and_model(db, streamer, table ):
	#Pulling Tweet_ID, Usr_ID, Screename, CreatedAt, Tweet_Text, and Usr_Description
	# other script doesnt get hashtags... :/ 
	# we will get hashtags from preprocess function
	#db = "tweets.sqlite"
	#table = "tweets10_streaming"
	
	#target = open("last_date.txt", "r")
	#last_acquired = target.read()
	#target.close()
	
	#last_acquired = "Wed Jun 15 16:13:17 +0000 2016"

	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	query = "select Tweet_Text, Tweet_ID, Usr_ID, Usr_Screename, TwtCreatedAt, Usr_Description from %s where not (ImpureQuery=0) and Tweet_ID not in (select Tweet_ID from %s)"%(streamer,table)
	cursor.execute(query)
	twe = cursor.fetchall()
	conn.close() 
	print len(twe)
	print "Received Data_preparing to preprocess"
    #preprocess	
	preprocessed =  preprocess(twe)
	tweet_text = [x[0] for x in preprocessed]
	htags = [h[1] for h in preprocessed]


	### while loop for tweets
	i = 0
	while i < len(preprocessed):
		#get pertinent tweet information
		tup = twe[i]
		tweet_id = tup[1]
		usr_id = tup[2]
		screename = tup[3]
		hashtags = htags[i]
		t_text = tweet_text[i]
		creationDate = tup[4]
		usr_desc = tup[5]
		#classify as positive or negative (MAKE SURE TWEET IS IN LIST, e.g. ["this is the tweet"])

		if classify_mdab([t_text]):
			#run topic_model
			tweet_topic_dist = run_topic_model(t_text)
			top_topic = sorted(tweet_topic_dist,key=lambda x: x[1], reverse = True)[0]

			space_topics = ""
			for top in tweet_topic_dist:
				space_topics += (str(top[1]) + " ")
			space_topics = space_topics[:-1]
			#update database with new tweet
			conn = sqlite3.connect(db)
			cursor = conn.cursor()
			query = " INSERT INTO %s (Tweet_ID, Usr_ID, Screename, hashtags, Tweet_Text, CreatedAt, DateChecked, TopTopic, SpaceTopic, Zero, One, Two, Three, Four, Five, Six, Seven, Eight) \
					 values (%s, %s, '%s', \"\"\"%s\"\"\", '%s', '%s', '%s', %s, '%s', " %(table, tweet_id, usr_id, screename, hashtags,t_text, creationDate,datetime.datetime.now(),top_topic[0],space_topics)
			print query
			for top in tweet_topic_dist:
				query += str(top[1])
				if (top[0]!=8):
					query += ", "
				else:
					query += ");"
			cursor.execute(query)
			conn.commit()
			conn.close()

			#see if user already in previous databases
			conn = sqlite3.connect(db)
			cursor = conn.cursor()
			query = "select Usr_ID from users"
			cursor.execute(query)
			old_users = cursor.fetchall()
			old_users = [user[0] for user in old_users]
			#query = "select Usr_ID from tweets9_users"
			#cursor.execute(query)
			#t9_users = cursor.fetchall()
			#t9_users = [user[0] for user in t9_users]
			conn.close()
			if (usr_id not in old_users):
				#if not, run user classification (like tweet classifier, put description in list, [])
				if classify_user([usr_desc]):


					###### We will get followers and followings of users separately to avoid api overload during the streaming #######

					#positive for individual, write to individuals table
					#get following and followers
					'''
					friends_follow = get_followers_following(usr_id)
					print friends_follow
					#here
					friends = friends_follow[0]
					follow = friends_follow[1]
					follow_count = len(follow.split(" "))
					friend_count = len(friends.split(" "))
					'''
					conn = sqlite3.connect(db)
					cursor = conn.cursor()

					'''
					query = "INSERT INTO users (Usr_ID, Screename, Category, Followers, Following, Description) " +\
							"values ('%s', '%s', %s, %s, 'individuals', '%s', '%s','%s');" % (usr_id, screename, follow_count, friend_count, follow, friends, usr_desc)
					'''
					query = "INSERT INTO users (Usr_ID, Screename,  Category,  Description) " +\
							"values ('%s',  '%s', 'individuals', \"\"\"%s\"\"\");" % (usr_id, screename, usr_desc)
					cursor.execute(query)
					conn.commit()
					conn.close()
				else:
					#negative for individual, write to non-individuals table
					#get following and followers
					'''
					friends_follow = get_followers_following(usr_id)
					friends = friends_follow[0]
					follow = friends_follow[1]
					follow_count = len(follow.split(" "))
					friend_count = len(friends.split(" "))
					'''
					conn = sqlite3.connect(db)
					cursor = conn.cursor()
					'''
					query = "INSERT INTO users (Usr_ID, Screename, NumFollowers, NumFollowing, Category, Followers, Following, Description) " +\
							"values ('%s', '%s', %s, %s, 'non-individuals', '%s', '%s','%s');" % (usr_id, screename, follow_count, friend_count, follow, friends, usr_desc)
					'''
					query = "INSERT INTO users (Usr_ID, Screename, Category,  Description) " +\
							"values ('%s', '%s', 'non-individuals', \"\"\"%s\"\"\");" % (usr_id, screename, usr_desc)
					cursor.execute(query)

					conn.commit()
					conn.close()
			else:
				print "User already in database"
		#update ImpureQuery
		conn = sqlite3.connect(db)
		cursor = conn.cursor()
		query = "UPDATE %s SET ImpureQuery=0 WHERE Tweet_ID = %s" % (streamer, tweet_id)
		cursor.execute(query)
		conn.commit()
		conn.close()
		i += 1
	return	

	
################################### Functions for Getting Retweet Counts ##################################
def getRetweetCount(twe_id):
	index=0
	while (index <len(APP_KEYS)):
		APP_KEY = APP_KEYS[index]
		APP_SECRET = APP_SECRETS[index]
		OAUTH_TOKEN = OAUTH_TOKENS[index]
		OAUTH_TOKEN_SECRET = OAUTH_TOKEN_SECRETS[index]
		try:
			twitter = Twython (APP_KEY, APP_SECRET)
			auth = twitter.get_authentication_tokens()
			twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET) 
			result = twitter.show_status(id=twe_id)
			'''
			#print result['user']['screen_name'] + " " + result['user']['description']
			tweet['Usr_Screename'] = result['user']['screen_name']
			tweet['Usr_Description'] = result['user']['description']
			
			tweet['FavoriteCount'] = int(result['favorite_count'])
			'''
			return int(result['retweet_count'])
		except Exception as e:
			if "429 (Too Many Requests)" in str(e):
				index += 1
				print "App Exceeded: index = %d"%(index)
				pass
			elif "404 (Not Found)" in str(e):
				return -1
			elif "403 (Forbidden)" in str(e):
				return -1
			else:
				print e

	return ''

def updateRetweetCountOnIntervals (db, streamer, table ):
	timeDifference = datetime.timedelta(hours = 5) # 5 hour time difference from running it at stl 
	# 15 minutes intervals for each category 
	#RetweetCount_15min INT
	#lets get rid of a couple of these so that there is not an app overload
	'''
	print "Updating Retweet Count - 15 minutes _______________ "
	now = datetime.datetime.now()
	timedelta = datetime.timedelta(minutes = 15)
	mark= now - timedelta + timeDifference
	#query = "select %s.Tweet_ID from %s INNER JOIN %s on %s.Tweet_ID = %s.Tweet_ID where TwtCreatedAt < '%s' and RetweetCount_15min is Null"%(streamer,streamer, table, table, streamer, mark)
	query = "select Tweet_ID from %s where CreatedAt < '%s' and RetweetCount_15min is Null"%(table, mark)
	print query
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	cursor.execute(query)
	ids_in_time_interval = cursor.fetchall()
	conn.close()
	print len(ids_in_time_interval)
	for twe_id in ids_in_time_interval:
		twe_id = twe_id[0]
		print twe_id
		rc = getRetweetCount ( twe_id )
		if len(str(rc)) > 0:
			query = "update %s set RetweetCount_15min = %d where tweet_id = %d"%(table,rc, twe_id)
			print  "RC: ", query
			conn = sqlite3.connect(db)
			cursor = conn.cursor()
			cursor.execute(query)
			conn.commit()
			conn.close()
	'''
	print "Updating Retweet Count - 1 hour _______________ "
	# one hour -  RetweetCount_1hour INT,
	now = datetime.datetime.now()
	timedelta = datetime.timedelta(hours = 1)
	mark= now - timedelta + timeDifference
	#mark= now - timedelta
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	query = "select %s.Tweet_ID from %s INNER JOIN %s on %s.Tweet_ID = %s.Tweet_ID where TwtCreatedAt < '%s' and RetweetCount_1hour is Null"%(streamer,streamer, table, table, streamer, mark)
	query = "select Tweet_ID from %s where CreatedAt < '%s' and RetweetCount_15min is Null"%(table, mark)
	cursor.execute(query)
	ids_in_time_interval = cursor.fetchall()
	conn.close()
	print len(ids_in_time_interval)
	for twe_id in ids_in_time_interval:
		twe_id = twe_id[0]
		print twe_id
		rc = getRetweetCount ( twe_id )
		if len(str(rc)) > 0:
			query = "update %s set RetweetCount_1hour = %d where tweet_id = %d"%(table,rc, twe_id)
			print  "RC: ", query
			conn = sqlite3.connect(db)
			cursor = conn.cursor()
			cursor.execute(query)
			conn.commit()
			conn.close()
	'''
	# a day - RetweetCount_1day INT,
	print "Updating Retweet Count - 1 day  _______________ "
	now = datetime.datetime.now()
	timedelta = datetime.timedelta(days = 1)
	#mark= now - timedelta
	mark= now - timedelta + timeDifference
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	query = "select %s.Tweet_ID from %s INNER JOIN %s on %s.Tweet_ID = %s.Tweet_ID where TwtCreatedAt < '%s' and RetweetCount_1day is Null"%(streamer,streamer, table, table, streamer, mark)
	query = "select Tweet_ID from %s where CreatedAt < '%s' and RetweetCount_15min is Null"%(table, mark)
	cursor.execute(query)
	ids_in_time_interval = cursor.fetchall()
	conn.close()
	print len(ids_in_time_interval)
	for twe_id in ids_in_time_interval:
		twe_id = twe_id[0]
		rc = getRetweetCount ( twe_id )
		if len(str(rc)) > 0:
			query = "update %s set RetweetCount_1day = %d where tweet_id = %d"%(table,rc, twe_id)
			print  "RC: ", query
			conn = sqlite3.connect(db)
			cursor = conn.cursor()
			cursor.execute(query)
			conn.commit()
			conn.close()
	'''
	print "Updating Retweet Count - 2 days_______________ "
	# a day - RetweetCount_2days INT,
	now = datetime.datetime.now()
	timedelta = datetime.timedelta(days = 1)
	#mark= now - timedelta
	mark= now - timedelta + timeDifference
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	query = "select %s.Tweet_ID from %s INNER JOIN %s on %s.Tweet_ID = %s.Tweet_ID where TwtCreatedAt < '%s' and RetweetCount_2day is Null"%(streamer,streamer, table, table, streamer, mark)
	query = "select Tweet_ID from %s where CreatedAt < '%s' and RetweetCount_15min is Null"%(table, mark)
	cursor.execute(query)
	ids_in_time_interval = cursor.fetchall()
	conn.close()
	print len(ids_in_time_interval)
	for twe_id in ids_in_time_interval:
		twe_id = twe_id[0]
		print twe_id
		rc = getRetweetCount ( twe_id )
		if len(str(rc)) > 0:
			query = "update %s set RetweetCount_2day = %d where tweet_id = %d"%(table, rc, twe_id)
			print  "RC: ", query
			conn = sqlite3.connect(db)
			cursor = conn.cursor()
			cursor.execute(query)
			conn.commit()
			conn.close()

	'''
	# a week -  RetweetCount_1week INT,
	print "Updating Retweet Count - 1 week _______________ "
	now = datetime.datetime.now()
	timedelta = datetime.timedelta(days = 7)
	#mark= now - timedelta
	mark= now - timedelta + timeDifference
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	query = "select %s.Tweet_ID from %s INNER JOIN %s on %s.Tweet_ID = %s.Tweet_ID where TwtCreatedAt < '%s' and RetweetCount_1week is Null"%(streamer,streamer, table, table, streamer, mark)
	query = "select Tweet_ID from %s where CreatedAt < '%s' and RetweetCount_15min is Null"%(table, mark)
	cursor.execute(query)
	ids_in_time_interval = cursor.fetchall()
	conn.close()
	print len(ids_in_time_interval)
	for twe_id in ids_in_time_interval:
		twe_id = twe_id[0]
		print twe_id
		rc = getRetweetCount ( twe_id )
		if len(str(rc)) > 0:
			query = "update %s set RetweetCount_1week = %d where tweet_id = %d"%(rc, twe_id)
			print "RC: ", query
			conn = sqlite3.connect(db)
			cursor = conn.cursor()
			cursor.execute(query)
			cursor.fetchall()
			conn.commit()
			conn.close()
        '''
################################### Functions for Getting Followers and Followings of New Users ##################################

#updates Followers and Followings for a User AND the respective counts (Followers, Following, NumFollowers, NumFollowing)
def updateFollowerFollowings(dbpath, user_table = "users"):
	distinct = get_D_UsrID(dbpath,sn_table )
	conn = sqlite3.connect(dbpath)
	cursor = conn.cursor()
	query = "select Usr_ID from %s where Following is null or Followers is null"
	cursor.execute(query)
	distinct = cursor.fetchall()
	follower_cursor = -1
	friend_cursor = -1
	print "Starting @ %d"%(ind)
	print datetime.datetime.now() 

	while ind < len(distinct):
	#for i in distinct:
		i = distinct[ind][0] # Usr_ID
		APP_KEY = APP_KEYS[index]
		APP_SECRET = APP_SECRETS[index]
		OAUTH_TOKEN = OAUTH_TOKENS[index]
		OAUTH_TOKEN_SECRET = OAUTH_TOKEN_SECRETS[index]

		try:
			#twitter = Twython (APP_KEY, APP_SECRET)
			#auth = twitter.get_authentication_tokens()
			twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET) 
			friends = ""
			while (friend_cursor):
				following = twitter.get_friends_ids(id = i,cursor= friend_cursor)
				for ID in following['ids']:
					friends += str(ID) + " " 
				friend_cursor =  following["next_cursor"]
				num_checked += 1
			friends = friends[:-1]
			if len(friends) == 0:
				friends = "null"
			
			follow = ""
			while (follower_cursor):
				followers = twitter.get_followers_ids(id = i,cursor= follower_cursor)
				for ID in followers['ids']:
					follow += str(ID) + " " 
				follower_cursor =  followers["next_cursor"]
				num_checked += 1
			follow= follow[:-1]
			if len(follow) == 0:
				follow = "null"

			conn = sqlite3.connect(dbpath)
			cursor = conn.cursor()
			query = "UPDATE %s SET Following = '%s', Followers = '%s', NumFollowing = '%d',  NumFollowers = '%d' where Usr_ID = '%s'"% (sn_table, friends,follow, len(friends.split(" ")), len(follow.split(" ")), i)
			cursor.execute(query)
			#print query
			conn.close()
			print "____________________ %dth following and friends and their corresponding counts updated ________ %d" % (ind, i)
			follower_cursor = -1
			friend_cursor = -1

			ind+=1

		except Exception as e:
			print e
			if "429 (Too Many Requests)" in str(e):
				index += 1
				if index == len(APP_KEYS):
					index = 0
					print "sleepy time; pausing for 15 minutes for APP Keys to renew"
					print datetime.datetime.now()
					#time.sleep(910)
					print "App Rate Limits has been exceeded- we will wait for next runtime before running rest of followers and followings"
					return 
			elif "401 (Unauthorized)" in str(e):
				print "401 Unauthorized Error nulling %d________________Usr_ID:%d"%(ind,i)
				conn = sqlite3.connect(dbpath)
				cursor = conn.cursor()
				query = "UPDATE %s SET Following = 'null', Followers = 'null' where Usr_ID = '%s'"% (sn_table, i)
				cursor.execute(query)
				conn.commit()
				conn.close()
				ind+=1
			elif "404 (Not Found)" in str(e):
				print "404 Not Found Error nulling %d________________Usr_ID:%d"%(ind,i)
				conn = sqlite3.connect(dbpath)
				cursor = conn.cursor()
				query = "UPDATE %s SET Following = 'null', Followers = 'null' where Usr_ID = '%s'"% (sn_table, i)
				cursor.execute(query)
				conn.commit()
				conn.close()
				ind+=1
			else:
				print e

########## DEPRECATED FUNCTIONS ##########
#pulls followers and following ids from twitter
#returns tuple, with string of friends' ids first and then followers' ids 
#returns ("null","null") if there is an error
def get_followers_following(usr_id):
	index = 0
	print "GETTING FOLLOWERS AND FOLLOWING: " + str(usr_id)
	friend_cursor = -1
	follower_cursor = -1

	APP_KEY = APP_KEYS[index]
	APP_SECRET = APP_SECRETS[index]
	OAUTH_TOKEN = OAUTH_TOKENS[index]
	OAUTH_TOKEN_SECRET = OAUTH_TOKEN_SECRETS[index]
	while (1==1):
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
				followers = twitter.get_followers_ids(id = usr_id,cursor= follower_cursor)
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
				#global index
				index += 1
				if index == len(APP_KEYS):
					index = 0
					print "sleepy time - 15 minutes"
					print datetime.datetime.now()
					time.sleep(910)
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
############ END OF DEPRECATED FUNCTIONS ############

#updateRetweetCountOnIntervals("sql_db/tweetDB.sqlite", "tweets11_streaming","tweets11_topics")
#exit()
updateRetweetCountOnIntervals("sql_db/tweetDB.sqlite","tweets11_streaming", "tweets11_topics")
#db = "tweets.sqlite"
#table = "tweets10_streaming"
try:
	timestart = datetime.datetime.now()
	print "Starting Scheduler @ ", timestart
	sched = BlockingScheduler()
	#sched.add_job(classify_and_model, 'interval', args=("tweets.sqlite", "tweets10_streaming"), minutes = 15)
	#sched.add_job(updateRetweetCountOnIntervals, 'interval', args=("tweets.sqlite", "tweets10_topics"), minutes = 15)
	sched.add_job(classify_and_model, 'interval', args=("sql_db/tweetDB.sqlite", "tweets11_streaming", "tweets11_topics"), minutes = 15)
	sched.add_job(updateRetweetCountOnIntervals, 'interval', args=("sql_db/tweetDB.sqlite", "tweets11_streaming","tweets11_topics"), hours = 1)
	sched.add_job(updateFollowerFollowings, 'interval', args=("sql_db/tweetDB.sqlite", "users"), minutes=15)
	sched.start()

	#classify_and_model("sql_db/tweetDB.sqlite", "tweets11_streaming")
except KeyboardInterrupt as k:
	print k
	print "Time Program Started: " , timestart
	print "Stopped process", datetime.datetime.now()
except Exception as e:
	print "other Exception"
	print e
	print "Time Program Started: " , timestart
	print "Stopped process", datetime.datetime.now()


'''
####### Example of using preprocess function ####
db = "tweets.sqlite"
table = "tweets9_streaming"
last_acquired = "Wed Jun 15 16:13:17 +0000 2016"
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
'''
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
'''


