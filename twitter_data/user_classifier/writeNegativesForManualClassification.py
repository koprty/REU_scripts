import sqlite3


'''
	#UPDATE USERS ALREADY CLASSIFIED from users and tweets9_users 
'''
def updateCategories_Descripts_fromDB():
	conn = sqlite3.connect("../tweets.sqlite")
	cursor  = conn.cursor()
	o=0
	query = "select Usr_ID, Screename, Description,  Category, Followers, Following from users where Usr_ID in (select Usr_ID from tweets9_musers);"
	query = "select Usr_ID, Screename, Description, Category, Followers, Following from tweets9_users where Usr_ID in (select Usr_ID from tweets9_musers);"
	cursor.execute(query)
	data = cursor.fetchall()

	for x in data: 
		query = "UPDATE tweets9_musers set Screename = '%s', Description = \"%s\", category = '%s', followers = '%s',following = '%s' where Usr_ID = '%s'"%(x[1], x[2], x[3],x[4], x[5], x[0])
		print query
		cursor.execute(query)
		conn.commit()
		o+=1
	print o
	conn.close()
	exit()
#updateCategories_Descripts_fromDB()

# update descriptions with quotation marks
# update users descriptions 
def updateDescripts():
	conn = sqlite3.connect("../tweets.sqlite")
	cursor  = conn.cursor()
	o=0
	# extra quotes from new descriptions not from users or tweets9_users
	#query = "select  Description, Usr_ID  from users where Usr_ID in (select Usr_ID from tweets9_musers);"
	query = "select  Description, Usr_ID  from tweets9_musers ;"
	query = "select  Usr_Description, Usr_ID  from posdab_tweets where Usr_ID in (select  Usr_ID from users where category is null);"
	cursor.execute(query)
	data = cursor.fetchall()
	for x in data:

		#if len(x[0]) > 0 and x[0][0] == '"' and x[0][-1] == '"':
		if len(x) > 0 and x[0]!= None:
			print x
			query = "UPDATE users set Description = \"%s\" where Usr_ID = '%s'"%(x[0][1:-1], x[1])
			print query
			cursor.execute(query)
			#conn.commit()
			o+=1
	print o
	conn.close()
	exit()
#updateDescripts()

def writeToFile():
	conn = sqlite3.connect("../tweets.sqlite")
	cursor  = conn.cursor()

	query = "select Usr_ID, Screename, Description from tweets9_users where category = 'null';"
	query = "select Usr_ID, Screename, Description, Numfollowing , numfollowers from users where category is null;"
	cursor.execute(query)
	

	results = cursor.fetchall()
	s = ""
	#re = results[:len(results)/3]
	
	for r in results:
		x = 0
		while x < len(r):
			if x ==1:
				s+= "\t"
			s += str(r[x]).replace("\r", "\t").replace("\n", "\t")
			s+= "\t"
			x+=1
		s += "\n"

	conn.close()


	f = open("data.txt", "wb")
	f.write(s)
	f.close()

#be careful here
#writeToFile()
#print "writing done"

# Usr_ID is trimmed off due to xlsx format -__-
# using screenames to relate
### update categories and screenames
def importCategoriesDB(fname):
	f = open (fname, "r")
	content = f.read()
	#print content
	f.close()

	conn = sqlite3.connect("../tweets.sqlite")
	cursor = conn.cursor()
	lines = content.split("\r")
	#print lines
	i = 0
	for line in lines:

		l = line.split("\t")
		'''
		if len(l) != 4:
			print l
			exit()
		'''
		###usr_id = l[0]
		cate = l[1]
		sn = l[2]
		if sn != "None" and len(cate) > 0:
			query = "UPDATE tweets9_musers set category = '%s' where Screename = '%s'"%(cate, sn)
			###query = "UPDATE users set category = '%s', Screename='%s' where Usr_ID = '%s'"%(cate, sn, usr_id)
			cursor.execute(query)
			print query 
			i+=1
		#conn.commit()
	print i
	conn.close()

	return content.split("\r")


#x =importCategoriesDB ("partA.txt")
#print len(x)


x =importCategoriesDB ("dataB.txt")
#print len(x)


#print x






