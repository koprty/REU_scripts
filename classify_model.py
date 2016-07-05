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
	tf = cPickle.load(open('../twitter_data/tweet_classifier/new_tf2.pickle','rb'))
	SVC = cPickle.load(open('../twitter_data/tweet_classifier/SVC2.pickle','rb'))
	vect = cPickle.load(open('../twitter_data/tweet_classifier/new_vect2.pickle','rb'))

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
	user_SVC = cPickle.load("twitter_date/user_classifier/SVC_users.pickle")
	user_vect = cPickle.load("twitter_date/user_classifier/count_users.pickle")

	v1 = user_vect.transform(user_desc)

	result = user_SVC.predict_proba(v1)

	return result[0][1] > .58257648005

def get_followers_following():
	pass

def classify_and_model():
	#Pulling Tweet_ID, Usr_ID, Screename, CreatedAt, Tweet_Text, and Usr_Description
	# other script doesnt get hashtags... :/ 
	# we will get hashtags from preprocess function
	'''
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	query = "select Tweet_ID, Usr_ID, Scrrename, CreatedAt, Tweet_Text, Usr_Description from %s"%(table)
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
		query = "insert into TABLE_NAME " + \
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
			#if not, run user classification
			if classify_user(usr_desc):
				#positive for individual, write to individuals table
				pass
			else:
				#negative for individual, write to non-individuals table
				pass
			#get following and followers
	return	


#sched = BlockingScheduler()
#sched.add_job(classify_and_model, 'interval', minutes = 15)
#sched.start()


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

#################################################
