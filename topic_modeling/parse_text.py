import os
#parses the text and writes only those where the content[2] is positive
#from data set A-F there are 15 lines in the tab-separated-values file that have been ommitted due to formatting issues (i.e. tabs are used within the tweet )
def parseText(fname, results_text):
	text = ""
	f = open (fname, 'r')
	for line in f:
		content = line.split('\t')
		try:
			if (content[2].lower() == "positive"):
				text += content[3]
		except IndexError as e:
			pass
			#print str(content)+ " <-- " + fname 
	f.close()

	rfile = open(results_text, 'a')
	rfile.write(text)
	rfile.close()

	r = open(results_text, 'r')
	s = r.read()

	return s

files =["SET_A.txt","SET_B.txt","SET_C.txt","SET_D.txt","SET_E.txt","SET_F.txt"]
filename = "data.txt"
if (os.path.exists(filename)):
	open(filename, 'w').close() #empty the file
for x in files:
	parseText(x, filename)



#or we can use grep:
#grep 'positive' SET* 
#grep '\tpositive\t' SET* > grepped_data.txt
#gets 3 more postiives omitted by python code above