import re
import json
import os

desc_keywords = ["smokeshop", "smoke shop", "business", "family owned", "family-owned","accessories","pipes","store","delivered","medical marijuana","free shipping"]
username_keywords = ["smoke shop", "smokeshop"]
scrnname_keywords = ["smokeshop", "smoke_shop", "vape"]
hashtag_keywords = ["smokeshop","vapeshop"]

ss = {}
ppl = {}

def identifier(dict_arr=[]):
	if os.path.isfile("smokeshops"):
		with open("smokeshops") as file:
			ss = json.load(file)
	if os.path.isfile("people"):
		with open("people") as file:
			ppl = json.load(file)
	for d in dict_arr:
		ss_count = 0

		screenname = ""
		if (type(None)!=type(d['Usr_Screename'])):
			screenname = d['Usr_Screename'].lower()

		username = d['Usrname'].lower()

		description = ""
		if (type(None) != type(d['Usr_Description'])):
			description= d['Usr_Description'].lower()

		hashtags = d['hashtags'].lower()

		for s_key in scrnname_keywords:
			if re.search(s_key,screenname):
				ss_count += 1
		for d_key in desc_keywords:
			if re.search(d_key, description):
				ss_count += 1
		for u_key in username_keywords:
			if re.search(u_key,username):
				ss_count += 1
		for h_key in hashtag_keywords:
			if re.search(h_key,hashtags):
				ss_count += 1

		if ss_count >= 2:
			already_present = False
			for s in ss:
				if (s ==screenname and ss[s]['Username'] == username):
					ss[s]['Tweets'].append(d['Tweet_Text'])
					ss[s]['hashtags'].append(hashtags)
					already_present = true
			if not already_present:
				ss[screenname]['Username']=username
				ss[screenname]['Description']= description
				ss[screenname]['Tweets'] = [d['Tweet_Text']]
				ss[screenname]['hashtags']=[hashtags]
				ss[screenname]['Following']=d['Usr_FollowingCount']
				ss[screenname]['Followers']=d['Usr_FollowersCount']
				ss[screenname]['NumTweets']=d['Usr_NumOfTweets']
		else:
			already_present = False
			for p in ppl:
				if (p ==screenname and ppl[p]['Username'] == username):
					ppl[p]['Tweets'].append(d['Tweet_Text'])
					ppl[p]['hashtags'].append(hashtags)
					already_present = true
			if not already_present:
				ppl[screenname]['Username']=username
				ppl[screenname]['Description']= description
				ppl[screenname]['Tweets'] = [d['Tweet_Text']]
				ppl[screenname]['hashtags']=[hashtags]
				ppl[screenname]['Following']=d['Usr_FollowingCount']
				ppl[screenname]['Followers']=d['Usr_FollowersCount']
				ppl[screenname]['NumTweets']=d['Usr_NumOfTweets']
	with open("smokeshops", 'w') as fout:
		json.dump(ss,fout)
	with open("people", 'w') as fout:
		json.dump(ppl,fout)

with open("tweet_dict_fully_checked") as file:
	twitterdata = json.load(file)
identifier(twitterdata)
