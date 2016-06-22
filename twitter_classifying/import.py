import sqlite3
import json
conn = sqlite3.connect("tweets (1).sqlite")
cursor = conn.cursor()

query = "select Tweet_Text from posdab_Tweets;"
cursor.execute(query)
positive_result = cursor.fetchall()
conn.close()
#print positive_result
pos_result = []
for x in positive_result:
	pos_result.append(x[0])
# your all tweets is in pos_result


conn2 = sqlite3.connect("tweets (1).sqlite")
cursor = conn2.cursor()
negative_result = []
set_a_f = ["SET_A", "SET_B", "SET_C", "SET_D", "SET_E", "SET_F"]
for s in set_a_f:
	query = "select Tweet_Text from %s where Tweet_ID not in (select Tweet_ID from posdab_Tweets);" % s
	cursor.execute(query)
	negative_result = cursor.fetchall()
	query = "select Tweet_Text from %s where Tweet_ID in (select Tweet_ID from posdab_Tweets);" % s
	cursor.execute(query)
	positive_result = cursor.fetchall()
	all_results = []
	for x in positive_result:
		a = "positive\t"+x[0]
		all_results.append(a)
	for y in negative_result:
		a = "negative\t"+y[0]
		all_results.append(a)

	fname = s +"_tweets"
	with open(fname,"w") as fout:
		json.dump(all_results,fout)
#print negative_result
conn2.close()

neg_result = []
for y in negative_result:
	neg_result.append(y[0])

# positive tweet text in pos_result
# negative tweet text in neg_result

all_results = []
for x in pos_result:
	s = "positive\t"+x
	all_results.append(s)
for y in neg_result:
	s = "negative\t"+y
	all_results.append(s)

#with open("all_tweets","w") as fout:
#	json.dump(all_results,fout)



#side comments
#len(pos_result) + len(neg_result) = 15,324
# sets_a-f = 15,353
# 29 tweets dont match...  :/ 