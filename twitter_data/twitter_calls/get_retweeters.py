from twython import Twython,TwythonError
import sqlite3
import time
#import tweepy

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

#conn = sqlite3.connect("../twitter_classifying/tweets.sqlite")
conn = sqlite3.connect("tweets.sqlite")
cursor = conn.cursor()

query = "select Tweet_ID from posdab_Tweets where Tweet_ID not in (select Tweet_ID from retweets);"
query = "select Tweet_ID from tweets9_mdab where Tweet_ID not in (select Tweet_ID from retweets);"
cursor.execute(query)
ids = cursor.fetchall()

#query = "drop table retweets;"
#cursor.execute(query)

#query = "create table retweets (Element_ID int, Tweet_ID int, Retweeter_ID int, Date text);"
#cursor.execute(query)


def get_retweeters(tweet_id, index):
	if index >= 7:
		print "sleepy time"
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
		#auth = tweepy.OAuthHandler(APP_KEY,APP_SECRET)
		#auth.set_access_token(OAUTH_TOKEN,OAUTH_TOKEN_SECRET)

		#twitter = tweepy.API(auth)

		result = twitter.get_retweets(id=tweet_id, count = 100, trim_user = 1)

		rters= []
		for r in result:	
			rtr = r['user']['id']
			date = r['created_at']
			tup = (rtr,date)
			rters.append(tup)

		return (rters, index)


	except Exception as e:
		if "429 (Too Many Requests)" in str(e):
			print "\nchanging apps!\n"
			new_index = index + 1
			return get_retweeters(tweet_id, new_index)
		elif "401 (Unauthorized)" in str(e):
			print "401 error"
			return ([],index)
		elif "404 (Not Found)" in str(e):
			print "404 error"
			return ([],index)
		else:
			print e
			return ([],index)

element_id = 0
last_index = 0
for tweet in ids:
	print tweet[0]
	rters_index = get_retweeters(tweet[0],last_index)
	retweeters = rters_index[0]
	last_index = rters_index[1]
	for rter in retweeters:
		query = "insert into retweets values (" + str(element_id) + ", "+ str(tweet[0])+ ", " + str(rter[0])+ ", '" + str(rter[1])+ "');"
		print query
		cursor.execute(query)
		conn.commit()
		element_id += 1

conn.commit()
conn.close()
