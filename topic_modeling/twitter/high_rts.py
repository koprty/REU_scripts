import sqlite3
import topic_dist2


def high_rts_topic_model(num = 0):
	conn = sqlite3.connect("../../tweets.sqlite")
	cursor = conn.cursor()

	query = "select Tweet_Text from totalmdabs where RetweetCount>%s" %(num-1)
	cursor.execute(query)
	tweets = cursor.fetchall()
	conn.close()
	print len(tweets)
	#print tweets
	fname="%s_rts_or_more_from_total" %num
	t = open(fname + ".txt", "w")
	for tweet in tweets:
		t.write(tweet[0])
		t.write("\n")
	t.close()

	doc_bow = topic_dist2.doc_to_bow(fname+".txt")
	topic_dist2.topic_dist_2(doc_bow,fname)

high_rts_topic_model(5)
