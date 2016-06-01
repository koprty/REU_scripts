from twython import Twython,TwythonError
from congress_members import govtrack_data, govtrack_twitterID
import os
import time


APP_KEYS = ['TSZyBWKsHZRBlvqrFag7FucuX','SXqFBvQ0ibQxJLzANwYYF1jcN','nkcpJtiZwqrcdEYVBYy7TvHm9']
APP_SECRETS = ['NNVeYdE9AICI1a4Ytkm4PHyY9KhwLehZItP0WiZUSLaZG9H2Ml','7Dz4eSTJumYpYnPWdgKitBN60OTFgREsp6OdiNY6C3ihT1OS2l','xZH27sxsjed2YADydR8q7xuIXvokLVZdPj1zR0VKZdr1y078o0']
OAUTH_TOKENS = ['701759705421639681-nutlNGruF7WZjq0kXZUTcKVbrnXs3vD','701759705421639681-KcNn0T4hdVjVSq2NhiGagdFV5pgUNHa','	258508177-544ZUJ5M4gdKW1t5F4DtmsJ2LeqyZujyFzIoSx0j']
OAUTH_TOKEN_SECRETS =['3hhidOQwxTMyc5MTDsmhaplfGcK5xVzB83hFb07OMALXh','HPmY0P8q23KVYx8AKS8tuWpCOAj8TMxQ3BYD1nb7sVF5s','qziIM5UgxVpit810HhlaQn6Zj8ZoYnKAlA2Stv18xQ2jd']



################ Intermediary Function for getting all data ###############
# deprecated
# Not a very useful function any more (created to get an idea of how the data set would look like)
#This function uses the govtrack_data which is a variable of a list of dictionaries relating known politician twitter_screennames to their parties
#We have omitted independents as they are not clear indicators of liberal or conservative ideals and assumed all republicans shown generally conservative sentiment and democrats show generally libral sentiment
#appends all dictionaries of tweets of twitter_ids that are listed in the govtrack_data
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
	return masterL
############################## End of Intermediary Function #################################



################### Functions used in COLLECTING DATA ######################
#searches a specific twitter_id for its first 20 comments and returns a list of dictionaries containing the twitter_id with the text of the tweet and the date the tweet was published
# the index parameter merely chooses which twitter api keys to use (since there is a 180 call limit on the twitter data)
def twitter_search(twitter_id, index = 0):

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
	
	response = twitter.get_user_timeline(screen_name = twitter_id)
    # gets 20 results, by default

	L = []
	for r in response:
		d = {} 
		d['text'] = r['text']
		d['screenname'] = r['user']['screen_name']
		d['date'] = r['created_at']
		L.append(d)
	return L
#print (twitter_search("SenatorBurr"),2)

def findAllPositions_DivideByParty (training_folder, testing_folder, politician_data, index =0, i = 0, labels=["republican", "democrat"]):
	masterL = []
	target_folder = training_folder
	if i%5 ==0:
		target_folder = testing_folder
	if i >= len(politician_data) :
		print i
		return "Done" + " " + str(i)
	if index >= 3:
		print "OUR i = " + str(i)
		print "OUR index = " + str(index) + " " + target_folder
		print "Exited because rate of all apps exceeded"
		print "waiting 15 minutes for next app windows"
		time.sleep(900)
		index = 0
	n = politician_data[i]
	try:

		if n["party"].lower() == labels[0]:
			os.chdir("{0}/{1}".format(target_folder, labels[0]))					
		elif n["party"].lower() == labels[1]:
			os.chdir("{0}/{1}".format(target_folder, labels[1])	)				
		else: # things that arent categorized as republican or democrate
			#Independent
			
			#os.chdir("{0}/{1}".format(target_folder, labels[2]))

			#SKIP TO NEXT PERSON on the list
			return findAllPositions_DivideByParty( target_folder, politician_data, index, i+1, labels)

		if n["twitterID"] != None and n["twitterID"] != "None":
			#masterL.append(twitter_search(n["twitterID"], index))

			#create file to contain comments of each politician
			twitter_comments = twitter_search(n["twitterID"], index)
			if len(twitter_comments) <= 0:
				os.chdir("../..")
				politician_data.remove(n)
				return findAllPositions_DivideByParty( training_folder, testing_folder, politician_data, index, i, labels)
	
			file_data =""
			#create string with all the comments grabbed per person
			for comment in twitter_comments:
				file_data += comment["text"].encode("utf-8") + " \n"
				txt_name = comment["screenname"].encode("utf-8") +  ".txt"
				f = open(txt_name, "w")
				f.write(file_data)

				f.close()
		
		os.chdir("../..")
		return findAllPositions_DivideByParty( training_folder, testing_folder, politician_data, index, i+1, labels)
	except TwythonError as e:
		#     print "429 (Too Many Requests)" in str(e)
		if "429 (Too Many Requests)" in str(e) or "400 (Bad Request)," in str(e):
			if index > 3:
				print "exception caught with {0}".format(index)
			else:
				index += 1
		else:
			print str(e) + "____"
		os.chdir("../..")
		return findAllPositions_DivideByParty( training_folder, testing_folder, politician_data, index, i, labels)
	

def setup_folder(foldername, labels = []):
	# each label is a folder for each label
	for label in labels:
		if not os.path.exists("{0}/{1}".format(foldername, label)):
			os.makedirs("{0}/{1}".format(foldername, label))
	return

setup_folder("twitter_training", ["republican", "democrat"])
setup_folder("twitter_testing", ["republican", "democrat"])

nn = int(len(govtrack_twitterID)*.8)

training_data = govtrack_twitterID[360:nn]
testing_data = govtrack_twitterID[nn:]


#findAllPositions_DivideByParty("twitter_training",training_data)
findAllPositions_DivideByParty("twitter_training","twitter_testing",govtrack_twitterID)



