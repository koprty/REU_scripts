from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.svm import SVC
import json
import numpy as np
import cPickle

#set_a_f = ["SET_A", "SET_B", "SET_C", "SET_D", "SET_E", "SET_F"]

#for s in set_a_f:
with open("all_tweets") as file:
	tweets = json.load(file)
rand = np.random.permutation(tweets)
tweet_text = []
tweet_class = []
print "PART 0"
for tweet in rand:
	parts = tweet.split("\t")
	tweet_text.append(parts[1])
	if(parts[0] == "positive"):
		tweet_class.append(1)
	else:
		tweet_class.append(0)

print "PART 1"

#the following code is adapted from sample scripts given on scikit-learn.org on their page about working with text data
#URL: http://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
#if s == "SET_A":
count_vect = CountVectorizer()
tweet_text_counts = count_vect.fit_transform(tweet_text)
f= open("new_vect2.pickle", "wb")
cPickle.dump(count_vect, f)
f.close()
#del(count_vect)

print "PART 2"


tf_transformer = TfidfTransformer(use_idf=False).fit(tweet_text_counts)
tweet_train_tf = tf_transformer.transform(tweet_text_counts)
print tweet_train_tf
g = open ("new_tf2.pickle","wb")
cPickle.dump(tf_transformer, g)
g.close()
#del(tf_transformer)

print "PART 3"

#this code is also adapted from another page on scikit-learn.org about using SVM classifiers
#URL: http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html
clf = SVC(kernel='linear')
clf.fit(tweet_train_tf,tweet_class)

h = open("SVC2.pickle", "wb")
cPickle.dump(clf,h)
h.close()

print clf
#del(clf)
'''
else:
	transformer = cPickle.load(open('new_tf.pickle','rb'))
	SVC = cPickle.load(open('SVC.pickle','rb'))
	vectorizer = cPickle.load(open('new_vect.pickle','rb'))

	tweet_text_counts = vectorizer.transform(tweet_text)
	tweet_train_tf = transformer.transform(tweet_text_counts)
	SVC.fit(tweet_train_tf,tweet_class)
	h = open("SVC.pickle", "w")
	cPickle.dump(SVC,h)
	h.close()
	print SVC
'''
#test_tweet = ["high dab"]
#ttc = count_vect.transform(test_tweet)
#ttt = tf_transformer.transform(ttc)
#print ttt
#print(clf.predict(ttt))

