import re
import sys

def error(file_name):
	results = open(file_name, "r")
	incorrect= 0
	total= 0
	for line in results:
		words = line.split('\t')
		if re.search("_Conservative.txt", words[0]):
			if words[2] < words[4]:
				if not re.search("E-", words[4]):
					incorrect += 1
		if re.search("_Liberal.txt", words[0]):
			if words[2] > words [4]:
				if not re.search("E-", words[2]):
					incorrect +=1
		total += 1
	error = incorrect*1.0/total
	results.close()
	print error
error(sys.argv[1])

