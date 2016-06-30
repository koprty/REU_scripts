from twython import Twython,TwythonError
import json
import time
import sqlite3

APP_KEYS = ['TSZyBWKsHZRBlvqrFag7FucuX','SXqFBvQ0ibQxJLzANwYYF1jcN','cNSOzpCmfS730QsIC8AC6fnVv']
APP_SECRETS = ['NNVeYdE9AICI1a4Ytkm4PHyY9KhwLehZItP0WiZUSLaZG9H2Ml','7Dz4eSTJumYpYnPWdgKitBN60OTFgREsp6OdiNY6C3ihT1OS2l','wPwcpAlVTYBWEqzYFWG6vsVi8YRzbY4XMC2Fe8DkD4DkRnIviz']
OAUTH_TOKENS = ['701759705421639681-nutlNGruF7WZjq0kXZUTcKVbrnXs3vD','701759705421639681-KcNn0T4hdVjVSq2NhiGagdFV5pgUNHa','258508177-BqAvmsMCK4vdfBVp5c0wIIyBB6nNrhtOWtbdM82O']
OAUTH_TOKEN_SECRETS =['3hhidOQwxTMyc5MTDsmhaplfGcK5xVzB83hFb07OMALXh','HPmY0P8q23KVYx8AKS8tuWpCOAj8TMxQ3BYD1nb7sVF5s','NWvnPLNLFrePW9dg9dYC9U0dhilZpbuI3TvkFdL8LrUgw']


# updates the Favorite and Retweet counts for each tweet
def getAllTweetIds(table = "posdab_tweets"):
	conn = sqlite3.connect("tweets.sqlite")
	cursor = conn.cursor()
	query = "select Tweet_ID from %s;"%table
	cursor.execute(query)
	r = cursor.fetchall()
	d = []
	for x in r:
		d.append(x[0])
	return d


#update counts of retweet and favorites into tweet
def UpdateCounts(id_list, table = "posdab_tweets"):
	index=0
	num_checked = 0
	rate_ex = 0
	#for tweet_id in id_list:
	i = 0
	j = 0 # 2155th
	while i < len(id_list):
		tweet_id = id_list[i]
		if index >= 3:
			if i > 0:
				i-=1
			print i
			print "Exceeded all app rate limits"
			time.sleep(900)
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
				tweet['Usr_Screename'] = result['user']['screen_name']
				tweet['Usr_Description'] = result['user']['description']
				
				tweet['FavoriteCount'] = int(result['favorite_count'])
				tweet['RetweetCount'] = int(result['retweet_count'])
				num_checked += 1

				print int(result['retweet_count']), int(result['favorite_count']) 
				if int(result['retweet_count']) > 0 or int(result['favorite_count']) > 0:
					print tweet_id
					conn = sqlite3.connect("tweets.sqlite")
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
				

alltweetids = getAllTweetIds("tweets9_posdab")
#alltweetids = getAllTweetIds()
UpdateCounts(alltweetids, "tweets9_posdab")
