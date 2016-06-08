import re
from twython import Twython,TwythonError
import sqlite3
import json

def dict_factory(cursor, row):
      d = {}
      for ids,col in enumerate(cursor.description):
        d[col[0]] = row[ids]
      return d

conn = sqlite3.connect('tweets.sqlite')

tablename = "posdab_tweets"
sql_query = """select * from [{0}] """.format(tablename)

conn.row_factory = dict_factory
cur = conn.cursor()
cur.execute(sql_query)
twitterdata = cur.fetchall()
conn.close()



APP_KEYS = ['TSZyBWKsHZRBlvqrFag7FucuX','SXqFBvQ0ibQxJLzANwYYF1jcN','nkcpJtiZwqrcdEYVBYy7TvHm9']
APP_SECRETS = ['NNVeYdE9AICI1a4Ytkm4PHyY9KhwLehZItP0WiZUSLaZG9H2Ml','7Dz4eSTJumYpYnPWdgKitBN60OTFgREsp6OdiNY6C3ihT1OS2l','xZH27sxsjed2YADydR8q7xuIXvokLVZdPj1zR0VKZdr1y078o0']
OAUTH_TOKENS = ['701759705421639681-nutlNGruF7WZjq0kXZUTcKVbrnXs3vD','701759705421639681-KcNn0T4hdVjVSq2NhiGagdFV5pgUNHa','	258508177-544ZUJ5M4gdKW1t5F4DtmsJ2LeqyZujyFzIoSx0j']
OAUTH_TOKEN_SECRETS =['3hhidOQwxTMyc5MTDsmhaplfGcK5xVzB83hFb07OMALXh','HPmY0P8q23KVYx8AKS8tuWpCOAj8TMxQ3BYD1nb7sVF5s','qziIM5UgxVpit810HhlaQn6Zj8ZoYnKAlA2Stv18xQ2jd']

index=0
for tweet in twitterdata:
	if index > 3:
		break

	tweet_id = tweet['Tweet_ID']

	APP_KEY = APP_KEYS[index]
	APP_SECRET = APP_SECRETS[index]
	OAUTH_TOKEN = OAUTH_TOKENS[index]
	OAUTH_TOKEN_SECRET = OAUTH_TOKEN_SECRETS[index]

	try:

		twitter = Twython (APP_KEY, APP_SECRET)
		auth = twitter.get_authentication_tokens()
		twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET) 

		result = twitter.statuses.show(id=tweet_id)
		tweet['Usr_Screename'] = result['user']['screen_name']
		tweet['Usr_Description'] = result['user']['description']

	except Exception as e:
		index += 1



desc_keywords = ["smokeshop", "smoke shop", "business", "family owned", "family-owned","accessories","pipes","store","delivered","medical marijuana","free shipping"]
username_keywords = ["smoke shop", "smokeshop"]
scrnname_keywords = ["smokeshop", "smoke_shop"]
hashtag_keywords = ["smokeshop","vapeshop"]

def identifier(dict_arr=[]):
	for d in dict_arr:
		ss_count = 0
		screenname = ""
		if (d['Usr_Screename']!=None):
			screenname = d['Usr_Screename'].lower()
		username = d['Usrname'].lower()
		description= d['Usr_Description'].lower()
		hashtags = d['hashtags'].lower()
		for s_key in scrnname_keywords:
			if re.search(s_key,screenname):
				ss_count += 1
		for d_key in desc_keywords:
			if re.search(d_key, description):
				ss_count += 1
		for u_key in username_keywords:
			if re.search(u_key,username):
				ss_count += 1
		for h_key in hashtags:
			if re.search(h_key,hashtags):
				ss_count += 1
		file = ""
		if ss_count >= 2:
			file="smoke_shops.txt"
		else:
			file = "people.txt"
		t=open(file,"a+")
		t.write(d)
		t.write("\n")
		t.close()
identifier(twitterdata)

