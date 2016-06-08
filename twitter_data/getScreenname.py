import json


def getDistinctScreenames(fname):
	distinct = []
	with open(fname) as file:
		twitterdata = json.load(file)

	for x in twitterdata:
		if not x['Usr_Screename'] == "":
			if not x['Usr_Screename'] in distinct:
				distinct.append(x['Usr_Screename'])
	return distinct
	
def getDistinctAndAll(fname):
	L = []
	distinct = []
	with open(fname) as file:
		twitterdata = json.load(file)

	for x in twitterdata:
		if not x['Usr_Screename'] == "":
			L.append(x['Usr_Screename'])
			if not x['Usr_Screename'] in distinct:
				distinct.append(x['Usr_Screename'])
	return [L, distinct]
	


'''
filename = "tweet_dict_fully_checked"
M = getDistinctAndAll(filename)
#print  M[0]
print len(M[0])

print len(M[1])
'''