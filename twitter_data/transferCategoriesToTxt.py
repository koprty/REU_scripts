'''
Script is written to write tweets by each category in separate files from the tweets database using the tables:
positivedabtweets
users
'''
import sqlite3

categories = ['individuals', 'shops', 'commercial_growers', 'service_providers', 'non-profits', 'news', 'interest_groups']



def transferTweetToFile(category, dbname = "tweets.sqlite", table1 = "positivedabtweets", table2 ="users"):
	conn = sqlite3.connect(dbname)
	cursor = conn.cursor()
	query = "select Tweet_Text From %s where Usr_ID in (select Usr_ID from %s where category = '%s');" % (table1, table2, category)
	s = ""
	i=0
	for row in cursor.execute(query):
		s+= row[0] + "\n"
		#print i
		i+=1

	
	f = open (category + ".txt", "w")
	f.write(s)
	f.close()
	return i

for c in categories:
	print c
	print transferTweetToFile(c)