import cPickle
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from random import shuffle
import sqlite3

######## Open relevant pickle files ##########
count_vectorizer = cPickle.load(open('count_users.pickle','rb'))
SVC = cPickle.load(open('SVC_users.pickle','rb'))

#################### Predict data ################
#### Get Data ####

conn = sqlite3.connect("../tweets.sqlite")
cursor = conn.cursor()
query = "select Usr_Description, Usr_ID, Usr_Screename from tweets9_streaming;"
cursor.execute(query)
descripts = cursor.fetchall()
conn.close()

results = [ x[0] if x[0] != None and x[0] != "None" else "null" for x in descripts ]


####### Applying SVC Pickles ########
#Vectorize
data_vector = count_vectorizer.transform(results)

predictions =  SVC.predict(data_vector)
print len(predictions)
print list(predictions).count("positive")
print SVC.classes_

columns = ", ".join(["Usr_ID, Screename, Description, Category"])

p = 0
count = 0
while p < len(predictions):
	if predictions[p] == "positive":
		category = "individuals"
		conn2 = sqlite3.connect("../tweets.sqlite")
		cursor = conn2.cursor()
		query = "select * from tweets9_users where Usr_ID = %s;"%(str(descripts[p][1]))
		cursor.execute(query)
		user_not_indb = len(cursor.fetchall()) == 0
		conn2.close()
		if (user_not_indb):
			# insert username/category into the table
			values = [
				descripts[p][1],
				descripts[p][2],
				results[p],
				"individuals"
			    ]
			dbname = "tweets9_users"
			    
			values = ", ".join(["\"\"\"" + str(x) + "\"\"\"" for x in values])

			conn3 = sqlite3.connect("../tweets.sqlite")
			cursor = conn3.cursor()
			query = "INSERT INTO %s (%s) VALUES (%s) " % (dbname,columns, values) 
			print query
			count+=1
			print "added %dth! "%(count)
			cursor.execute(query)
			#cursor.commit()
			conn3.close()		
	p+=1




######### Using Test data for prediction (example/test) ###############
'''
####### Get data for Testing ########
conn = sqlite3.connect("../tweets.sqlite")
cursor = conn.cursor()
#query = "select screename, Description from users where category = 'individuals';"
query = "select Description from users where category = 'individuals';"
cursor.execute(query)
indi_result = cursor.fetchall()
conn.close()


conn2 = sqlite3.connect("../tweets.sqlite")
cursor = conn2.cursor()
#query = "select screename, Description from users where not category = 'individuals';"
query = "select Description from users where not category = 'individuals';"
cursor.execute(query)
notindi_result = cursor.fetchall()
conn2.close()

print len(indi_result) #2324
print len(notindi_result) #336

#values = []
individuals = [] 
for ind in indi_result:
	individuals.append(ind[0])
#	values.append(1)
others = [] 
for o in notindi_result:
	others.append(o[0])
#	values.append(0)

shuffle(individuals)
shuffle(others)


####### Apply Da Pickles ########
expected_V = (len(individuals)-300) *["positive"] + (len(others)-300) *["negative"]
vector_1 = count_vectorizer.transform(individuals[:-300] + others[:-300] )
# ~ high 90's%

vector_1 = count_vectorizer.transform(individuals[:] + others[:] )
expected_V = len(individuals) *["positive"] + len(others) *["negative"]
# ~ 89% 

print SVC.predict(vector_1)
print SVC.score(vector_1, expected_V)
print SVC.classes_
'''
