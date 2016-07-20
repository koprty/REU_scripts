import datetime # datetime, timedelta
import re
import sqlite3
import string
import time
import numpy as np
import scipy.stats as stats
import pylab as pl
import matplotlib.pyplot as plt

#### Not needed anymore #### 
##### Updating the old dataset's RCount from the posdab tables ########
def UpdateRetweetCountsOldDb(db, top_table, table):
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	query = "select Tweet_ID, RetweetCount from %s"%(table)
	cursor.execute(query)
	allTweetsRC =cursor.fetchall()
	i = 0
	for (twe_id, rc) in allTweetsRC:
		query = "update %s set RetweetCount_1week = %d, RetweetCount_2day = %d, RetweetCount_1day = %d, RetweetCount_1week = %d, RetweetCount_1hour = %d, RetweetCount_15min = %d where Tweet_ID = %d"%(top_table, rc, rc, rc, rc, rc, rc, twe_id)
		print query 
		cursor.execute(query)
		conn.commit()
		print i
		i+=1
#UpdateRetweetCountsOldDb("rt_tweets.sqlite", "total_topics", "totalmdabs")
#UpdateRetweetCountsOldDb("rt_tweets.sqlite", "tweets9_topics", "tweets9_mdab")
#UpdateRetweetCountsOldDb("rt_tweets.sqlite", "topics", "posdab_Tweets")

######################Analyze Unpopular Tweets
## we will define popular as having at least 5 retweets
### THESE FUNCTIONS USE THE RETWEETCOUNT FROM 1HOUR.... FROM THE OLD DATASET, THIS DOESNT CHANGE ANYTHING SINCE ALL THE RC COUNTS WILL BE THE SAME (SCRIPT TO UPDATE THEM WAS RUN THE SAME)

# get greater than or equal 5 retweet counts 
def popHighThres(db, top_table, color="b", label="Greater than or equal to %d, 'Popular'",low_thres = 5):
	conn = sqlite3.connect(db)
	cursor = conn.cursor() 
	query = "select TopTopic, Zero,  One, Two, Three, Four, Five, Six, Seven, Eight, Usr_ID from %s where RetweetCount_1hour >= %d"%(top_table, low_thres)
	cursor.execute(query)
	topicModels = cursor.fetchall()
	label=label%(low_thres)
	print label
	getStatistics (topicModels, color=color,label=label )
	conn.close()

# get unpopular tweets
def getUnpop(db, top_table, high_thres = 5, color="g",label="Lower than %d, 'Unpopular'"):
	conn = sqlite3.connect(db)
	cursor = conn.cursor() 
	query = "select TopTopic, Zero,  One, Two, Three, Four, Five, Six, Seven, Eight, Usr_ID from %s where RetweetCount_1hour < %d and RetweetCount_1hour >= 0"%(top_table, high_thres)
	cursor.execute(query)
	topicModels = cursor.fetchall()
	getStatistics (topicModels,color = color, label= label%(high_thres))
	conn.close()
#getUnpop("rt_tweets.sqlite", "total_topics")

#get all
def getAll(db, top_table, high_thres = 5, color="c",label="All Tweets"):
	conn = sqlite3.connect(db)
	cursor = conn.cursor() 
	query = "select TopTopic, Zero,  One, Two, Three, Four, Five, Six, Seven, Eight, Usr_ID from %s "%(top_table)
	cursor.execute(query)
	topicModels = cursor.fetchall()
	getStatistics (topicModels,color = color, label = label, linewidth = .5)
	conn.close()
#getUnpop("rt_tweets.sqlite", "total_topics")

##### Zero
# why so many tweets have 0 even though their user has lots of followers 
# Get tweets with RC count = 0  
# RC counts in the topic tables from the old database are all the same
def analyzeZeroTweets (db, top_table, user_table = "totalusers", thres = 0,color = 'r', extension="", label = "Zero"):
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	query = "select TopTopic, Zero,  One, Two, Three, Four, Five, Six, Seven, Eight, %s.Usr_ID from %s inner join %s on %s.Usr_ID = %s.Usr_ID where RetweetCount_1hour = %d "%(user_table, top_table, user_table, top_table, user_table, thres) + extension
	print query
	cursor.execute(query)
	# getting tweets retweeted zero topicModels
	# analyzing topic models of these tweets
	topicModels = cursor.fetchall()
	getStatistics (topicModels, color=color, label=label)
	conn.close()

def getStatistics (topicModels,p= plt,  color = "b", label = "", marker = "", linewidth=2.0):
	topTopics = [x[0] for x in topicModels]
	#get frequencies of Topic Models
	tt = []
	for y in range(9):
		tt.append( (y, topTopics.count(y)))
	# get averages for topic models
	sums = [0]*9
	for (TopTopic, Zero, One, Two, Three, Four, Five, Six, Seven, Eight, user_ID) in topicModels:
		sums[0] += Zero
		sums[1] += One
		sums[2] += Two
		sums[3] += Three
		sums[4] += Four
		sums[5] += Five
		sums[6] += Six 
		sums[7] += Seven
		sums[8] += Eight
	n = len(topTopics)
	averages = [(z, sums[z]/n) for z in range(9)]
	print n 
	#print "Sums: ", sums
	
	#print "Topic Models: ", tt
	#print "Averages: ", averages
	for a in averages:
		print a[0], "\t", a[1]
	sorted_avg = sorted(averages, key= lambda a:a[1], reverse = True)
	sorted_top_topicmodel = sorted(tt, key= lambda t:t[1], reverse = True)

	#print "Sorted Topic Models: ", sorted_top_topicmodel
	#print "Sorted Averages: ", sorted_avg

	#h = [av[1] for av in averages]
	#h = L
	#fit = stats.norm.pdf(h, np.mean(h), np.std(h))  #this is a fitting indeed
	ax = p.subplot(111)
	lines = ax.plot([h[0] for h in averages], [h[1] for h in averages])
	p.setp(lines, color=color,label=label, linewidth=linewidth)
	
	p.ylabel("Average Topic Distributions")
	p.xlabel("Topic Number")
	#shrink graph space to make room for legend
	box = ax.get_position()
	#ax.set_position([box.x0, box.y0, box.width * 0.95, box.height])
	#ax.legend(loc='lower left', bbox_to_anchor=(.6, 0.03))
	ax.legend(loc='lower left', bbox_to_anchor=(.4, 0.03))
	#pl.hist(,normed=True) 

#################### Lets look what percent of zero retweeted tweets have media (we will check this by looking and the corresponding streaming table) ######
def checkMedia (db, table, streamer, extension = "and total_topics.retweetCount_1week >= 0"):
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	query = """select count(*) from %s inner join %s on %s.Tweet_ID = %s.Tweet_ID
				where %s.Media is not null and not %s.Media = "None"
			"""%(table, streamer, table, streamer, streamer,streamer) + extension
	cursor.execute(query)
	#print query
	HasMedia = cursor.fetchall()[0][0]
	'''
	query = """select count(*) from %s inner join %s on %s.Tweet_ID = %s.Tweet_ID where %s.Tweet_ID is not null
			"""%(table, streamer, table, streamer, streamer) + extension
	'''
	query = """select count(*) from %s where Tweet_ID is not null """%(table ) + extension
	cursor.execute(query)

	#print query

	total = cursor.fetchall()[0][0]

	print "Has Media: \t\t %d/%d" %(HasMedia, total)
	print "Percentage Has Media", '\t\t\t', "%.5f"%(float(HasMedia*100.0/total))+" %"
	conn.close()




#plot line of topic distributions for all tweets retweeted more than 5 times
print "_________________ >= 5 - blue"
popHighThres("rt_tweets.sqlite", "total_topics")
#print "_________________ >= 1"
#popHighThres("rt_tweets.sqlite", "total_topics", color="c",low_thres = 1)
print 

#plot line of topic distributions for all tweets retweeted less than 5 times but 0 or more
print "_________________ < 5 - green"
getUnpop("rt_tweets.sqlite", "total_topics")
print 

#plot line of topic distributions for all tweets 
print "_________________ ALL - cyan"
getAll("rt_tweets.sqlite", "total_topics")
print 


#plot line of topic distributions for all tweets retweeted exactly 1 time
print "_________________  =0 - red "
analyzeZeroTweets("rt_tweets.sqlite", "total_topics", "totalusers" )

pl.title("Average Topic Distributions among Popular and Unpopular Tweets")
#pl.show()
pl.clf()

analyzeZeroTweets ("rt_tweets.sqlite", "total_topics", "totalusers", label = "Followers > 100", color = 'r', extension = "and totalusers.NumFollowers > 100" )
analyzeZeroTweets ("rt_tweets.sqlite", "total_topics", "totalusers", label = "Followers > 500", color = 'g', extension = "and totalusers.NumFollowers > 500")
analyzeZeroTweets ("rt_tweets.sqlite", "total_topics", "totalusers", label = "Followers > 1000", color = 'b', extension = "and totalusers.NumFollowers > 1000")
analyzeZeroTweets ("rt_tweets.sqlite", "total_topics", "totalusers", label = "Followers > 10000", color = 'c', extension = "and totalusers.NumFollowers > 1000")

pl.title("Average Topic Distributions Zero Retweeted Tweets ")
#pl.show()


print 
print 
print 
print 
print "Percentage of Medias ___________________________________________"
print "ALL"
checkMedia("rt_tweets.sqlite", "total_topics", "total_streaming") # >= 0 because we will exclude all retweet counts with negative values i.e. -1
print "Zero Retweeted Tweets"
checkMedia("rt_tweets.sqlite", "total_topics", "total_streaming" , "and total_topics.retweetCount_1week = 0 ")
print "UnPopular Retweeted Tweets (<5 but >=0 RT)"
checkMedia("rt_tweets.sqlite", "total_topics", "total_streaming" , "and total_topics.retweetCount_1week < 5 and total_topics.retweetCount_1week >=0")
print "Semi-Popular Retweeted Tweets (>0 RT)"
checkMedia("rt_tweets.sqlite", "total_topics", "total_streaming" , "and total_topics.retweetCount_1week > 0 ")



print "Popular Retweeted Tweets (5+ RT)"
checkMedia("rt_tweets.sqlite", "total_topics", "total_streaming" , "and total_topics.retweetCount_1week >= 5 ")



def printUserDataTopicZero(db, top_table, label = "Users", user_table = "totalusers", thres = 0,color = 'r', extension=""):
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	query = "select Tweet_ID, %s.Screename, Category, NumFollowers, NumFollowing,Tweet_Text, RetweetCount_1hour,  Tweet_ID,TopTopic, Zero,  One, Two, Three, Four, Five, Six, Seven, Eight from %s inner join %s on %s.Usr_ID = %s.Usr_ID where NumFollowers > %d "%(user_table, top_table, user_table, top_table, user_table, thres) + extension
	#print query
	cursor.execute(query)
	# getting tweets retweeted zero topicModels
	# analyzing topic models of these tweets
	topicModels = cursor.fetchall()
	#print topicModels
	#getStatistics (topicModels, color=color, label=label)
	i = 0
	for x in topicModels:
		i = 0
		for element in x:
			if i == 0:
				print "https://twitter.com/%s/None/status/%d"%("#!", int(element)), "\t",
			else:
				print element, "\t",
			i+=1
		print
	conn.close()
#printUserDataTopicZero("rt_tweets.sqlite", top_table = "total_topics", thres = 10000, extension = "Order By totalusers.Screename DESC, RetweetCount_1hour DESC")



def TopicsDistForZero(db, top_table, label = "Users", user_table = "totalusers", thres = 0,color = 'r', extension=""):
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	query = "select Distinct Tweet_ID, TopTopic, Zero,  One, Two, Three, Four, Five, Six, Seven, Eight, %s.Screename, Category, NumFollowers, NumFollowing,Tweet_Text, RetweetCount_1hour,  Tweet_ID from %s inner join %s on %s.Usr_ID = %s.Usr_ID where NumFollowers > 10000 "%(user_table, top_table, user_table, top_table, user_table) + extension
	#print query
	print query

	cursor.execute(query)
	# getting tweets retweeted zero topicModels
	# analyzing topic models of these tweets
	topicModels = cursor.fetchall()
	#print topicModels
	#getStatistics (topicModels, color=color, label=label)

	TopT = []
	i = 0
	for x in topicModels:
		TopT.append(x[1])
	Z = []
	for y in range(9):
		#AVERAGE
		#Z.append( (y, TopT.count(y)*1.0/len(TopT)))
		#JUST NUMBER OF TWEETS IN GENERAL
		Z.append( (y, TopT.count(y)))

	pl.clf()
	ax = pl.subplot(111)
	lines = ax.plot([h[0] for h in Z], [h[1] for h in Z])
	pl.setp(lines, color="r",label="Greater than 10k followers")


	####  > = 5k followers
	query = "select Distinct Tweet_ID, TopTopic, Zero,  One, Two, Three, Four, Five, Six, Seven, Eight, %s.Screename, Category, NumFollowers, NumFollowing,Tweet_Text, RetweetCount_1hour,  Tweet_ID from %s inner join %s on %s.Usr_ID = %s.Usr_ID where NumFollowers > 5000 "%(user_table, top_table, user_table, top_table, user_table) + extension
	#print query
	print query

	cursor.execute(query)
	# getting tweets retweeted zero topicModels
	# analyzing topic models of these tweets
	topicModels = cursor.fetchall()
	#print topicModels
	#getStatistics (topicModels, color=color, label=label)

	TopT = []
	i = 0
	for x in topicModels:
		TopT.append(x[1])
	Z = []
	for y in range(9):
		#AVERAGE
		#Z.append( (y, TopT.count(y)*1.0/len(TopT)))
		#JUST NUMBER OF TWEETS IN GENERAL
		Z.append( (y, TopT.count(y)))
	print Z

	ax = pl.subplot(111)
	lines = ax.plot([h[0] for h in Z], [h[1] for h in Z])
	pl.setp(lines, color='b',label="Greater than 5k followers ")

	######## Any number of followers (positive)
	query = "select Distinct Tweet_ID, TopTopic, Zero,  One, Two, Three, Four, Five, Six, Seven, Eight, %s.Screename, Category, NumFollowers, NumFollowing,Tweet_Text, RetweetCount_1hour,  Tweet_ID from %s inner join %s on %s.Usr_ID = %s.Usr_ID where NumFollowers >= 0 "%(user_table, top_table, user_table, top_table, user_table) + extension
	#print query
	print query

	cursor.execute(query)
	# getting tweets retweeted zero topicModels
	# analyzing topic models of these tweets
	topicModels = cursor.fetchall()
	#print topicModels
	#getStatistics (topicModels, color=color, label=label)

	TopT = []
	i = 0
	for x in topicModels:
		TopT.append(x[1])
	Z = []
	for y in range(9):
		#AVERAGE
		#Z.append( (y, TopT.count(y)*1.0/len(TopT)))
		#JUST NUMBER OF TWEETS IN GENERAL
		Z.append( (y, TopT.count(y)))
	print Z

	ax = pl.subplot(111)
	lines = ax.plot([h[0] for h in Z], [h[1] for h in Z])
	pl.setp(lines, color='g',label="All users ")


	pl.ylabel("Number of Zero Retweeted Tweets ")
	pl.xlabel("Top Topic Number")



	#shrink graph space to make room for legend
	box = ax.get_position()
	#ax.set_position([box.x0, box.y0, box.width * 0.95, box.height])
	#ax.legend(loc='lower left', bbox_to_anchor=(.6, 0.03))
	ax.legend(loc='lower left', bbox_to_anchor=(.4, 0.03))
	pl.title("Top Topics from Zero Retweeted Tweets")
	pl.show()
	conn.close()


#TopicsDistForZero("rt_tweets.sqlite", top_table = "total_topics", thres = 10000, extension = "and retweetCount_1hour = 0 Order By totalusers.Screename DESC, RetweetCount_1hour DESC")





#clear any graph data

######### Time Analysis #######
def analyzeTime(db, table, extension = "", color = "b", label = "", average=False):
	if len(extension) > 0:
		extension = " where "+extension

	conn = sqlite3.connect("rt_tweets.sqlite")
	cursor = conn.cursor()
	query = "select distinct Tweet_ID, CreatedAt from %s"%(table) + extension
	cursor.execute(query)
	rs = cursor.fetchall()
	L = []
	for (twe_id, created) in rs:
		timeparse = int(created.split(" ")[1].split(":")[0])
		L.append(timeparse)
	result = []
	for x in range(24):
		result.append((x, L.count(x)) if not average else (x,L.count(x)*1.0/len(L)))
		
	
	ax = pl.subplot(111)
	lines = ax.plot([h[0] for h in result], [h[1] for h in result])
	pl.setp(lines, color=color,label=label)
	box = ax.get_position()
	#ax.set_position([box.x0, box.y0, box.width * 0.95, box.height])
	#ax.legend(loc='lower left', bbox_to_anchor=(.6, 0.03))
	ax.legend(loc='lower left', bbox_to_anchor=(.7, 0.03))

	conn.close()

pl.clf()

### All Tweets
analyzeTime("rt_tweets.sqlite", "total_topics", extension = "RetweetCount_1hour >= 0", color = "g", label = "All Tweets")
### Popular Tweets
analyzeTime("rt_tweets.sqlite", "total_topics", extension = "RetweetCount_1hour >= 5", color = "r", label = "Popular Tweets")
### Zero Retweeted Tweets
analyzeTime("rt_tweets.sqlite", "total_topics", extension = "RetweetCount_1hour = 0", color = "b", label = "Zero Tweets")
pl.ylabel("Number of Tweets ")
pl.xlabel("Hour of Day")
#shrink graph space to make room for legend
pl.title("Time Analysis of Tweets Grouped by Retweet Count (#)")
pl.show()



#___________________________Average___________________________#
pl.clf()
### All Tweets
analyzeTime("rt_tweets.sqlite", "total_topics", extension = "RetweetCount_1hour >= 0", color = "g", label = "All Tweets", average = True)
### Popular Tweets
analyzeTime("rt_tweets.sqlite", "total_topics", extension = "RetweetCount_1hour >= 5", color = "r", label = "Popular Tweets", average = True)
### Zero Retweeted Tweets
analyzeTime("rt_tweets.sqlite", "total_topics", extension = "RetweetCount_1hour = 0", color = "b", label = "Zero Tweets", average = True)
pl.ylabel("Percent of Tweets ")
pl.xlabel("Hour of Day")
#shrink graph space to make room for legend
pl.title("Time Analysis of Tweets Grouped by Retweet Count (%) ")
pl.show()






