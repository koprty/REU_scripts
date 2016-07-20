
categories = ["individuals", "shops", "commercial_growers", "service_providers", "non-profits", "news", "interest_groups"]

for c in categories:
	file = c + "_topic_dist_2_retry.txt"
	topic_dist = open(file, "r")
	fout = c + "_just_prob.txt"
	t = open(fout, 'w')
	for line in topic_dist:
		words = line.split("\t")
		t.write(words[1])
	topic_dist.close()
	t.close()

