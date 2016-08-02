from twython import Twython,TwythonError
import json
import time
import sqlite3
from datetime import datetime 

print datetime.now()
APP_KEYS = ['e1BX8phYqSTD9wmovg8z6NLKa','SK9uJmmUCKh25Wyq5zdxpfOKa','6ZAS6VKXGKOde8M01LCBLQTJ4','3q7HU0E0qnlVcn5dRHksjTEDF']
APP_SECRETS = ['yqhUrjViagMiLGZSgugFdXCCMejuPjnCxJhqh9j0tJiHbba200','MLjU8z5Zym5PiEf8A3XqEbUGnoaFhHnc8sjAimcjPdD8Zpg8MR','4OQJi7pcoTswP1bjyCOQuMXTaWh1madWivBAl7cRlxv4gtxvhe','IY8M4lchjh8kbAYTwL4aPzgAbGZNAJjnxaztuwXYC5sNRgCyIA']
OAUTH_TOKENS = ['4859184461-PLPMivzdhoFYEboXdAXtkTBS75UjQm218pkbqij','4859184461-rwGMGntHvc6Y4a4UfEWjY6nOXnpARt72PulT7mb','4859184461-XwnnZEEtKZ1FnkEtwzORp9mUQHfoINHi9UIxwcg', '4859184461-r4ZVaLnUmbyjimB2nRd4G1QUg3xtOM2tsF7c3g9']
OAUTH_TOKEN_SECRETS =['Egj8zW8t5YHi7BRxHQf6rnKepKLjK5igfHZ6O8A5u2rsd','mcimxGrpL0RRDlfm5UsDKt7HjskWFjsymuoBePZqbaog9','B9cGqxfOTKJ5I1uetaSWy6efRS6vYohpYWzwC7ZBkVV7o','95noHaXiDFW4XbVDt9bbWg6VgHxikVqdCWqBMc6NQzT7k']

'''
APP_KEYS2 = ['TSZyBWKsHZRBlvqrFag7FucuX',
'SXqFBvQ0ibQxJLzANwYYF1jcN','cNSOzpCmfS730QsIC8AC6fnVv',
'HEGsXHtuOLUlUNkUcBWMlLqaK','OtspVKgnB2UhNJSIXhf8QYIQO',
'7nTuFIXq6QmanfVx20OGXsL6N', 'PxNDGaWD6hUWLFpYffl8a83ZD', 
'Du77cjeL7Q7hIrg89S62R6scu', 'zssUc5yAchM6TTPs5nRbsMxsQ']

APP_SECRETS2 = ['NNVeYdE9AICI1a4Ytkm4PHyY9KhwLehZItP0WiZUSLaZG9H2Ml',
'7Dz4eSTJumYpYnPWdgKitBN60OTFgREsp6OdiNY6C3ihT1OS2l','wPwcpAlVTYBWEqzYFWG6vsVi8YRzbY4XMC2Fe8DkD4DkRnIviz',
'KeiDW2vmHIMUcUN9scHFYqYBlQg7K3LfOPinjtTA6cxbXyEve5', 'fv77emr7170r7uh4vSHLSfrnK4c8ZGmNZ88foysls3L15MRprZ',
'wDL6lXHThz2GubZmFEogZE9ZcDDD6mJBTrSiaonjUZ6J1vGuPa', 'gwrVjhgXosdQcL5cSXXmlC8QsI29g4vs9bJj6iWmemNyeMcjQe',
'e7cOLH4PDTf3bvgJuXg7xtLiW7M2oPimr2oP4wN8RANdXEP0gF','zealQwvvv5N0r0Olja053Wd19VK59qeyCvTA45dXtq5OLkSFkZ']

OAUTH_TOKENS2 = ['701759705421639681-nutlNGruF7WZjq0kXZUTcKVbrnXs3vD',
'701759705421639681-KcNn0T4hdVjVSq2NhiGagdFV5pgUNHa','258508177-BqAvmsMCK4vdfBVp5c0wIIyBB6nNrhtOWtbdM82O',
'258508177-uQDYR2XTlrMpxfjwKYEIAaxarHkhZygl3n44Jz8k','258508177-bHYLjetyZRNsulsFtI8oIBVJsrr3DxHdqhgxWzJ4',
'258508177-KHviBY6zYX7PjVBzKjfCbsDWuXSyBHOcfuo7HzyQ','701759705421639681-F84hDkTSfuG7KqJcqzk1rm88Izx1NUG',
'701759705421639681-O9d1FGk2LfGZ5FdR4wwlJpWCqf914MM', '701759705421639681-xYAlZAI4x0dJhUEOe6hawOea1MbQc8o']

OAUTH_TOKEN_SECRETS2 =['3hhidOQwxTMyc5MTDsmhaplfGcK5xVzB83hFb07OMALXh',
'HPmY0P8q23KVYx8AKS8tuWpCOAj8TMxQ3BYD1nb7sVF5s','NWvnPLNLFrePW9dg9dYC9U0dhilZpbuI3TvkFdL8LrUgw',
'jBItJWaPly3P8QUmCAbeix6n9JLjqEV4fNQkkrnYe4UJk', 'A7iKPr6haM4P5kbGTVzEmID4tyjm1tYCsUc8R8b61B6BR',
'2GyQgJizM5ipjr5OVC8iYEav7DlPWMjvwLTSKqVIPAMFI','4qVZZVzlayIHuXNb69yysjKZbR2Pg1z5gd7ItSfnbjgdE', 
'J4ma0LYo1iQexcivSzuQcYUmtDteYYAzni5bT7hz5MSk4', 'vdsE88d7ptFvmH1yEZorLwnr7JQLvGz9dlAEETUJ4kdAH']

APP_KEYS += APP_KEYS2
APP_SECRETS += APP_SECRETS2
OAUTH_TOKENS += OAUTH_TOKENS2
OAUTH_TOKEN_SECRETS += OAUTH_TOKEN_SECRETS2
'''

# updates the Favorite and Retweet counts for each tweet
def getAllTweetIds(table = "posdab_tweets", extension = "", dbname="tweets.sqlite"):
	conn = sqlite3.connect(dbname)
	cursor = conn.cursor()
	query = "select Distinct Tweet_ID from %s "%(table) + extension
	cursor.execute(query)
	print query
	r = cursor.fetchall()
	print len(r)
	d = []
	for x in r:
		d.append(x[0])
	return d


#update counts of retweet and favorites into tweet
def UpdateCounts(id_list, table = "posdab_tweets", dbname = "tweets.sqlite"):
	index=0
	num_checked = 0
	rate_ex = 0
	#for tweet_id in id_list:
	i = 0
	j = 0# 189th
	while i < len(id_list):
		tweet_id = id_list[i]
		if index >= len(APP_KEYS):
			if i > 0:
				i-=1
			print i
			print "Exceeded all app rate limits, sleeping 15 minutes"
			print datetime.now()
			time.sleep(800)
			index = 0
		
		APP_KEY = APP_KEYS[index]
		APP_SECRET = APP_SECRETS[index]
		OAUTH_TOKEN = OAUTH_TOKENS[index]
		OAUTH_TOKEN_SECRET = OAUTH_TOKEN_SECRETS[index]
		tweet = {}

		if (1 == 1):
			try:
				twitter = Twython (APP_KEY, APP_SECRET)
				auth = twitter.get_authentication_tokens()
				twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET) 
				result = twitter.show_status(id=tweet_id)
				#print result['user']['screen_name'] + " " + result['user']['description']
				#tweet['Usr_Screename'] = result['user']['screen_name']
				#tweet['Usr_Description'] = result['user']['description']
				
				tweet['FavoriteCount'] = int(result['favorite_count'])
				tweet['RetweetCount'] = int(result['retweet_count'])
				num_checked += 1

				print int(result['retweet_count']), int(result['favorite_count']) 
				if int(result['retweet_count']) > 0 or int(result['favorite_count']) > 0:
					print tweet_id
					conn = sqlite3.connect(dbname)
					cursor = conn.cursor()
					query = "Update %s set FavoriteCount = %d, RetweetCount = %d where Tweet_ID = '%s'" % (table,int(result['favorite_count']),int(result['retweet_count']), tweet_id)
					print query
					cursor.execute(query)
					conn.commit()
					conn.close()
					print "Updated %dth :D "%(j)
					j+=1

			except Exception as e:
				if "429 (Too Many Requests)" in str(e):
					index += 1
					i-=1
					print "RAN OUT OF REQUEST, API APP KEY OVERLOAD ____________ CHANGING APP KEYS"
					
				elif "404 (Not Found)" in str(e):
					print "404"
					tweet['Usr_Screename'] = ""
					tweet['Usr_Description'] = ""
				elif "403 (Forbidden)" in str(e):
					print "403"
					tweet['Usr_Screename'] = ""
					tweet['Usr_Description'] = ""
				else:
					print e
				rate_ex += 1
		print "_______ + " + str(i) + "     "+ str(len(id_list))
		i+=1
	print j
	return j
				

alltweetids = getAllTweetIds("total_streaming", extension = " where Tweet_ID in (select Tweet_ID from total_topics)", dbname = "rt_tweets.sqlite")
#alltweetids = getAllTweetIds()

UpdateCounts(alltweetids, "total_streaming",dbname = "rt_tweets.sqlite")
