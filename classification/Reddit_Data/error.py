import re

def error(file_name):
	results = open(file_name, "r")
	correct= 0
	incorrect= 0
	total= 0
	for line in results:
		words = line.split('\t')
		if re.search("_Conservative.txt", words[0]):
			if words[2] > words[4]:
				correct += 1
			else:
				incorrect += 1
		if re.search("_Liberal.txt", words[0]):
			if words[2] < words [4]:
				correct += 1
			else:
				incorrect +=1
		total += 1
	error = incorrect*1.0/total
	results.close()
	print error
error("reddit_results.txt")

