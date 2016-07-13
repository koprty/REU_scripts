import sqlite3
from datetime import datetime
import gensim
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
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

	d = corpora.Dictionary.load("topic_modeling/twitter/tweet_dict.dict")
	bow = d.doc2bow(stemmed_tokens)

	lda = models.ldamodel.LdaModel.load("topic_modeling/twitter/lda_9.ginsem")
	tweet_lda = lda.get_document_topics(bow,minimum_probability = .001)
	return tweet_lda


def getTopicModelsOfTweetsInDB(db, table, topic_table):
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	query = "select Tweet_Text, Tweet_ID, Usr_ID, Usr_Screename, TwtCreatedAt,  hashtags from %s "%(table)
	cursor.execute(query)
	twe = cursor.fetchall()
	print twe
	conn.close() 

	for (t_text, tweet_id, usr_id,screename, creationDate, hashtags) in twe:
		#run topic_model
		tweet_topic_dist = run_topic_model(t_text)
		top_topic = sorted(tweet_topic_dist,key=lambda x: x[1], reverse = True)[0]

		space_topics = ""
		for top in tweet_topic_dist:
			space_topics += (str(top[1]) + " ")
		space_topics = space_topics[:-1]
		#update database with new tweet
		t_text = t_text.strip("'").strip('"')
		hashtags = hashtags.strip('"').strip('"').replace('"',"").replace("'","")
		conn = sqlite3.connect(db)
		cursor = conn.cursor()
		query = " INSERT INTO %s (Tweet_ID, Usr_ID, Screename, hashtags, Tweet_Text, CreatedAt, DateChecked, TopTopic, SpaceTopic, Zero, One, Two, Three, Four, Five, Six, Seven, Eight) \
				 values (%s, %s, '%s', \"\"\"%s\"\"\", '%s', '%s', '%s', %s, '%s', " %(topic_table, tweet_id, usr_id, screename, hashtags,t_text, creationDate,datetime.now(),top_topic[0],space_topics)
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

db = "rt_tweets.sqlite"

getTopicModelsOfTweetsInDB(db, "posdab_tweets", "topics")
getTopicModelsOfTweetsInDB(db, "tweets9_mdab", "tweets9_topics")
getTopicModelsOfTweetsInDB(db, "totalmdabs", "total_topics")




