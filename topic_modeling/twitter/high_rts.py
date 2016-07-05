import sqlite3
import topic_dist2


def high_rts_topic_model(num = 0):
	conn = sqlite3.connect("../../twitter_classifying/tweets.sqlite")
	cursor = conn.cursor()

	query = "select Tweet_Text from posdab_Tweets where RetweetCount>%s" %(num-1)
	cursor.execute(query)
	tweets = cursor.fetchall()
	conn.close()

	print tweets
	fname="%s_rts_or_more" %num
	t = open(fname + ".txt", "w")
	for tweet in tweets:
		t.write(tweet[0])
		t.write("\n")
	t.close()

	doc_bow = topic_dist2.doc_to_bow(fname+".txt")
	topic_dist2.topic_dist_2(doc_bow,fname)

high_rts_topic_model(10)
