from twython import Twython,TwythonError
import json
import time
import sqlite3

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

#get_info()


#update description, screename, and other relavent info into db
def get_userinfo_intoDB(table):
	index = 0
	#get users that need to be updated
	conn = sqlite3.connect("tweets.sqlite")
	cursor = conn.cursor()
	#query = "select Usr_ID from tweets9_users where NumFollowers is  null"
	query = "select Usr_ID from users where Description is null or Screename is null"
	cursor.execute(query)
	users = cursor.fetchall()

	i = 0
	for user in users:
		try:
			APP_KEY = APP_KEYS[index]
			APP_SECRET = APP_SECRETS[index]
			OAUTH_TOKEN = OAUTH_TOKENS[index]
			OAUTH_TOKEN_SECRET = OAUTH_TOKEN_SECRETS[index]
			

			twitter = Twython (APP_KEY, APP_SECRET)
			auth = twitter.get_authentication_tokens()
			twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET) 

			usr_id = int(user[0])

			result = twitter.show_user(user_id = user[0])
			
			fo_count = int(result["followers_count"])
			fr_count = int(result["friends_count"])
			screename = str(result["screen_name"])
			descript= str(result['description'])
			
			query = "update %s set NumFollowers=%d, NumFollowing=%d, Screename ='%s', Description=\"\"\"%s\"\"\" where Usr_ID=%d;"%(table, fo_count, fr_count, screename, descript, usr_id)
			cursor.execute(query)
			conn.commit()
			print i
			i+=1
		except Exception as e:
			if "429 (Too Many Requests)" in str(e):
				print "\nchanging apps!\n"
				if index >= 7:
					print "sleepy time"
					print datetime.datetime.now()
					time.sleep(860)
					index = 0
				index = index + 1
			elif "401 (Unauthorized)" in str(e):
				print "401 error"
			elif "404 (Not Found)" in str(e):
				print "404 error"
			else:
				print e
	return
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



#conn.commit()
conn.close()

'''
get_userinfo_intoDB("users")
