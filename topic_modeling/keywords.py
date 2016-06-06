import re

desc_keywords = ["smokeshop", "smoke shop", "business", "family owned", "family-owned","accessories","pipes","store","delivered","medical marijuana","free shipping"]
scrnname_keywords = ["smoke shop", "smokeshop"]
username_keywords = ["smokeshop", "smoke_shop"]
hashtag_keywords = ["smokeshop","vapeshop"]

def identifier(dict_arr=[]):
	for d in dict_arr:
		ss_count = 0
		screenname = d['screenname'].lower()
		username = d['username'].lower()
		description= d['description'].lower()
		hashtags = d['hastags'].lower()
		for s_key in scrnname_keywords:
			if re.search(s_key,screenname):
				ss_count += 1
		for d_key in desc_keywords:
			if re.search(d_key, description):
				ss_count += 1
		for u_key in username_keywords:
			if re.search(u_key,username):
				ss_count += 1
		for h_key in hashtags:
			if re.search(h_key,hashtags):
				ss_count += 1
		file = ""
		if ss_count >= 2:
			file="smoke_shops.txt"
		else:
			file = "people.txt"
		t=open(file,"a+")
		t.write(d)
		t.write("\n")
		t.close()


