from twython import Twython
from congress_members import govtrack_data
import os


APP_KEYS = ['TSZyBWKsHZRBlvqrFag7FucuX','SXqFBvQ0ibQxJLzANwYYF1jcN','nkcpJtiZwqrcdEYVBYy7TvHm9']
APP_SECRETS = ['NNVeYdE9AICI1a4Ytkm4PHyY9KhwLehZItP0WiZUSLaZG9H2Ml','7Dz4eSTJumYpYnPWdgKitBN60OTFgREsp6OdiNY6C3ihT1OS2l','xZH27sxsjed2YADydR8q7xuIXvokLVZdPj1zR0VKZdr1y078o0']
OAUTH_TOKENS = ['701759705421639681-nutlNGruF7WZjq0kXZUTcKVbrnXs3vD','701759705421639681-KcNn0T4hdVjVSq2NhiGagdFV5pgUNHa','	258508177-544ZUJ5M4gdKW1t5F4DtmsJ2LeqyZujyFzIoSx0j']
OAUTH_TOKEN_SECRETS =['3hhidOQwxTMyc5MTDsmhaplfGcK5xVzB83hFb07OMALXh','HPmY0P8q23KVYx8AKS8tuWpCOAj8TMxQ3BYD1nb7sVF5s','qziIM5UgxVpit810HhlaQn6Zj8ZoYnKAlA2Stv18xQ2jd']

def twitter_search(twitter_id, index = 0):
	
	

   	''' FIRST RUN... ran out of twitter searches... :/ stupid rate limits '''
	'''
    APP_KEY = 'TSZyBWKsHZRBlvqrFag7FucuX'
    APP_SECRET = 'NNVeYdE9AICI1a4Ytkm4PHyY9KhwLehZItP0WiZUSLaZG9H2Ml'
    OAUTH_TOKEN = '701759705421639681-nutlNGruF7WZjq0kXZUTcKVbrnXs3vD'
    OAUTH_TOKEN_SECRET = '3hhidOQwxTMyc5MTDsmhaplfGcK5xVzB83hFb07OMALXh'
	'''

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
	ACCESS_TOKEN = '701759705421639681-nutlNGruF7WZjq0kXZUTcKVbrnXs3vD'
    #ACCESS_TOKEN = '3hhidOQwxTMyc5MTDsmhaplfGcK5xVzB83hFb07OMALXh'
    #twitter = Twython(APP_KEY, access_token = ACCESS_TOKEN)

    #print twitter.get_home_timeline()
    #print (twitter.search(q='twitter'))

	response = twitter.get_user_timeline(screen_name = twitter_id)
    # gets 20 results
    
    #John Boozman -> LOL 
    #print response[0]
	L = []
	for r in response:
		d = {} 
		d['text'] = r['text']
		d['screenname'] = r['user']['screen_name']
		d['date'] = r['created_at']
		L.append(d)
	print L
	return L

#print (twitter_search("SenatorBurr"),2)


def findAllPosition (index =0, i = 0):
	masterL = []
	try:
		while i < len(govtrack_data):
			n = govtrack_data[i]
			print n["twitterID"]
			if n["twitterID"] != None and n["twitterID"] != "None":
				masterL.append(twitter_search(n["twitterID"], index))
			i += 1
	except Exception as e:
		if "429 (Too Many Requests)" in str(e):
			if (index == len(APP_KEYS)-1):
				print masterL
				print "OUR i = " + str(i)
				print "Exited because rate of all apps exceeded"
				return masterL
			else:
				index += 1
			print "i = " + str(i)
			findAllPosition(index,i)
		print masterL
		print (e)
	print masterL
	return masterL

def findAllPositions_DivideByParty (target_folder,limit, index =0, i = 0, labels=["republican", "democrat", "independent"]):
	masterL = []
	if i >= limit:
		print i
		return "done"
	try:
		n = govtrack_data[i]
		if n["party"].lower() == labels[1]:
			os.chdir("{0}/{1}".format(target_folder, labels[1]))					
		elif n["party"].lower() == labels[2]:
			os.chdir("{0}/{1}".format(target_folder, labels[2])	)				
		else: # things that arent categorized as republican or democrate
			#Independent
			os.chdir("{0}/{1}".format(target_folder, labels[2]))
	
		if n["twitterID"] != None and n["twitterID"] != "None":
			#masterL.append(twitter_search(n["twitterID"], index))

			#create file to contain comments of each politician
			

			twitter_comments = twitter_search(n["twitterID"], index)

			#create string with all the comments grabbed per person
			for comment in twitter_comments:
				file_data += comment+ " \n"
			txt_name = n["name"]+ ".txt"
			f = open(txt_name, "w")
			f.write(file_data)
			f.close

			
		findAllPositions_DivideByParty(index,i+1, labels, target_folder)
	except Exception as e:
		print e
		if "429 (Too Many Requests)" in str(e):
			if (index == len(APP_KEYS)-1):
				print masterL
				print "OUR i = " + str(i)
				print "Exited because rate of all apps exceeded"
				return "something happened... :( "
			else:
				index += 1
			print "i = " + str(i)
			findAllPosition(index,i)
		print masterL
		print (e)
	return "all have been reached"

def setup_folder(foldername, labels = []):
	# each label is a folder for each label
	for label in labels:
		if not os.path.exists("{0}/{1}".format(foldername, label)):
			os.makedirs("{0}/{1}".format(foldername, label))
	return
setup_folder("twitter_training", ["republican", "democrat", "independent"])
print findAllPositions_DivideByParty("twitter_training",1)
'''
x = []
i = 0
while i < len(govtrack_data):
	n = govtrack_data[i]
	
	if n["party"] not in x:
		x.append(n["party"])
	i+=1
print x
'''
'''
'Republican', 'Democrat', 'Independent'
'''

exit(0)



#findAllPositions_DivideByParty ()




