from twython import Twython,TwythonError
import json
import time
import sqlite3
from datetime import datetime
import numpy as np
import scipy.stats as stats
import pylab as pl
import matplotlib.pyplot as plt

#2016-06-15 15:46:15
def getDayOfWeek(datestring, format = ""):
	newdate = datetime.strptime(datestring, '%Y-%m-%d %X')
	dayofweek = newdate.strftime("%a")
	return dayofweek
getDayOfWeek("2016-07-26 15:46:15")

days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
def drawDayAnalysisLine (db, query = "select distinct Tweet_ID, CreatedAt from total_topics where CreatedAt is not null ", average = True, color ='b', label = "All M-dabs tweets"):
	conn = sqlite3.connect(db)
	cursor = conn.cursor()
	#print query
	cursor.execute(query)
	data = cursor.fetchall()
	results = [getDayOfWeek(x[1]) for x in data]
	num_elements = len(results)
	print label, " : ", num_elements
	factor = 1
	if average:
		factor = factor * 1.0 / num_elements
	result = []
	for d in days:
		result.append((days.index(d), results.count(d) * factor))
	ax = pl.subplot(111)
	lines = ax.plot([h[0] for h in result], [h[1] for h in result])
	pl.setp(lines, color=color,label=label)
	box = ax.get_position()
	#ax.set_position([box.x0, box.y0, box.width * 0.95, box.height])
	#ax.legend(loc='lower left', bbox_to_anchor=(.6, 0.03))
	ax.legend(loc='lower left', bbox_to_anchor=(.6, 0.7))
	conn.close()
	return ax


drawDayAnalysisLine("rt_tweets.sqlite", color = "b", label = "All M-dab Tweets")
drawDayAnalysisLine("rt_tweets.sqlite", color = "g", label = "Popular M-dab Tweets", \
				query = "select  Tweet_ID, CreatedAt from total_topics where CreatedAt is not null and  RetweetCount_2day >= 5")
drawDayAnalysisLine("rt_tweets.sqlite", color = "r", label = "All D-dab Tweets", \
				query = "select  Tweet_ID, TwtCreatedAt  Tweet_ID from total_streaming where TwtCreatedAt is not null")
drawDayAnalysisLine("rt_tweets.sqlite", color = "m", label = "Popular D-dabTweets", \
				query = "select  Tweet_ID, TwtCreatedAt from total_streaming where TwtCreatedAt is not null and  RetweetCount >= 5")
pl.title(" Day Analysis for Tweets By Percents")
pl.show()

exit()

drawDayAnalysisLine("rt_tweets.sqlite", color = "b", label = "All M-dab Tweets", average = False)
drawDayAnalysisLine("rt_tweets.sqlite", color = "g", label = "Popular M-dab Tweets", \
				query = "select  Tweet_ID, CreatedAt from total_topics where CreatedAt is not null and  RetweetCount_2day >= 5", average = False)
drawDayAnalysisLine("rt_tweets.sqlite", color = "r", label = "All D-dab Tweets", \
				query = "select  Tweet_ID, TwtCreatedAt  Tweet_ID from total_streaming where TwtCreatedAt is not null", average = False)
drawDayAnalysisLine("rt_tweets.sqlite", color = "m", label = "Popular D-dabTweets", \
				query = "select  Tweet_ID, TwtCreatedAt from total_streaming where TwtCreatedAt is not null and  RetweetCount >= 5", average = False)
pl.title(" Day Analysis for Tweets By Number")
pl.show()