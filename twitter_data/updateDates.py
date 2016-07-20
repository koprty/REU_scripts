import sqlite3
from datetime import datetime
import time

def updateDates(table, streamer):
	conn = sqlite3.connect("tweets.sqlite")
	cursor = conn.cursor()
	#query = "select TwtCreatedAt, Tweet_ID from %s"%(table)
	#cursor.execute(query)
	#time_results = cursor.fetchall()
	#print time_results

	query = "select %s.TwtCreatedAt, %s.Tweet_ID from %s inner join %s on %s.Tweet_ID = %s.Tweet_ID "%(streamer, table,table,streamer,table,streamer)
	cursor.execute(query)
	#print query
	time_results = cursor.fetchall()
	if len(time_results) == 0:
		print time_results, "sucks"
		exit()
	for (created, tid) in time_results:
		
		try:
			#print created
			#print datetime.strptime(created, '%Y-%m-%d %X')
			created_time = datetime.strptime(created, '%Y-%m-%d %X')
		except ValueError:
			created_list = created.split(" ")
			created_list = created_list[:4] + created_list[5:]
			created = " ".join(created_list)
			#Mon Feb 29 18:00:33 2016
			#print datetime.strptime(created, '%c')
			created_time = datetime.strptime(created, '%c')
		query = "update %s set TwtCreatedAt = '%s' where Tweet_ID = '%d'"%(table, created_time, tid)
		cursor.execute(query)
		#conn.commit()
		print query
	conn.close()
	return 



def updateStreamerDates(streamer, streaming = True):
	#query = "select TwtCreatedAt, Tweet_ID from %s"%(table)
	#cursor.execute(query)
	#time_results = cursor.fetchall()2
	#print time_results
	if streaming:
		createdAt = "TwtCreatedAt"
	else:
		createdAt = "CreatedAt"
	query = "select %s, Tweet_ID from %s  "%(createdAt,streamer)
	cursor.execute(query)
	#print query
	time_results = cursor.fetchall()
	if len(time_results) == 0:
		print time_results, "sucks"
		exit()
	for (created, tid) in time_results:
		
		try:
			#print created
			#print datetime.strptime(created, '%Y-%m-%d %X')
			created_time = datetime.strptime(created, '%Y-%m-%d %X')
		except ValueError:
			created_list = created.split(" ")
			created_list = created_list[:4] + created_list[5:]
			created = " ".join(created_list)
			#Mon Feb 29 18:00:33 2016
			#print datetime.strptime(created, '%c')
			created_time = datetime.strptime(created, '%c')
		query = "update %s set %s = '%s' where Tweet_ID = '%d'"%(streamer,createdAt, created_time, tid)
		cursor.execute(query)
		conn.commit()
		print query
	return 

'''
conn = sqlite3.connect("server_tweet.sqlite")
cursor = conn.cursor()
#updateDates("posdab_Tweets")

#updateDates("tweets9_mdab", "tweets9_streaming")
updateStreamerDates("tweets10_streaming")
'''

conn = sqlite3.connect("../rt_tweets.sqlite")
cursor = conn.cursor()

#updateDates("tweets9_mdab", "tweets9_streaming")
#updateStreamerDates("tweets10_streaming")
updateStreamerDates("totalmdabs")
print "Resting after updating totalmdabs"
time.sleep(50)
updateStreamerDates("tweets9_mdab")
print "Resting after updating tweets9"
time.sleep(50)
updateStreamerDates("posdab_Tweets")
print "Done"

conn.close()

#updateDates("posdab_Tweets")
### updating topic table dates... change TwtCreated to Created At in Streaming function
'''
updateStreamerDates("total_topics")
conn.close()
'''