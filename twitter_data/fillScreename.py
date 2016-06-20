import json
import sqlite3
import re
import string
import pyexcel as pe
'''
Dependencies:
pip install pyexcel
(Depending on what data file you are reading off of):"
pip install pyexcel-xlsx
pip install pyexcel-xls


'''


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
	'''
	f = open (dataf, 'r')
	x = f.read()
	lines = x.split("\n")
	for line in lines:
		y = line.split("")
		'''
# takes a dictionary of dictionaries where the upper level key is the screenname matching the value of it to a corresponding dictionary 
#inserts to users database where follower and following key is the space separated list of ids
def insertScreenname ( distinctd ):
	'''
2
 (Usr_ID INT, 
 NumFollowers INT, 
 NumFollowing INT, 
 Category TEXT, 
 Followers TEXT , 
 Following TEXT, 
 AccountCreated DATETIME , 
 Description TEXT,
 user_mentions TEXT

'''
	conn = sqlite3.connect("tweets.sqlite")
	cursor = conn.cursor()
	dbname = "users"
	i = 0
	for x in distinctd:
		userd = distinctd[x]
		columns = ", ".join(["Usr_ID", "Screename", "NumFollowers", "NumFollowing", "Category", "Followers", "Following", "AccountCreated", "Description", "user_mentions"])
		v = [str(userd["Usr_ID"]), str(userd["Usr_Screename"]), str(userd["Usr_FollowingCount"]), str(userd["Usr_FollowersCount"]), str(userd["Category"]), "null", "null", "null", str(userd["Usr_Description"].encode("utf-8")), "null"]
		if userd["Usr_ID"] == 0 or len(str(userd['Usr_ID'])) <= 1:
			print userd["Usr_ID"]

		if len(v[-2]) == 0:
			v[-2] = "null"
		L = []
		for x in v:
			if len(x) == 0 or x == None or x == "":
				x = "null"
			x = "'%s'" % x.replace("'","")
			L.append(x)
		values = ", ".join(L).decode("utf-8").encode("ascii", "ignore")
		query = 'INSERT INTO %s (%s) VALUES (%s)' % (dbname,columns, values)
		
		conn.execute(query)
		#conn.commit()
		i+=1
		#print userd["Usr_Screename"]
		#print "Added one more; row_" + str(i) + " has been added :D "
	conn.close()
	return




filename = "all_tweets_dict_fully_checked"

dp = getDistinctUserProfiles(filename)
dp = exceltodictionary("data.xlsx", dp)
dp = exceltodictionary("part2.xlsx", dp)
#for x in dp.keys():
#	print dp[x]["Usr_Screename"] if len(dp[x]["Usr_Screename"]) > 0 else exit()
#insertScreenname(dp)

'''
M = getDistinctAndAll(filename)
#print  M[0]
print len(M[0])

print len(M[1])
'''