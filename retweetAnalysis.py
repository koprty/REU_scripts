import sqlite3

conn = sqlite3.connect("rt_tweets.sqlite")
cursor = conn.cursor()

# PRINTING TOP RETWEETS

def printTopRetweets():
	#greater than
	for n in [0]:#1,5,10,25,50,100,150,200,500, 1000,
		#query = "select count(*) from posdab_Tweets where %s+%s > %d " % ("FavoriteCount", "RetweetCount", n)
		#query = "select count(*) from posdab_Tweets where %s > %d " % ("FavoriteCount",  n)
		#query = "select DISTINCT Tweet_ID, Usr_Screename, RetweetCount, Tweet_Text, Usr_ID, TwtCreatedAt, Usr_URL, Media_URL, Media from tweets9_posdab where %s > %d " % ("RetweetCount",  n)
		#query = "select DISTINCT Tweet_ID, Usr_Screename, RetweetCount, Tweet_Text, Usr_ID, TwtCreatedAt, Usr_URL, Media_URL, Media from tweets9_mdab where %s > %d " % ("RetweetCount",  n)
		query = "select DISTINCT Tweet_ID, Usr_Screename, RetweetCount, Tweet_Text, Usr_ID, TwtCreatedAt, Usr_URL, Media_URL, Media from totalmdabs where %s > %d " % ("RetweetCount",  n)
		cursor.execute(query)
		result = cursor.fetchall()

	results = result
	results.sort(key = lambda tup:tup[2], reverse=True)
	L = []
	for x in results:
		query = "select Category, Usr_ID, NumFollowers, NumFollowing  from users where Usr_ID = '%s'"% (x[4])
		#query = "select Category, Usr_ID, NumFollowers, NumFollowing  from tweets9_users where Usr_ID = '%s'"% (x[4])
		cursor.execute(query)
		cate = cursor.fetchall()
		
		for z in cate:
			L.append(z[0])
		if len(cate) == 0:
			query = "select Category,  Usr_ID, NumFollowers, NumFollowing  from users where Usr_ID = '%s'"% (x[4])
			cursor.execute(query)
			cate = cursor.fetchall()
		if len(cate) == 0:
			cate = (("unknown", x[4], 0, 0), ())
		
		print "https://twitter.com/%s/%s/status/%d"%("#!",x[1], int(x[0])) , \
								"\t", x[2], "\t", x[3].strip(),"\t", str(cate[0][0] ) , "\t", \
								cate[0][1], "\t", cate[0][2], "\t", cate[0][3], "\t", x[5]

def printTweetsFromTopRetweets(thres):
	query = """select totalmdabs.Tweet_Text, totalmdabs.TwtCreatedAt, totalmdabs.RetweetCount, tu.Usr_ID, tu.Screename, totalmdabs.Tweet_ID from totalmdabs inner join totalusers as tu on tu.Usr_ID = totalmdabs.USr_ID where 
			Tweet_ID not in (select Tweet_ID from totalmdabs inner join totalusers on totalmdabs.Usr_ID = totalusers.Usr_ID where totalmdabs.RetweetCount > %d) 
			and tu.Usr_ID in (select Usr_ID from totalmdabs where RetweetCount > 5)  Order By Screename, RetweetCount DESC, TwtCreatedAt"""%(thres)

	query = """select totalmdabs.Tweet_Text, totalmdabs.TwtCreatedAt, totalmdabs.RetweetCount, tu.Usr_ID, tu.Screename, totalmdabs.Tweet_ID from totalmdabs inner join totalusers as tu on tu.Usr_ID = totalmdabs.USr_ID where 
			 tu.Usr_ID in (select Usr_ID from totalmdabs where RetweetCount > 5)  Order By Screename, RetweetCount DESC, TwtCreatedAt"""

	cursor.execute(query)
	tweetsFromTopRetweetUsers  = cursor.fetchall()

	for (t_txt, createdAt, rt_count, usrID, Screename, twe_id) in tweetsFromTopRetweetUsers:
		print "https://twitter.com/%s/%s/status/%d"%("#!",Screename, int(twe_id)) , \
							"\t", t_txt, "\t", rt_count, "\t", createdAt
	'''
	for x in tweetsFromTopRetweetUsers:
		s = ""
		for y in x:
			s += str(y) + "\t"
		print s
	'''


	conn.close()	



printTweetsFromTopRetweets(10)
