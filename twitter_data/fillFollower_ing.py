import json
import sqlite3
from itertools import izip_longest, ifilter
import time

#reads a follower/following file and turnes it into a dictionary 
def readFollowerstoD (fname):
	f = open (fname, "r")
	dataread = f.read()
	d = {}
	linedata = dataread.split("\n")
	for x in linedata:
		twocolumns = x.split("\t")
		#print twocolumns
		if len(twocolumns) != 2:
			print twocolumns
			exit()
		d[twocolumns[0]] = twocolumns[1]
	f.close()
	return d

# takes the dictionary from readfollowers method and searches database for screenames and returns new dictionary with screennames alphabetized
def parseOutIdsNotInDataSet (d, columntype="followers"):
	newd = {}
	conn = sqlite3.connect("tweets.sqlite")
	cursor = conn.cursor()
	i = 0
	j = 0
	query = "select usr_id from users;" 
	cursor.execute(query)
	
	result_data = cursor.fetchall()
	idsinDB = []
	for x in result_data:
		idsinDB.append(str(int(x[0])).strip())
	print len(idsinDB)
	print idsinDB

	for x in d.keys():
		ids = d[str(x)].split(" ") 
		follow = []		
		for user_id in ids:
			#q += "usr_id = '%s' " % (user_id) + " or "
		#if q != "":
			#query = "select Screename from users where %s " % (q[:-4])

			if user_id in idsinDB:
				#print result_data[0][0]
				follow.append(user_id)
		follow = " ".join(follow)
		newd[x] = follow
		if len(follow) > 0:
			q = "UPDATE users set %s = \'%s\' where screename =\'%s\'" % (columntype, follow, x)
			print q
			cursor.execute(q)
			conn.commit()
			j+=1
		print i
		i+=1

	conn.close()
	print newd
	print j
	return newd

#given a dictionary where the screenname is the key to the value of a space separated list of screenames, 
#update each screen which this list of followers
def insertFollower_ing():
	pass


filename = "followers.txt"

dictF= readFollowerstoD(filename)

chunks = [dictF.iteritems()]*40
g = (dict(ifilter(None, v)) for v in izip_longest(*chunks))
#print list(g)
x = list(g)
print len(x)
i = 0
for d in x:
	result = parseOutIdsNotInDataSet (d)
	print i
	i += 1
	time.sleep(20)
#print dictF
print "hi we done :D "

'''
M = getDistinctAndAll(filename)
#print  M[0]
print len(M[0])

print len(M[1])
'''