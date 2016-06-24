import sqlite3
import heapq

categories = ['individuals', 'shops', 'commercial_growers', 'service_providers', 'non-profits', 'news', 'interest_groups']

def retweets_favs(category):
	conn = sqlite3.connect("tweets.sqlite")
	cursor = conn.cursor()

	query = "select FavoriteCount,RetweetCount,Tweet_Text,Usrname from posdab_Tweets where Usr_ID in (select Usr_ID from users where category = '%s');" % (category)
	cursor.execute(query)
	fav_rt_result = cursor.fetchall()
	conn.close()
	return fav_rt_result

def average(r = []):
	tot = len(r) * 1.0
	rt = totals(r)[1]
	fv = totals(r)[0]
	return (fv/tot,rt/tot)
'''
def average_favs(r = []):
	tot = len(r) * 1.0
	s = total_favs(r)
	return s/tot
'''
def totals(r=[]):
	rt = sum([tup[1] for tup in r]) * 1.0
	f = sum([tup[0] for tup in r]) * 1.0
	return (f,rt)
'''
def total_favs(r=[]):
	return sum([tup[0] for tup in r]) * 1.0
'''
def above(count = 1, r= []):
	num_r = 0
	num_f = 0
	for tup in r:
		if tup[1] >= count:
			num_r += 1
		if tup[0] >= count:
			num_f += 1
	return (num_f,num_r)

def highest_fav(num =1, r= []):
	fav = sorted(r, key = lambda tup: tup[0], reverse = True)
	i = 0
	tups = []
	if num >1 :
		while (i < num):
			tup = (fav[i][0], fav[i][2],fav[i][3])
			tups.append(tup)
			i += 1
		return tups
	else:
		return (fav[0][0], fav[0][2],fav[0][3])

def highest_rt(num =1, r= []):
	rt = sorted(r, key = lambda tup: tup[1], reverse = True)
	i = 0
	tups = []
	if num >1 :
		while (i < num): 
	 		tup = (rt[i][1], rt[i][2],rt[i][3])
			tups.append(tup)
			i += 1
		return tups
	else:
		return (rt[0][1], rt[0][2],rt[0][3])
	

for c in categories:
	results = retweets_favs(c)
	avg = average(results)
	tot = totals(results)
	once = above(1, results)
	hfav = highest_fav(1,results)
	hrt = highest_rt(1,results)
	print
	print c
	print "Total Tweets: " + str(len(results)) + " || Total Retweets: " + str(tot[1]) + " || Total Favorites: " + str(tot[0])
	print "Average RTs: " + str(avg[1]) + " || Average Favorites: " + str(avg[0]) 
	print "Number of Tweets with one or more RT: " +str(once[1]) + " || Number of Tweets with one or more fav: " + str(once[0])
	print "Most Favorited Tweet: " + str(hfav[2]) + " '" + str(hfav[1]) + "' with " + str(hfav[0]) + " favorites"
	print "Most Retweeted Tweet: " + str(hrt[2]) + " '" + str(hrt[1]) + "' with " + str(hrt[0]) + " retweets"
'''
	avg_rts = average_rts(results)
	avg_favs = average_favs(results)
	tot_rts = total_rts(results)
	tot_favs = total_favs(results)
	print c + ": "
	print "Total Tweets: " + str(len(results)) + " || Total Retweets: " + str(tot_rts) + " || Total Favorites: " + str(tot_favs) + " || Average RTs: " + str(avg_rts) + " || Average Favorites: " + str(avg_favs) 
	'''