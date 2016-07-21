#
import json
import sqlite3
#import pyexcel as pe
import time
'''
This table structure is constructed differently from fillScreename.py / users table
				
CREATE TABLE followers
(Usr_ID INT, 
 Screename TEXT,
 Follower TEXT,
 Follower_ID TEXT,
 Category TEXT, 
 AccountCreated DATETIME , 
 Description TEXT,
 user_mentions TEXT
)


CREATE TABLE followings
(Usr_ID INT, 
 Screename TEXT,
 Following TEXT,
 Following_ID TEXT,
 Category TEXT, 
 AccountCreated DATETIME , 
 Description TEXT,
 user_mentions TEXT
)


each element in following represents the user following one person (this is extracted from users) 
'''

############################ From data in File Format ################################
filename = "all_tweets_dict_fully_checked"

# gets distinct user profiles stored in a file that can be json loaded (array of dictionaries)
def getDistinctUserProfiles( fname ):
	distinct = []
	distinctdictionaries ={}
	with open(fname) as file:
		twitterdata = json.load(file)

	for x in twitterdata:
		if not x['Usr_Screename'] == "":
			if not x['Usr_Screename'] in distinct:
				distinct.append(x['Usr_Screename'])
				if x['Usr_Screename'] in distinctdictionaries.keys():
					print x['Usr_Screename']
					exit()
				x["Category"] = "None"
				distinctdictionaries[x['Usr_Screename']]= x
	print len(distinctdictionaries)
	return distinctdictionaries

# reads an excel file and merges it into the associated dictionary where the dictionary key is the username and the value is the dictionary of the user profile 
def exceltodictionary(dataf, dic = {}):
	data = pe.get_records(file_name=dataf)
	for line in data:
		usrname = line['-1']
		dic[usrname]['Category'] = line['']
	return dic

#insert Following and Follower tables (one row = one connection) uses the dictionary from getDistinctUserProfiles
def fillConnection(distinctd, types = "Followings", datafile = "following.txt", users_table = "users"):
	if types != "Followings" and types != "Followers":
		print "fillConnection( distinctd) has optional inputs, and the first optional input has to be either:\n 1. Followers   \t      OR  2. Followings"
		exit()
	else:
		dbname = types
	conn = sqlite3.connect("tweets.sqlite")
	cursor = conn.cursor()
	i = 0
	distinctID = []
	for x in distinctd:
		distinctID.append(int(distinctd[x]["Usr_ID"]))
		#print userd
	user_col = types[:-1]
	if user_col == "Follower":
		user_col += "s"
	query = "select %s, Usr_ID, Screename from %s;" % (user_col, users_table)
	cursor.execute(query)
	result_follow = cursor.fetchall()
	for result in result_follow:
		r = result[0].split(" ")
		#print r
		for twitterid in r:
			if twitterid == "null" or len(twitterid) <= 0:
				break
			else:
				if int(twitterid) in distinctID:
					cols = ["Usr_ID", "Screename", 
							 types[:-1] , 	# Follower, Following
							 types[:-1]+"_ID", 						# Follower_ID, Following_ID
							 "Category",
							 "AccountCreated",
							 "Description"
							 ]
					# check to see if pair exists in database being modified
					quer = "select * from %s where Usr_ID = %s and %s = %s;" % (dbname, int(result[1]), cols[3], int(twitterid))
	
					cursor.execute(quer)
					indb = cursor.fetchall()
					if len(indb) == 0:
						# if not add to database
						columns = ", ".join(cols)
						# check to see if part of dataset from users table
						query = "select screename, Category, AccountCreated, Description from %s where Usr_ID = '%s';"%(users_table, twitterid)
						cursor.execute(query)
						data = cursor.fetchall()
						if len(data) > 0:
							screename = data [0][0]
							v = [result[1], result[2], 
									screename, twitterid, 
									data[0][1], # category
									data[0][2], # account created date
									data[0][3] # description
									]
							L = []
							for x in v:
								x = "'%s'" % x
								L.append(x)
							#print L
							# Insert row into the table
							values = ", ".join(L).decode("utf-8").encode("ascii", "ignore")
							query = 'INSERT INTO %s (%s) VALUES (%s)' % (dbname,columns, values)
							print query
							conn.execute(query)
							conn.commit()
							i+=1
							print "Added one more; row_" + str(i) + " has been added :D "
	conn.close()
	return i

############################ From DB ################################
# takes data from the database and turns it into a dictionary 
# not used in fill Connection from DB
def readFollowersFromDB(table= "followers", users_table = "users"):
	conn = sqlite3.connect("tweets.sqlite")
	cursor = conn.cursor()
	query = "select Usr_id, %s from %s "%(table, users_table)
	cursor.execute(query)
	data = cursor.fetchall()
	conn.close()
	d = {}
	for x in data:
		twitter_ids = x[1].split(" ")
		for t in twitter_ids:
			d[int(x[0])] = t
	return d

#fills following of all
def fillConnectionFromDB(types = "Followings",tablename = "Followings", users_table = "users",   database = "tweets.sqlite", users_table2 = None):
	if users_table2 == None:
		users_table2 = users_table

	
	user_col = types[:-1]
	if user_col == "Follower":
		user_col += "s"
	#pairs = readFollowersFromDB(user_col, users_table)

	#tweets.sqlite or postweets.sqlite
	conn = sqlite3.connect(database)
	print "Connecting to database: %s" % (database)
	cursor = conn.cursor()
	i = 0
	
	#query = "select %s, Usr_ID, Screename from %s where Usr_ID not in (select Distinct Usr_ID from followers) ;" % (user_col, users_table)
	query = "select %s, Usr_ID, Screename from %s;" % (user_col, users_table)

	#print query 
	time.sleep(10)
	cursor.execute(query)
	result_follow = cursor.fetchall()


	exceptions = ["Unauthorized", "NotFound"]
	distinctID = []
	for x in result_follow:
		if int(x[1]) not in result_follow:
			distinctID.append(int(x[1]))
	for result in result_follow:
		if result[0] != None and result[0].strip() not in exceptions and len(result[0]) != 0:
			
			r = result[0].split(" ")
			#print r

			for twitterid in r:
				if twitterid == "null" or twitterid == "None" or len(twitterid) <= 0:
					break
				else:
					#print "TwitterID:" + str(twitterid)
					#print result[1]
					
					if int(twitterid) in distinctID:
						cols = ["Usr_ID", "Screename", 
								 types[:-1] , 	# Follower, Following
								 types[:-1]+"_ID", 						# Follower_ID, Following_ID
								 "Category",
								 "AccountCreated",
								 "Description"
								 ]
						# check to see if pair exists in database being modified
						quer = "select * from %s where Usr_ID = %s and %s = %s;" % (tablename, int(result[1]), cols[3], int(twitterid))
		
						cursor.execute(quer)
						indb = cursor.fetchall()
						if len(indb) == 0:
							# if not add to database
							columns = ", ".join(cols)
							# check to see if part of dataset from users table and get all relevant data 
							query = "select screename, Category, AccountCreated, Description from %s where Usr_ID = '%s';"%(users_table2, twitterid)
							cursor.execute(query)
							print query
							data = cursor.fetchall()
							if len(data) > 0 and data[0][1] != None:
								screename = data [0][0]
								v = [result[1], result[2], 
										screename, twitterid, 
										data[0][1], # category
										data[0][2], # account created date
										
										]
								L = []
								for x in v:
									x = "'%s'" % x
									L.append(x)
								print data
								if data[0][3] != None:
									L.append('"""'+ data[0][3].strip("'").strip('"')+ '"""' ) # description )
								else:
									L.append("''")
								print L
								#print L
								# Insert row into the table
								values = ", ".join(L)#.decode("utf-8").encode("ascii", "ignore")
								query = 'INSERT INTO %s (%s) VALUES (%s)' % (tablename,columns, values)
								print query
								conn.execute(query)
								conn.commit()
								i+=1
								print "Added one more; row_" + str(i) + " has been added :D "
	conn.close()
	return i



#fillConnectionFromDB(types = "Followers", users_table = "users", database = "tweets.sqlite")
#fillConnectionFromDB(types = "Followings", users_table = "users",database = "tweets.sqlite")


#fillConnectionFromDB(types = "Followers", users_table = "tweets9_musers", database = "tweets.sqlite")
#fillConnectionFromDB(types = "Followings", users_table = "tweets9_musers", database = "tweets.sqlite")



fillConnectionFromDB(types = "Followers",tablename = "total_followers", users_table = "totalusers", database = "tweets.sqlite")
fillConnectionFromDB(types = "Followings",tablename = "total_followings", users_table = "totalusers", database = "tweets.sqlite")



#readFollowersFromDB("followers", "tweets9_users")
'''

filename = "all_tweets_dict_fully_checked"

dp = getDistinctUserProfiles(filename)
dp = exceltodictionary("data.xlsx", dp)
dp = exceltodictionary("part2.xlsx", dp)
#for x in dp.keys():
#	print dp[x]["Usr_Screename"] if len(dp[x]["Usr_Screename"]) > 0 else exit()
#insertScreenname(dp)


print fillConnection(dp)
time.sleep(30)
print fillConnection(dp, "Followers", "followers.txt")
'''


