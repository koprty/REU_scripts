import xlsxwriter
import sqlite3

workbook = xlsxwriter.Workbook("non_retweeted_users.xlsx")
user_ws = workbook.add_worksheet("Retweeted User Info")

conn = sqlite3.connect("../tweets.sqlite")
cursor = conn.cursor()
query = "select Usr_ID, Tweet_ID, Tweet_Text, RetweetCount from totalmdabs where Usr_ID in (select Usr_ID from totalusers) and RetweetCount<5"
cursor.execute(query)
tweets = cursor.fetchall()

query = "select Usr_ID, Screename, Category, NumFollowers from totalusers"
cursor.execute(query)
users = cursor.fetchall()

tweets.sort(key = lambda tup: tup[3], reverse = True)

tweets_w_user = []

for tweet in tweets:
	for user in users:
		if tweet[0] == user[0]:
			tup = (user[0],user[1],user[2],user[3],tweet[1],tweet[2],tweet[3])
			tweets_w_user.append(tup)

user_ws.write(0,0,"User ID")
user_ws.write(0,1,"Screename")
user_ws.write(0,2,"Category")
user_ws.write(0,3,"Number of Followers")
user_ws.write(0,4,"Tweet IDs")
user_ws.write(0,5,"Tweets")
user_ws.write(0,6,"Retweet Count")

row = 1
already_added = []
for x in tweets_w_user:
	if (x[0] not in already_added):
		for i in range(7):
			user_ws.write(row,i,x[i])
		row += 1
		already_added.append(x[0])
		for y in tweets_w_user:
			if x[0] == y[0] and x[4] != y[4]:
				user_ws.write(row,3,x[3])
				for i in range(4,7):
					user_ws.write(row,i,y[i])
				row += 1


workbook.close()