import tweepy
import sqlite3
import json
import pprint
import numpy
import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer

# manually matching the 23 that the finddb.py script does not match and sticks into the datbase
unmatched = ['amp smoke dabs all day but hey i guess thats drugs', 'medreleaf in excruciating pain  9gday mega dabbing narcos pleasehelpus mm marijuana','mp3 danagog x davido  your way from his soon to be released ep hookah dab danagog repping hkn muisc drops anot', 'nikkiallenpoes latest phillyhighlife marijuana column  virgin dabbers','this is why you dont do drugs boy tries dabs weed wax for the first time freaks out', 'im legit wondering when i d himprobably something about dabbing and smoking weed if it was recent', 'hugest dab i have ever seen  6 gram smoke', 'my goal in life is to smoke a blunt with 42 billclinton maybe dabs too', 'amp smoke dabs all day but hey i guess thats drugs', 'medreleaf in excruciating pain  9gday mega dabbing narcos pleasehelpus mm marijuana', 'losfelizdaycare dabbing with marijuana', 'dab oil', 'dab oil', 'check out and vaderextracts have awesome ovens and oil ommp 710 dabs extracts  medicate terps', 'im highcold dab', 'and thrillermasters performance   how you feeling man im hella thigh nigga dab','huffy glass dabstation glass concentrate dabbing station  18mm  via smokecartel','this is why you dont do drugs boy tries dabs weed wax for the first time freaks out', 'go panthers beat the broncos in the superbowl today i drew cam dabbing cannabis dab weed', 'glorious slabs of dabs by tinmanoil just beautiful in the sunlight  weed weedstagram 420 cannabis stone', 'hburtonracing dab is also a form of marijuana im sure you arent promoting weed but maybe lets all drop the dab slang', 'amp they talk bout weed like some experts like dude stfu like just walk out u annoying dab', 'vapes i smoke that']

tablenames = ["SET_A", "SET_B", "SET_C", "SET_D", "SET_E", "SET_F"]
#tablenames = ["SET_A"]
unmatched = [

['amp smoke dabs all day but hey i guess thats drugs', 'medreleaf in excruciating pain  9gday mega dabbing narcos pleasehelpus mm marijuana'],
['mp3 danagog x davido  your way from his soon to be released ep hookah dab danagog repping hkn muisc drops anot', 'nikkiallenpoes latest phillyhighlife marijuana column  virgin dabbers'],

['this is why you dont do drugs boy tries dabs weed wax for the first time freaks out', 'im legit wondering when i d himprobably something about dabbing and smoking weed if it was recent', 'hugest dab i have ever seen  6 gram smoke', 'my goal in life is to smoke a blunt with 42 billclinton maybe dabs too', 'amp smoke dabs all day but hey i guess thats drugs', 'medreleaf in excruciating pain  9gday mega dabbing narcos pleasehelpus mm marijuana', 'losfelizdaycare dabbing with marijuana', 'dab oil', 'dab oil', 'check out and vaderextracts have awesome ovens and oil ommp 710 dabs extracts  medicate terps', 'im highcold dab', 'and thrillermasters performance   how you feeling man im hella thigh nigga dab'],
['huffy glass dabstation glass concentrate dabbing station  18mm  via smokecartel'],
['this is why you dont do drugs boy tries dabs weed wax for the first time freaks out', 'go panthers beat the broncos in the superbowl today i drew cam dabbing cannabis dab weed', 'glorious slabs of dabs by tinmanoil just beautiful in the sunlight  weed weedstagram 420 cannabis stone', 'hburtonracing dab is also a form of marijuana im sure you arent promoting weed but maybe lets all drop the dab slang', 'amp they talk bout weed like some experts like dude stfu like just walk out u annoying dab', 'vapes i smoke that'],
[]

]


stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

'''remove punctuation, lowercase, stem'''
def normalize(text):
    return nltk.word_tokenize(text.lower().translate(remove_punctuation_map))




## convert sql query result into a dictionary
def dict_factory(cursor, row):
      d = {}
      for ids,col in enumerate(cursor.description):
        d[col[0]] = row[ids]
      return d




def getDatafromDB (z):
	#z = "positivedabtweets"
	conn = sqlite3.connect('tweets.sqlite')
	sql_query = """select * from [{0}] """.format(z)

	conn.row_factory = dict_factory
	cur = conn.cursor()
	cur.execute(sql_query)
	twitterdata = cur.fetchall()
	#print twitterdata[0].keys()
	newlist = sorted(twitterdata, key=lambda k: k['Tweet_ID']) 
	#print newlist
	L = []
	for x in newlist:
		L.append(x['Tweet_Text'])
	conn.close()
	return [L, newlist]

def DBcount(dbname):
	conn = sqlite3.connect('tweets.sqlite')
	conn.row_factory = dict_factory
	cur = conn.cursor()
	sql_query = """ select count(*) as count from {0} """.format(dbname)
	cur.execute(sql_query)
	n = cur.fetchone()
	conn.close()
	return n["count"]

def addDataToDB(dic, dbname):
	
	conn = sqlite3.connect('tweets.sqlite')
	conn.row_factory = dict_factory
	cur = conn.cursor()
	columns = ', '.join(dic.keys())
	placeholders = ':'+', :'.join(dic.keys())
	sql_query = 'INSERT INTO %s (%s) VALUES (%s)' % (dbname,columns, placeholders)
	cur.execute(sql_query, dic)
	conn.commit()
	print sql_query
	print str(dic["element_id"]) + " was added to db: "  + dbname 
	conn.close()



dbname = str(raw_input("Write stuff into already created database (type tablename if yes; 'n' if no )\n"))
if dbname == "n":
      exit()

#dbname = "positivedabtweets"
o = 1
index = 0
counts = DBcount(dbname)
while index < len(tablenames) -1 : #set_F is all matched already
	x = tablenames[index]
	databasedata = getDatafromDB(x)
	texts = databasedata[0]
	dicts = databasedata[1]

	masterlist = unmatched[index] + texts
	vect = TfidfVectorizer(tokenizer=normalize,min_df=1)
	tfidf = vect.fit_transform(masterlist)
	L = []
	j = 0
	print x
	while j < len(unmatched[index]):
		result = (tfidf * tfidf.T).A
		for x in range (len(result)):
			result[x][x] = 0
		maxindex = numpy.argmax(result[j])
		
		print masterlist[maxindex]
		print dicts[maxindex -len(unmatched[index])]
		print " "
		print masterlist[j]
		print "-------------"
		dictionary = dicts[maxindex-len(unmatched[index])]
		dictionary['element_id'] = o + counts
		addDataToDB(dictionary,dbname)
		o+=1
		j += 1
	index+=1
	
