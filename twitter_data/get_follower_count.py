import sqlite3
from twython import Twython,TwythonError
import time
import datetime

APP_KEYS = ['TSZyBWKsHZRBlvqrFag7FucuX','SXqFBvQ0ibQxJLzANwYYF1jcN','cNSOzpCmfS730QsIC8AC6fnVv','HEGsXHtuOLUlUNkUcBWMlLqaK',
'OtspVKgnB2UhNJSIXhf8QYIQO','7nTuFIXq6QmanfVx20OGXsL6N', 'PxNDGaWD6hUWLFpYffl8a83ZD', 'Du77cjeL7Q7hIrg89S62R6scu']
APP_SECRETS = ['NNVeYdE9AICI1a4Ytkm4PHyY9KhwLehZItP0WiZUSLaZG9H2Ml','7Dz4eSTJumYpYnPWdgKitBN60OTFgREsp6OdiNY6C3ihT1OS2l',
'wPwcpAlVTYBWEqzYFWG6vsVi8YRzbY4XMC2Fe8DkD4DkRnIviz','KeiDW2vmHIMUcUN9scHFYqYBlQg7K3LfOPinjtTA6cxbXyEve5', 'fv77emr7170r7uh4vSHLSfrnK4c8ZGmNZ88foysls3L15MRprZ',
'wDL6lXHThz2GubZmFEogZE9ZcDDD6mJBTrSiaonjUZ6J1vGuPa', 'gwrVjhgXosdQcL5cSXXmlC8QsI29g4vs9bJj6iWmemNyeMcjQe','e7cOLH4PDTf3bvgJuXg7xtLiW7M2oPimr2oP4wN8RANdXEP0gF']
OAUTH_TOKENS = ['701759705421639681-nutlNGruF7WZjq0kXZUTcKVbrnXs3vD','701759705421639681-KcNn0T4hdVjVSq2NhiGagdFV5pgUNHa',
'258508177-BqAvmsMCK4vdfBVp5c0wIIyBB6nNrhtOWtbdM82O','258508177-uQDYR2XTlrMpxfjwKYEIAaxarHkhZygl3n44Jz8k', '258508177-bHYLjetyZRNsulsFtI8oIBVJsrr3DxHdqhgxWzJ4',
'258508177-KHviBY6zYX7PjVBzKjfCbsDWuXSyBHOcfuo7HzyQ','701759705421639681-F84hDkTSfuG7KqJcqzk1rm88Izx1NUG','701759705421639681-O9d1FGk2LfGZ5FdR4wwlJpWCqf914MM']
OAUTH_TOKEN_SECRETS =['3hhidOQwxTMyc5MTDsmhaplfGcK5xVzB83hFb07OMALXh','HPmY0P8q23KVYx8AKS8tuWpCOAj8TMxQ3BYD1nb7sVF5s',
'NWvnPLNLFrePW9dg9dYC9U0dhilZpbuI3TvkFdL8LrUgw','jBItJWaPly3P8QUmCAbeix6n9JLjqEV4fNQkkrnYe4UJk', 'A7iKPr6haM4P5kbGTVzEmID4tyjm1tYCsUc8R8b61B6BR',
'2GyQgJizM5ipjr5OVC8iYEav7DlPWMjvwLTSKqVIPAMFI','4qVZZVzlayIHuXNb69yysjKZbR2Pg1z5gd7ItSfnbjgdE', 'J4ma0LYo1iQexcivSzuQcYUmtDteYYAzni5bT7hz5MSk4']




'''
target = open("followers.txt", "r")
snames = target.read()
snames = snames.split("\n")
'''
conn = sqlite3.connect("../rt_tweets.sqlite")
cursor = conn.cursor()
'''
for sname in snames:
	sn_f = sname.split("\t")
	sn = sn_f[0]
	f = sn_f[1]
	f = f.split(" ")
	num = len(f)
	print sn 
	print num
	if(f[0]!="Unauthorized" and f[0]!="NotFound"):
		query = "update users set NumFollowers=" + str(num) + " where Screename ='"+sn +"'"
		cursor.execute(query)
'''
#####################

def followers_friends(user, index = 0):
	if index >= 7:
		print "sleepy time"
		print datetime.datetime.now()
		time.sleep(860)
		index = 0

	APP_KEY = APP_KEYS[index]
	APP_SECRET = APP_SECRETS[index]
	OAUTH_TOKEN = OAUTH_TOKENS[index]
	OAUTH_TOKEN_SECRET = OAUTH_TOKEN_SECRETS[index]

	try:
		twitter = Twython (APP_KEY, APP_SECRET)
		auth = twitter.get_authentication_tokens()
		twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET) 

		result = twitter.show_user(user_id = user)

		fo_count = result["followers_count"]
		fr_count = result["friends_count"]
		return (fo_count,fr_count,index)

	except Exception as e:
		if "429 (Too Many Requests)" in str(e):
			print "\nchanging apps!\n"
			new_index = index + 1
			return followers_friends(user, new_index)
		elif "401 (Unauthorized)" in str(e):
			print "401 error"
			return ("NULL","NULL",index)
		elif "404 (Not Found)" in str(e):
			print "404 error"
			return ("NULL","NULL",index)
		else:
			print e
			return ("NULL","NULL",index)

'''
#query = "select Usr_ID from tweets9_users where NumFollowers is  null"
query = "select Usr_ID from tweets9_musers where NumFollowers is  null"
cursor.execute(query)
users = cursor.fetchall()
last_index = 0
print datetime.datetime.now()
for user in users:
	ffi = followers_friends(user[0], last_index)
	print ffi
	fo_count = ffi[0]
	fr_count = ffi[1]
	last_index = ffi[2]
	if (fo_count!="NULL" and fr_count!="NULL"):

		#query = "update tweets9_users set NumFollowers=" + str(fo_count) + ", NumFollowing=" + str(fr_count) + " where Usr_ID ='"+str(user[0]) +"'"
		query = "update tweets9_musers set NumFollowers=" + str(fo_count) + ", NumFollowing=" + str(fr_count) + " where Usr_ID ='"+str(user[0]) +"'"
		print query
		cursor.execute(query)
		conn.commit()
'''

query = "select Usr_ID from users where NumFollowers=5001;"
query = "select Distinct Usr_ID from totalusers where NumFollowing is Null or NumFollowers is null;"
cursor.execute(query)
users = cursor.fetchall()
last_index = 1
for user in users:
	ffi = followers_friends(user[0], last_index)
	print ffi
	fo_count = ffi[0]
	fr_count = ffi[1]
	last_index = ffi[2]
	if (fo_count=="NULL" or fr_count=="NULL"):
		fo_count = -1
		fr_count = -1	
	#query = "update tweets9_users set NumFollowers=" + str(fo_count) + ", NumFollowing=" + str(fr_count) + " where Usr_ID ='"+str(user[0]) +"'"
	query = "update totalusers set NumFollowers=" + str(fo_count) + ", NumFollowing=" + str(fr_count) + " where Usr_ID ='"+str(user[0]) +"'"
	print query
	cursor.execute(query)
	conn.commit()



#conn.commit()
conn.close()

