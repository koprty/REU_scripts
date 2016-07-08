from twython import Twython,TwythonError
import json
import time
import sqlite3
import datetime

APP_KEYS = ['TSZyBWKsHZRBlvqrFag7FucuX','SXqFBvQ0ibQxJLzANwYYF1jcN','cNSOzpCmfS730QsIC8AC6fnVv','HEGsXHtuOLUlUNkUcBWMlLqaK',
'OtspVKgnB2UhNJSIXhf8QYIQO',
'7nTuFIXq6QmanfVx20OGXsL6N', 
'PxNDGaWD6hUWLFpYffl8a83ZD', 
'Du77cjeL7Q7hIrg89S62R6scu', 'zssUc5yAchM6TTPs5nRbsMxsQ']

APP_SECRETS = ['NNVeYdE9AICI1a4Ytkm4PHyY9KhwLehZItP0WiZUSLaZG9H2Ml','7Dz4eSTJumYpYnPWdgKitBN60OTFgREsp6OdiNY6C3ihT1OS2l',
'wPwcpAlVTYBWEqzYFWG6vsVi8YRzbY4XMC2Fe8DkD4DkRnIviz','KeiDW2vmHIMUcUN9scHFYqYBlQg7K3LfOPinjtTA6cxbXyEve5', 'fv77emr7170r7uh4vSHLSfrnK4c8ZGmNZ88foysls3L15MRprZ',
'wDL6lXHThz2GubZmFEogZE9ZcDDD6mJBTrSiaonjUZ6J1vGuPa', 

'gwrVjhgXosdQcL5cSXXmlC8QsI29g4vs9bJj6iWmemNyeMcjQe',
'e7cOLH4PDTf3bvgJuXg7xtLiW7M2oPimr2oP4wN8RANdXEP0gF','zealQwvvv5N0r0Olja053Wd19VK59qeyCvTA45dXtq5OLkSFkZ']

OAUTH_TOKENS = ['701759705421639681-nutlNGruF7WZjq0kXZUTcKVbrnXs3vD','701759705421639681-KcNn0T4hdVjVSq2NhiGagdFV5pgUNHa',
'258508177-BqAvmsMCK4vdfBVp5c0wIIyBB6nNrhtOWtbdM82O','258508177-uQDYR2XTlrMpxfjwKYEIAaxarHkhZygl3n44Jz8k', 
'258508177-bHYLjetyZRNsulsFtI8oIBVJsrr3DxHdqhgxWzJ4',
'258508177-KHviBY6zYX7PjVBzKjfCbsDWuXSyBHOcfuo7HzyQ',
'701759705421639681-F84hDkTSfuG7KqJcqzk1rm88Izx1NUG',
'701759705421639681-O9d1FGk2LfGZ5FdR4wwlJpWCqf914MM', '701759705421639681-xYAlZAI4x0dJhUEOe6hawOea1MbQc8o']

OAUTH_TOKEN_SECRETS =['3hhidOQwxTMyc5MTDsmhaplfGcK5xVzB83hFb07OMALXh','HPmY0P8q23KVYx8AKS8tuWpCOAj8TMxQ3BYD1nb7sVF5s',
'NWvnPLNLFrePW9dg9dYC9U0dhilZpbuI3TvkFdL8LrUgw','jBItJWaPly3P8QUmCAbeix6n9JLjqEV4fNQkkrnYe4UJk', 'A7iKPr6haM4P5kbGTVzEmID4tyjm1tYCsUc8R8b61B6BR',
'2GyQgJizM5ipjr5OVC8iYEav7DlPWMjvwLTSKqVIPAMFI','4qVZZVzlayIHuXNb69yysjKZbR2Pg1z5gd7ItSfnbjgdE', 
'J4ma0LYo1iQexcivSzuQcYUmtDteYYAzni5bT7hz5MSk4', 'vdsE88d7ptFvmH1yEZorLwnr7JQLvGz9dlAEETUJ4kdAH']

def get_D_UsrID(dbpath, table):
	conn = sqlite3.connect(dbpath)
	cursor = conn.cursor()
	#query = "select Distinct Usr_ID from %s "% table
	query = "select Distinct Usr_ID from %s where Following='null' or Followers = 'null' or Following is Null or Followers is null"% table
	cursor.execute(query)
	ids = cursor.fetchall()
	conn.close()
	print ids
	return ids

def get_following_to_db(dbpath, sn_table = "tweets9_users"):
	distinct = get_D_UsrID(dbpath,sn_table )

	index=0
	num_checked = 0
	rate_ex = 0
	ind = 0
	already_checked = False
	follower_cursor = -1
	friend_cursor = -1
	print "Starting @ %d"%(ind)
	print datetime.datetime.now() 

	while ind < len(distinct):
	#for i in distinct:
		i = distinct[ind][0]
		APP_KEY = APP_KEYS[index]
		APP_SECRET = APP_SECRETS[index]
		OAUTH_TOKEN = OAUTH_TOKENS[index]
		OAUTH_TOKEN_SECRET = OAUTH_TOKEN_SECRETS[index]

		try:
			#twitter = Twython (APP_KEY, APP_SECRET)
			#auth = twitter.get_authentication_tokens()
			twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET) 

			#friend_results = twitter.cursor(twitter.get_friends_ids, id = i, cursor= friend_cursor)
			 
			friends = ""
			while (friend_cursor):
				following = twitter.get_friends_ids(id = i,cursor= friend_cursor)
				for ID in following['ids']:
					friends += str(ID) + " " 
				friend_cursor =  following["next_cursor"]
				num_checked += 1
			friends = friends[:-1]
			if len(friends) == 0:
				friends = "null"
			
			follow = ""
			while (follower_cursor):
				followers = twitter.get_followers_ids(id = i,cursor= follower_cursor)
				for ID in followers['ids']:
					follow += str(ID) + " " 
				follower_cursor =  followers["next_cursor"]
				num_checked += 1
			follow= follow[:-1]
			if len(follow) == 0:
				follow = "null"

			conn = sqlite3.connect(dbpath)
			cursor = conn.cursor()
			query = "UPDATE %s SET Following = '%s' where Usr_ID = '%s'"% (sn_table, friends, i)
			cursor.execute(query)
			#print query
			print "____________________ %dth following updated ________ %d" % (ind, i)
			conn.commit()

			query = "UPDATE %s SET Followers = '%s' where Usr_ID = '%s' "% (sn_table, follow, i)
			cursor.execute(query)
			#print query
			conn.commit()
			conn.close()
			print "%dth follower updated_______________________  %d" %  (ind, i)
			print num_checked
			print
			follower_cursor = -1
			friend_cursor = -1
			ind+=1

		except Exception as e:
			print e
			if "429 (Too Many Requests)" in str(e):
				index += 1
				if index == len(APP_KEYS):
					index = 0
					print "sleepy time - 15 minutes"
					print datetime.datetime.now()
					time.sleep(910)
			elif "401 (Unauthorized)" in str(e):
				print "401 error"
				f = open("skipped.txt", "a")
				f.write("skipped %dth element, ID: %d\n"%(ind, i))
				f.write("__________________________________________"+str(datetime.datetime.now()) + "\n")
				f.close()
				print "skipped %d"%ind
				ind+=1
				time.sleep(1)
			elif "404 (Not Found)" in str(e):
				print "404 error"
				f = open("skipped.txt", "a")
				f.write("404: skipped %dth element, ID: %d \n"%(ind, i))
				f.write("__________________________________________"+str(datetime.datetime.now()) + "\n")
				f.close()
				print "404 skipped %d"%ind
				ind+=1
				time.sleep(1)
			else:
				print e
			rate_ex += 1

	print ind
	print num_checked
	print rate_ex

	'''
	if (num_checked != 0 or rate_ex !=0):
		print "sleepy time"
		time.sleep(900)
		get_following()
		'''


dbpath = "tweets.sqlite"
print len(get_D_UsrID(dbpath, table = "users"))
get_following_to_db(dbpath,sn_table = "users")


