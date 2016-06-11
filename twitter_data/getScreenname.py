import json
import csv
from xlsxwriter.workbook import Workbook


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
	
def separateScreennames(array):
	L = array[:len(array)/2]
	M = array[len(array)/2:]
	f = open ("first_half_yay.tsv", "w")
	for x in L:
		f.write(x + "\n")
	f.close()

	f2 = open ("second_half_yay.tsv", "w")
	for y in L:
		f2.write(y+ "\n")
	f2.close()

	
def separateDicts(dicts):
	L = dicts[:len(dicts)/2]
	M = dicts[len(dicts)/2:]
	f = open ("1half.xls", "w")
	for x in L:
		s = ""
		s += x["Usr_Screename"]
		s+= "\t" + x["Usr_Description"].encode("ascii", "ignore")
		f.write( s+ "\n")
	f.close()

	f2 = open ("2half.xls", "w")
	for y in L:
		s = ""
		s += y["Usr_Screename"]
		s+= "\t" + y["Usr_Description"].encode("ascii", "ignore")
		f2.write(s+ "\n")
	f2.close()




filename = "all_tweets_dict_fully_checked"

with open(filename) as file:
	twitterdata = json.load(file)
#s = getDistinctScreenames(filename)

separateDicts(twitterdata)



'''
M = getDistinctAndAll(filename)
#print  M[0]
print len(M[0])

print len(M[1])
'''