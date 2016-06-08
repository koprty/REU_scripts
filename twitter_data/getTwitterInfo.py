from twython import Twython,TwythonError
import json
import time


APP_KEYS = ['TSZyBWKsHZRBlvqrFag7FucuX','SXqFBvQ0ibQxJLzANwYYF1jcN','cNSOzpCmfS730QsIC8AC6fnVv']
APP_SECRETS = ['NNVeYdE9AICI1a4Ytkm4PHyY9KhwLehZItP0WiZUSLaZG9H2Ml','7Dz4eSTJumYpYnPWdgKitBN60OTFgREsp6OdiNY6C3ihT1OS2l','wPwcpAlVTYBWEqzYFWG6vsVi8YRzbY4XMC2Fe8DkD4DkRnIviz']
OAUTH_TOKENS = ['701759705421639681-nutlNGruF7WZjq0kXZUTcKVbrnXs3vD','701759705421639681-KcNn0T4hdVjVSq2NhiGagdFV5pgUNHa','258508177-BqAvmsMCK4vdfBVp5c0wIIyBB6nNrhtOWtbdM82O']
OAUTH_TOKEN_SECRETS =['3hhidOQwxTMyc5MTDsmhaplfGcK5xVzB83hFb07OMALXh','HPmY0P8q23KVYx8AKS8tuWpCOAj8TMxQ3BYD1nb7sVF5s','NWvnPLNLFrePW9dg9dYC9U0dhilZpbuI3TvkFdL8LrUgw']

def get_info():

	with open('tweet_dict') as file:
		twitterdata=json.load(file)
	index=0
	num_checked = 0
	rate_ex = 0
	for tweet in twitterdata:
		if index >= 3:
			"Exceeded all app rate limits"
			break

		tweet_id = tweet['Tweet_ID']

		APP_KEY = APP_KEYS[index]
		APP_SECRET = APP_SECRETS[index]
		OAUTH_TOKEN = OAUTH_TOKENS[index]
		OAUTH_TOKEN_SECRET = OAUTH_TOKEN_SECRETS[index]


		if (tweet['Usr_Screename']== None or tweet['Usr_Description']== None):
			try:

				twitter = Twython (APP_KEY, APP_SECRET)
				auth = twitter.get_authentication_tokens()
				twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET) 

				result = twitter.show_status(id=tweet_id)
				print result['user']['screen_name'] + " " + result['user']['description']
				tweet['Usr_Screename'] = result['user']['screen_name']
				tweet['Usr_Description'] = result['user']['description']
				num_checked += 1


			except Exception as e:
				if "429 (Too Many Requests)" in str(e):
					index += 1
				elif "404 (Not Found)" in str(e):
					print "404"
					tweet['Usr_Screename'] = ""
					tweet['Usr_Description'] = ""
					print "403"
				elif "403 (Forbidden)" in str(e):
					tweet['Usr_Screename'] = ""
					tweet['Usr_Description'] = ""
				else:
					print e
				rate_ex += 1
	if (num_checked == 0 and rate_ex ==0):
		with open("tweet_dict_fully_checked",'w') as fout:
			json.dump(twitterdata,fout)
	else:
		with open('tweet_dict','w') as fout:
			json.dump(twitterdata,fout)
		time.sleep(900)
		get_info()

get_info()

