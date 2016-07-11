from sklearn.feature_extraction.text import TfidfVectorizer
import sqlite3
import xlsxwriter

wb = xlsxwriter.Workbook("tweets_similar_to_retweeted.xlsx")
ws = wb.add_worksheet()

conn = sqlite3.connect("../tweets.sqlite")
cursor = conn.cursor()

vect = TfidfVectorizer(min_df=1)

query = "select Tweet_ID, Tweet_Text, RetweetCount, TwtCreatedAt, Usr_ID from totalmdabs"
cursor.execute(query)
tweets_wo_users = cursor.fetchall()

query = "select Usr_ID, Screename, Category, NumFollowers, NumFollowing from totalusers"
cursor.execute(query)
users = cursor.fetchall()

conn.close()

tweets = []

for tweet in tweets_wo_users:
	for user in users:
		if tweet[4] == user[0]:
			tup = (tweet[0],tweet[1],tweet[2],tweet[3],user[0],user[1],user[2],user[3],user[4])
			tweets.append(tup)

tweets.sort(key = lambda tup: tup[2], reverse = True)

i = 1
row = 0
for tweet in tweets:
	if (tweet[2]>4):
		print "-----------------------------------------------------"
		print "Tweet: " + tweet[1]
		print "Retweet Count: " + str(tweet[2])

		#write to workbook - in order of tuple
		ws.write(row,0, "ORIGINAL TWEET")
		for k in range(len(tweet)):
			ws.write(row,k+1,tweet[k])
		row += 1
		j = i
		while (j <len(tweets)):
			tfidf = vect.fit_transform([tweet[1],tweets[j][1]])
			array = (tfidf*tfidf.T).A
			if (array[1][0]>.5):
				print array[1][0]
				print "Compared Tweet: " + tweets[j][1]
				print "Compared Tweet Retweet Count: " + str(tweets[j][2])
				ws.write(row,0,"SIMILAR TWEET: "+ str(array[1][0]))
				for k in range(len(tweets[j])):
					ws.write(row,k+1,tweets[j][k])
				row += 1
			j += 1
	i+=1

wb.close()