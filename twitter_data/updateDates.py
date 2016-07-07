import sqlite3
from datetime import datetime

conn = sqlite3.connect("tweets.sqlite")
cursor = conn.cursor()
def updateDates(table):
	#query = "select TwtCreatedAt, Tweet_ID from %s"%(table)
	#cursor.execute(query)
	#time_results = cursor.fetchall()
	#print time_results

	query = "select tweets9_streaming.TwtCreatedAt, %s.Tweet_ID from %s inner join tweets9_streaming on %s.Tweet_ID = tweets9_streaming.Tweet_ID "%(table,table,table)
	cursor.execute(query)
	#print query
	time_results = cursor.fetchall()
	if len(time_results) == 0:
		print time_results, "sucks"
		exit()
	for (created, tid) in time_results:
		
		try:
			print created
			print datetime.strptime(created, '%Y-%m-%d %X')
			created_time = datetime.strptime(created, '%Y-%m-%d %X')
		except ValueError:
			created_list = created.split(" ")
			created_list = created_list[:4] + created_list[5:]
			created = " ".join(created_list)
			#Mon Feb 29 18:00:33 2016
			print datetime.strptime(created, '%c')
			created_time = datetime.strptime(created, '%c')
		query = "update %s set TwtCreatedAt = '%s' where Tweet_ID = '%d'"%(table, created_time, tid)
		cursor.execute(query)
		#conn.commit()
		print query
	return 


#updateDates("posdab_Tweets")

updateDates("tweets9_mdab")
conn.close()