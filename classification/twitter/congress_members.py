import requests

## We use the GovTrack API in order to categorize twitter_id's with their respective parties <- and thus their respective whether liberal or conservative
# https://www.govtrack.us/developers/api

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

govtrack_twitterID= []
r = []
d=[]

for x in govtrack_data:
	if x["twitterID"] != None and x["twitterID"] != "None" and len("twitterID") != 0 and x["party"].lower() not in "independent":
		govtrack_twitterID.append(x)
		'''
		if x["party"].lower() in "republican":
			r.append(x)
		elif x["party"].lower() in "democrat":
			d.append(x)
		'''

# r and d are just separate arrays with republicans and democrat politican data 
# in twitter.py, we will still defaultly use govtrack_twitterID

