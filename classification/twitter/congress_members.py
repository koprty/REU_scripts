import requests

# sends a request to the GovTrack API in order to find CURRENT Congress members that 
def congress_members():
	c = requests.get("https://www.govtrack.us/api/v2/role?current=true&limit=600")
	r = c.json()
	members = r['objects']

	arr = []
	d = {}
	member_party = ""
	member_first = ""
	member_last = ""
	member_id = ""
	member_twitter_id = ""
	twitter_count= 0
	for m in members:
		member_party = m['party']
		member_first = m["person"]["firstname"]
		member_last = m["person"]["lastname"]
		member_id = m["person"]["id"]
		member_twitter_id = str(m["person"]["twitterid"])
		if (member_twitter_id != "None"):
			twitter_count += 1

		#print (member_first + " " + member_last + ": " + member_party + ", twitterID = " + member_twitter_id)
		d = { "twitterID":member_twitter_id, "first":member_first, "last":member_last, "id":member_id, "party":member_party}
		arr.append(d)

	#print arr
	#print twitter_count
	#print len(members)
	return arr

govtrack_data = congress_members()


#get statistics of congress_members with twitterID
def getNumTwitter ():
	i = 0
	for x in govtrack_data:
		if x["twitterID"] != None and x["twitterID"] != "None" and len("twitterID") != 0:
			i+=1
	return i
#getNumTwitter()
#542
#521 with twitter 
#we will use 80% for training data and 20% for testing 

#print govtrack_data

govtrack_twitterID= []
r = []
d=[]

for x in govtrack_data:
	if x["twitterID"] != None and x["twitterID"] != "None" and len("twitterID") != 0 and x["party"].lower() not in "independent":
		govtrack_twitterID.append(x)
		if x["party"].lower() in "republican":
			r.append(x)
		elif x["party"].lower() in "democrat":
			d.append(x)
'''
print len(r)
print len(d)

		
y = len(govtrack_twitterID)
print y
#print y
#print int(y*.8)
y = int(y*.8)
print len(govtrack_twitterID[:y])
print len(govtrack_twitterID[y:])
'''
y = len(govtrack_twitterID)
y = int(y*.8)

r = []
d=[]


f = open ("republican.txt", "rb")
s = f.read()
s = s.split("\n")
for x in s:
	if len(x) >0 or x in r:
		r.append(x.lower())
print r
f.close()

ff = open("stuff.txt", "rb")
ss = ff.read()
ss = ss.split("\n")
i = 0
z = []
for y in ss:
	if len(y) >0 or y in z:
		z.append(y.lower()[:-4])
	i+=1

print len(z)
print len(r)

print sorted(z) 
print sorted(r)
for u in z:
	if u in r:
		r.remove(u)

print r

'''
x = govtrack_data[416:434]
for y in x:
	print y["twitterID"] + " " + y["party"]


for y in govtrack_data: 
	if y["party"].lower() =="independent":
		print y["twitterID"]
'''


