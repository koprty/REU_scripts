import re
import sys

def twitter_error(file_name):
	results = open(file_name, "r")
	incorrect= 0
	total= 0
	for line in results:
		words = line.split('\t')

		if re.search("republican", words[0]):
			if float(words[2]) > float(words[4]):
				incorrect += 1
		if re.search("democrat", words[0]):
			if float(words[2]) < float(words[4]):
				incorrect +=1
		total += 1
	error = incorrect*1.0/total
	results.close()
	print error


twitter_error(sys.argv[1])

