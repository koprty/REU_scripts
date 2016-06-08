from twython import Twython,TwythonError

import os
import time
from getScreenname import getDistinctScreenames

#APP_KEYS = ['TSZyBWKsHZRBlvqrFag7FucuX','SXqFBvQ0ibQxJLzANwYYF1jcN','nkcpJtiZwqrcdEYVBYy7TvHm9']
#APP_SECRETS = ['NNVeYdE9AICI1a4Ytkm4PHyY9KhwLehZItP0WiZUSLaZG9H2Ml','7Dz4eSTJumYpYnPWdgKitBN60OTFgREsp6OdiNY6C3ihT1OS2l','xZH27sxsjed2YADydR8q7xuIXvokLVZdPj1zR0VKZdr1y078o0']
#OAUTH_TOKENS = ['701759705421639681-nutlNGruF7WZjq0kXZUTcKVbrnXs3vD','701759705421639681-KcNn0T4hdVjVSq2NhiGagdFV5pgUNHa','	258508177-544ZUJ5M4gdKW1t5F4DtmsJ2LeqyZujyFzIoSx0j']
#OAUTH_TOKEN_SECRETS =['3hhidOQwxTMyc5MTDsmhaplfGcK5xVzB83hFb07OMALXh','HPmY0P8q23KVYx8AKS8tuWpCOAj8TMxQ3BYD1nb7sVF5s','qziIM5UgxVpit810HhlaQn6Zj8ZoYnKAlA2Stv18xQ2jd']

APP_KEYS = ['PxNDGaWD6hUWLFpYffl8a83ZD']
APP_SECRETS = ['gwrVjhgXosdQcL5cSXXmlC8QsI29g4vs9bJj6iWmemNyeMcjQe']
OAUTH_TOKENS = ['701759705421639681-F84hDkTSfuG7KqJcqzk1rm88Izx1NUG']
OAUTH_TOKEN_SECRETS =['4qVZZVzlayIHuXNb69yysjKZbR2Pg1z5gd7ItSfnbjgdE']

buzzwords = [

'weed', 'marijuana', 'vape', 'cannabis', 'rig', 'smoke', 'oil', 'wax', 'extracts',
'420', '710', 
'promo', 'sale', 'deal', 'deals', 'prices', 'buy', 'price', 'shop'

]

def user_timeline(screenname, index=0):
	APP_KEY = APP_KEYS[index]
	APP_SECRET = APP_SECRETS[index]
	OAUTH_TOKEN = OAUTH_TOKENS[index]
	OAUTH_TOKEN_SECRET = OAUTH_TOKEN_SECRETS[index]
	
	twitter =  Twython (APP_KEY, APP_SECRET)
	
	auth = twitter.get_authentication_tokens()
	
    #OAUTH_TOKEN = auth['oauth_token']
    #OAUTH_TOKEN_SECRET = auth['oauth_token_secret']

    
    #print OAUTH_TOKEN
	twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET) 
    #ACCESS_TOKEN = twitter.obtain_access_token()
	
    #print twitter.verify_credentials()
	#ACCESS_TOKEN = '701759705421639681-nutlNGruF7WZjq0kXZUTcKVbrnXs3vD'
    #twitter = Twython(APP_KEY, access_token = ACCESS_TOKEN)
	response = twitter.get_user_timeline(screen_name = screenname, count= 200, exclude_replies = True, include_rt = False)

	L = []
	for r in response:
		L.append(r['text'])
		'''
		d = {} 
		d['text'] = r['text']
		d['screenname'] = r['user']['screen_name']
		d['date'] = r['created_at']
		L.append(d)
		'''
	return L



'''
screennames = ['cannabis_net', 'VapePenUs','HeadShopNations','ReDTheStepChild',
'jenquisha',
'Cannaradio',
'official2piece',
'swannydabs710',
'WeedHistory',
'sillllyperson',
'EZabari98',
'TYPBankroll',
'AngelesCannabis',
'Ganoobies_SD',
'baldtatteddmme',
'HOLYASSNIPPLES',
'eyeswid3',
'thatdude415',
]
'''
smokeshops = []
ppl = []

def analyzeAllScreennames(sn_index = 0):
	print str(sn_index) + " SN_INDEX "
	ind = 0
	while sn_index < len(screennames):
		s = screennames[sn_index]
		try:
			texts = user_timeline(s,ind)
		except:
			ind+=1
			if ind > 0:
				print "OUR index = " + str(ind) + " "
				print "Exited because rate of all apps exceeded"
				print "waiting 15 minutes for next app windows"
				
				time.sleep(900)
				ind -=1
			analyzeAllScreennames(sn_index )
		mdab_count = 0
		nottext = 0
		for t in texts:
			contains_m_ref = False
			for bw in buzzwords:
				if bw in t.lower():
					contains_m_ref = True
			listwords = t.split()
			if len(listwords) == 1 and "http" in listwords[0]:
				nottext += 1
			if contains_m_ref:
				mdab_count+=1

		if len(texts) > 0:
			if mdab_count*1.0 / (len(texts)-nottext) > .6:
				smokeshops.append(s)
				f = open ("smokeshops_d.txt", "a+")
				f.write(s + "\n")
				f.close()
				print "Smokie => " + s
			else:
				ppl.append(s)

				f = open ("people_d.txt", "a+")
				f.write(s + "\n")
				f.close()
				print "Person => " + s
			print mdab_count*1.0 / (len(texts)-nottext)
			print 
		else:
			print s + " is probably not a live twitter handle or has not tweeted ... :/"
		print "END of analysis of " + s + " of SN_INDEX=" + str(sn_index) + "\n"
		sn_index += 1

def analyzeOneScreenname(s):
	texts = user_timeline(s)
	

	mdab_count = 0
	nottext = 0
	for t in texts:
		contains_m_ref = False
		for bw in buzzwords:
			if bw in t.lower():
				contains_m_ref = True
		listwords = t.split()
		if len(listwords) == 1 and "http" in listwords[0]:
			nottext += 1
		if contains_m_ref:
			mdab_count+=1
	if len(texts) > 0:
		if mdab_count*1.0 / (len(texts)-nottext) > .6:
			print "Smokie => " + s
		else:
			print "Person => " + s
		print mdab_count*1.0 / (len(texts)-nottext)
		print 
	else:
		print s + " is probably not a live twitter handle or has not tweeted ... :/"



filename = "tweet_dict_fully_checked"
screennames = getDistinctScreenames(filename)
#analyzeOneScreenname("ElevatedRental")
#analyzeAllScreennames(sn_index = 0)
print len(screennames)
print ppl
print smokeshops


print screennames[171 + 180] 


