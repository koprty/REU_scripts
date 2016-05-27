import requests

# sends a request to the GovTrack API in order to find CURRENT Congress members that 
def congress_members():
	c = requests.get("https://www.govtrack.us/api/v2/role?current=true&limit=600")
	r = c.json()
	members = r['objects']

	print len(members)


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

#print govtrack_data
