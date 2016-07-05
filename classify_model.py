from apscheduler.schedulers.blocking import BlockingScheduler
import cPickle
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.svm import SVC

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

def run_topic_model():
	pass

def classify_user():
	pass

def get_followers_following():
	pass

def classify_and_model():
	#preprocess
	#classify as positive or negative (MAKE SURE TWEET IS IN LIST, e.g. ["this is the tweet"])
	if classify_mdab([tweet_text]):
		#run topic_model
		#update database with new tweet

		#see if user already in previous databases
			#if not, run user classification
			#get following and followers
	pass

sched = BlockingScheduler()
sched.add_job(classify_and_model, 'interval', minutes = 15)
sched.start()

