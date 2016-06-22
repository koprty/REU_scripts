from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.svm import SVC
import cPickle

transformer = cPickle.load(open('new_tf2.pickle','rb'))
SVC = cPickle.load(open('SVC2.pickle','rb'))
vectorizer = cPickle.load(open('new_vect2.pickle','rb'))

fname = "test_set_new_corrected.txt"
t = open(fname, "r")
data = t.read()
arr = data.split("\r")
t_txt = []
t_class_num = []
t_class = []
for line in arr:
	parts = line.split("\t")
	t_txt.append(parts[3])
	if (parts[2] == "positive"):
		t_class_num.append(1)
	else:
		t_class_num.append(0)
	t_class.append(parts[2])

v1 = vectorizer.transform(t_txt)
v2 = transformer.transform(v1)

results = SVC.predict(v2)


'''
index = 0
for t in t_txt:
	print t 
	print "\t" + t_class[]
	print "\t" + str(results[index])
	index += 1

'''
tweet_results = []
index = 0
for r in results:
	tup = (t_class[index],r)
	index+=1
	tweet_results.append(tup)

tweet_results.sort(key = lambda tup: tup[1])


print SVC.score(v2,t_class_num)



#fout = open("results.txt", "w")
incorrect = 0.
total = 0.
for tr in tweet_results:
	if (tr[0] == "positive" and tr[1] == 0):
		incorrect += 1
	if (tr[0] == "negative" and tr[1] == 1):
		incorrect += 1
	total += 1

error = incorrect / total
print error 
#	fout.write(str(tr))
#	fout.write("\n")
##fout.close()
