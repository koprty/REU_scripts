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
from gensim import corpora, mod

conn = sqlite3.connect("tweets.sqlite")
cursor = conn.cursor()

def preprocess():
	pass

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

def classify_user():
	pass

def get_followers_following():
	pass

def classify_and_model():
	#assuming we've pulled Tweet_ID, Usr_ID, Screename, CreatedAt, hashtags, and Tweet_Text
	#preprocess
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
		query = ("insert into TABLE_NAME "
				 "(Tweet_ID, Usr_ID, Screename, hashtags, Tweet_Text, CreatedAt, DateChecked, "
				 "TopTopic, SpaceTopic, Zero, One, Two, Three, Four, Five, Six, Seven, Eight) "
				 "values (" + tweet_id + ", " + usr_id + ", '" + screename + "', '" + hashtags + "',"
				 " '" + tweet_text + "', '" + creationDate + "', '" + datetime.datetime.now() + "',"
				 " " + top_topic[0] + ", '" + space_topics + "', ")
		for top in tweet_topic _dist:
			query += top[1]
			if (top[0]!=8):
				query += ", "
			else:
				query += ");"
		cursor.execute()
		conn.commit()

		#see if user already in previous databases
			#if not, run user classification
			#get following and followers
	pass

sched = BlockingScheduler()
sched.add_job(classify_and_model, 'interval', minutes = 15)
sched.start()

