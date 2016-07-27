from twython import Twython,TwythonError
import json
import time
import sqlite3
import datetime
import numpy as np
import scipy.stats as stats
import pylab as pl
import matplotlib.pyplot as plt


APP_KEYS = ['TSZyBWKsHZRBlvqrFag7FucuX','SXqFBvQ0ibQxJLzANwYYF1jcN','cNSOzpCmfS730QsIC8AC6fnVv']
APP_SECRETS = ['NNVeYdE9AICI1a4Ytkm4PHyY9KhwLehZItP0WiZUSLaZG9H2Ml','7Dz4eSTJumYpYnPWdgKitBN60OTFgREsp6OdiNY6C3ihT1OS2l','wPwcpAlVTYBWEqzYFWG6vsVi8YRzbY4XMC2Fe8DkD4DkRnIviz']
OAUTH_TOKENS = ['701759705421639681-nutlNGruF7WZjq0kXZUTcKVbrnXs3vD','701759705421639681-KcNn0T4hdVjVSq2NhiGagdFV5pgUNHa','258508177-BqAvmsMCK4vdfBVp5c0wIIyBB6nNrhtOWtbdM82O']
OAUTH_TOKEN_SECRETS =['3hhidOQwxTMyc5MTDsmhaplfGcK5xVzB83hFb07OMALXh','HPmY0P8q23KVYx8AKS8tuWpCOAj8TMxQ3BYD1nb7sVF5s','NWvnPLNLFrePW9dg9dYC9U0dhilZpbuI3TvkFdL8LrUgw']

APP_KEYS = ['e1BX8phYqSTD9wmovg8z6NLKa','SK9uJmmUCKh25Wyq5zdxpfOKa','6ZAS6VKXGKOde8M01LCBLQTJ4','3q7HU0E0qnlVcn5dRHksjTEDF']
APP_SECRETS = ['yqhUrjViagMiLGZSgugFdXCCMejuPjnCxJhqh9j0tJiHbba200','MLjU8z5Zym5PiEf8A3XqEbUGnoaFhHnc8sjAimcjPdD8Zpg8MR','4OQJi7pcoTswP1bjyCOQuMXTaWh1madWivBAl7cRlxv4gtxvhe','IY8M4lchjh8kbAYTwL4aPzgAbGZNAJjnxaztuwXYC5sNRgCyIA']
OAUTH_TOKENS = ['4859184461-PLPMivzdhoFYEboXdAXtkTBS75UjQm218pkbqij','4859184461-rwGMGntHvc6Y4a4UfEWjY6nOXnpARt72PulT7mb','4859184461-XwnnZEEtKZ1FnkEtwzORp9mUQHfoINHi9UIxwcg', '4859184461-r4ZVaLnUmbyjimB2nRd4G1QUg3xtOM2tsF7c3g9']
OAUTH_TOKEN_SECRETS =['Egj8zW8t5YHi7BRxHQf6rnKepKLjK5igfHZ6O8A5u2rsd','mcimxGrpL0RRDlfm5UsDKt7HjskWFjsymuoBePZqbaog9','B9cGqxfOTKJ5I1uetaSWy6efRS6vYohpYWzwC7ZBkVV7o','95noHaXiDFW4XbVDt9bbWg6VgHxikVqdCWqBMc6NQzT7k']

'''
consumer_key = "3CsAylH4X8nkGYkXNzjoJVFgv"
consumer_secret = "G0f9SGjf76E984ijG57mdwcv82fsuIxuaxBC0Pl2M6MzvtUrjM"
access_token = "4553384003-wUZPZCzFyFh58jZaJE1gXYiFgff7c4EBAjCBWeW"
access_token_secret = "GMAvmUmpcvzjywwoGhdqSkievTpykZ98ofV9LUQ6sUX9e"   

APP_KEYS.append(consumer_key)
APP_SECRETS.append(consumer_secret)
OAUTH_TOKENS.append(access_token)
OAUTH_TOKEN_SECRETS.append(access_token_secret)
'''

#update description, screename, and other relavent info into db
def get_userinfo_intoDB(db= "tweets.sqlite", table = "users"):
	index = 0
	#get users that need to be updated
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	#query = "select Usr_ID from tweets9_users where NumFollowers is  null"
	query = "select Usr_ID from %s where Description is null or Screename is null" %(table)
	query = "select Usr_ID from %s where utc_offset is null" %(table)

	cursor.execute(query)
	users = cursor.fetchall()
	result = ""
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
			'''
			fo_count = int(result["followers_count"])
			fr_count = int(result["friends_count"])
			screename = str(result["screen_name"])
			descript= str(result['description'])
			'''
			if (result['utc_offset'] == None):
				utc = -1
			else:
				utc = int(result['utc_offset'])
			
			#query = "update %s set NumFollowers=%d, NumFollowing=%d, Screename ='%s', Description=\"\"\"%s\"\"\" where Usr_ID=%d;"%(table, fo_count, fr_count, screename, descript, usr_id)
			query = "update %s set utc_offset ='%d' where Usr_ID=%d;"%(table, utc, usr_id)
			cursor.execute(query)
			conn.commit()
			print i, utc
			i+=1
		except Exception as e:
			if "429 (Too Many Requests)" in str(e):
				print "\nchanging apps!\n"
				if index >= len(APP_KEYS)-1:
					print "sleepy time"
					print datetime.datetime.now()
					time.sleep(900)
					index = 0
				else:
					index = index + 1
				print index


				print len(APP_KEYS)
			elif "401 (Unauthorized)" in str(e):
				print "401 error"
			elif "403 (Forbidden)" in str(e):
				print "403 (Forbidden)"
			elif "404 (Not Found)" in str(e):
				print "404 error"
			else:
				print index, len(APP_KEYS)
				print e
				print result
	return
#get_userinfo_intoDB( table = "totalusers", db = "rt_tweets.sqlite")



# getting not positive dab tweets and their utc
def get_UTCinfo_intoStreamingDB(db= "tweets.sqlite", table = "users"):
	index = 0
	#get users that need to be updated
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	#query = "select Usr_ID from tweets9_users where NumFollowers is  null"
	query = "select Usr_ID from %s where Description is null or Screename is null" %(table)
	query = "select Usr_ID from %s where Tweet_ID not in (select DISTINCT Tweet_ID from total_topics) and ImpureQuery = 2" %(table)

	cursor.execute(query)
	users = cursor.fetchall()
	print len(users)

	result = ""
	i = 5604#2710 #46958 
	i = 26060
	while i < len(users):
		try:
			APP_KEY = APP_KEYS[index]
			APP_SECRET = APP_SECRETS[index]
			OAUTH_TOKEN = OAUTH_TOKENS[index]
			OAUTH_TOKEN_SECRET = OAUTH_TOKEN_SECRETS[index]
			

			twitter = Twython (APP_KEY, APP_SECRET)
			auth = twitter.get_authentication_tokens()
			twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET) 
			user = users[i]
			usr_id = int(users[i][0])

			result = twitter.show_user(user_id = user[0])
			'''
			fo_count = int(result["followers_count"])
			fr_count = int(result["friends_count"])
			screename = str(result["screen_name"])
			descript= str(result['description'])
			'''
			if (result['utc_offset'] == None):
				utc = -1
			else:
				utc = int(result['utc_offset'])
			
			#query = "update %s set NumFollowers=%d, NumFollowing=%d, Screename ='%s', Description=\"\"\"%s\"\"\" where Usr_ID=%d;"%(table, fo_count, fr_count, screename, descript, usr_id)
			query = "update %s set ImpureQuery ='%d' where Usr_ID=%d;"%(table, utc, usr_id)
			cursor.execute(query)
			conn.commit()
			print i, utc
			i+=1
		except Exception as e:
			if "429 (Too Many Requests)" in str(e):
				print "\nchanging apps!\n"
				if index >= len(APP_KEYS)-1:
					print "sleepy time"
					print datetime.datetime.now()
					time.sleep(800)
					index = 0
				else:
					index = index + 1
				print index


				print len(APP_KEYS)
			elif "401 (Unauthorized)" in str(e) or "403 (Forbidden)" in str(e) or "404 (Not Found)" in str(e):
				try:
					print "400's error"
					utc = -2
					query = "update %s set ImpureQuery ='%d' where Usr_ID=%d;"%(table, utc, usr_id)
					cursor.execute(query)
					conn.commit()
					print i, utc, "_"
					i+=1
				except Exception as e:
					if "429 (Too Many Requests)" in str(e):
						print "\nchanging apps!\n"
						if index >= len(APP_KEYS)-1:
							print "sleepy time"
							print datetime.datetime.now()
							time.sleep(800)
							index = 0
						else:
							index = index + 1
						print index

			
			else:
				print index, len(APP_KEYS)
				print e
				print result
	conn.close()
	return

#get_UTCinfo_intoStreamingDB(db= "rt_tweets.sqlite", table = "total_streaming")
#get_UTCinfo_intoStreamingDB(db= "rt_tweets.sqlite", table = "generaltweets_streaming")
#exit()
#get_userinfo_intoDB(table = "users")



#### with Accurate locale time
def convertUTCToLocale (datestring, utc_offset):
	#utc_offset is in seconds. We will divide to get the hour difference
	if utc_offset == None:
		return datestring
	utc_hours = utc_offset/3600
	timedelta = datetime.timedelta(hours = utc_hours)
	datestr = datetime.datetime.strptime(datestring, "%Y-%m-%d %H:%M:%S")
	datestr = datestr+timedelta
	return datetime.datetime.strftime(datestr, "%Y-%m-%d %H:%M:%S")


######### Time Analysis #######
def analyzeTime_locale(db, table , extension = "", color = "b", label = "", average=False, query = None, createdAt = "CreatedAt"):
	if len(extension) > 0:
		if extension[:4] != " and":
			extension = " where "+extension

	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	if query == None:
		query = "select  Tweet_ID, %s, totalusers.utc_offset from %s inner join totalusers on %s.Usr_ID = totalusers.Usr_ID where totalusers.Usr_ID = totalusers.Usr_ID "%(createdAt, table, table) + extension
	cursor.execute(query)
	#print query

	rs = cursor.fetchall()
	#print query
	print label, " : ", len(rs)
	L = []
	for (twe_id, created, utc) in rs:
		created = convertUTCToLocale(created, utc)
		#print created
		timeparse = int(created.split(" ")[1].split(":")[0])

		L.append(timeparse)
	result = []
	count = []
	for x in range(24):
		count.append((x, L.count(x)))
		result.append((x, L.count(x)) if not average else (x,L.count(x)*1.0/len(L)) )
	c = 0
	for y in count:
		c += y[1]
	#print count
	#print result
	ax = pl.subplot(111)
	lines = ax.plot([h[0] for h in result], [h[1] for h in result])
	pl.setp(lines, color=color,label=label)
	box = ax.get_position()
	#ax.set_position([box.x0, box.y0, box.width * 0.95, box.height])
	#ax.legend(loc='lower left', bbox_to_anchor=(.6, 0.03))
	ax.legend(loc='lower left', bbox_to_anchor=(.6, 0.7))
	conn.close()

	return ax




############################################### GENERAL BY PERCENTAGE Late Fri - Early Tues ###############################################
pl.clf()



analyzeTime_locale("generaltweets.sqlite", "GENERALTWEETS_STREAMING", createdAt = "TwtCreatedAt", \
					color = "m", label = "General Politics ", average = True,  \
					query = "select distinct Tweet_ID, TwtCreatedAt, ImpureQuery from total_streaming where not ImpureQuery = -1 and not ImpureQuery = 5 and Tweet_ID not in (select distinct Tweet_ID from total_topics) " )

'''ax =analyzeTime_locale("generaltweets.sqlite", "GENERALTWEETS_STREAMING", createdAt = "TwtCreatedAt", \
					color = "c", label = "Popular General Politics ", average = True,  \
					query = "select distinct Tweet_ID, TwtCreatedAt, ImpureQuery from total_streaming where not ImpureQuery = -1 and RetweetCount >= 5 and Tweet_ID not in (select distinct Tweet_ID from total_topics) " )
'''
analyzeTime_locale("rt_tweets.sqlite", "total_streaming", createdAt = "TwtCreatedAt", \
					color = "r", label = "Non M-Dab ", average = True,  \
					query = "select distinct Tweet_ID, TwtCreatedAt, ImpureQuery from total_streaming where not ImpureQuery = -1 and Tweet_ID not in (select distinct Tweet_ID from total_topics) " )

analyzeTime_locale("rt_tweets.sqlite", "total_topics", createdAt = "CreatedAt", \
					color = "b", label = "M-Dab Tweets  ", average = True, extension = " and utc_offset is not null and not utc_offset  = -1 " )

ax = analyzeTime_locale("rt_tweets.sqlite", "total_topics", createdAt = "CreatedAt", \
					color = "g", label = "Popular M-Dab Tweets  ", average = True, extension = " and utc_offset is not null and RetweetCount_1hour >=5")



ax.legend(loc='lower left', bbox_to_anchor=(.6, 0.03))
pl.title("Locale Time Analysis of General Tweets ")



pl.show()
print 
print 
exit()

########### BY NUMBER #########
pl.clf()
analyzeTime_locale("rt_tweets.sqlite", "total_topics", createdAt = "CreatedAt", \
					color = "b", label = "M-Dab Tweets  ", average = False, extension = " and utc_offset is not null and not utc_offset  = -1  " )

ax =analyzeTime_locale("rt_tweets.sqlite", "total_topics", createdAt = "TwtCreatedAt", \
					color = "m", label = "Non M-Dab ", average = False,  \
					query = "select distinct Tweet_ID, TwtCreatedAt, ImpureQuery from total_streaming where  not ImpureQuery = -1 and Tweet_ID not in (select distinct Tweet_ID from total_topics) " ) 

ax.legend(loc='lower left', bbox_to_anchor=(.4, 0.2))
pl.title("Locale Time Analysis of Tweets (#) ")

#pl.show()
################################

############################################### BY PERCENTAGE ###############################################
pl.clf()


analyzeTime_locale("rt_tweets.sqlite", "total_topics", createdAt = "CreatedAt", \
					color = "b", label = "M-Dab Tweets  ", average = True, extension = " and utc_offset is not null and not utc_offset  = -1 " )

ax = analyzeTime_locale("rt_tweets.sqlite", "total_topics", createdAt = "CreatedAt", \
					color = "g", label = "Popular M-Dab Tweets  ", average = True, extension = " and utc_offset is not null and RetweetCount_1hour >=5")


analyzeTime_locale("rt_tweets.sqlite", "total_streaming", createdAt = "TwtCreatedAt", \
					color = "r", label = "Non M-Dab ", average = True,  \
					query = "select distinct Tweet_ID, TwtCreatedAt, ImpureQuery from total_streaming where not ImpureQuery = -1 and Tweet_ID not in (select distinct Tweet_ID from total_topics) " )

ax =analyzeTime_locale("rt_tweets.sqlite", "total_streaming", createdAt = "TwtCreatedAt", \
					color = "m", label = "Popular Non M-Dab ", average = True,  \
					query = "select distinct Tweet_ID, TwtCreatedAt, ImpureQuery from total_streaming where not ImpureQuery = -1 and RetweetCount >= 5 and Tweet_ID not in (select distinct Tweet_ID from total_topics) " )
ax.legend(loc='lower left', bbox_to_anchor=(.4, 0.2))
pl.title("Locale Time Analysis of Tweets (#) ")

ax.legend(loc='lower left', bbox_to_anchor=(.6, 0.03))
pl.title("Locale Time Analysis of Tweets Grouped by RetweetCount(%) ")


'''
analyzeTime_locale("rt_tweets.sqlite", "total_topics", createdAt = "CreatedAt", \
					color = "g", label = "All M-Dab Tweets (Locale) ", average = True,  )
analyzeTime_locale("rt_tweets.sqlite", "total_topics", createdAt = "TwtCreatedAt", \
					color = "r", label = "All Non M-Dab Tweets", average = True,  \
					query = "select distinct Tweet_ID, TwtCreatedAt, ImpureQuery from total_streaming " ) 
'''					 
pl.show()
#########################################################################################################################



