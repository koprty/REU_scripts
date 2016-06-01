from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import os

# this script is adapted from the sample script by Jordan Barber on the following web page
# https://rstudio-pubs-static.s3.amazonaws.com/79360_850b2a69980c4488b1db95987a24867a.html

tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list <- we will join the default list provided by NLTK and another list from a github repo
# we will add other filler words/ abbreviates used in various twitter tweets
en_stop = list(set(get_stop_words('en')) | set(stopwords.words('english'))) + ['u','oh', 'uh', 'im' ]

#print "\n".join(en_stop)
#exit(0)
# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()
    
# get the data from the file and stick it into a list
data_file = "data.txt"

f = open (data_file, 'r')
x = f.readlines()
for y in x:
	y = y.strip('\n')

# compile sample documents into a list
doc_set = x
# list for tokenized documents in loop
texts = []
# loop through document list
for i in doc_set:
    # clean and tokenize document string
    raw = i.lower()
    tokens = tokenizer.tokenize(raw)
    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if not i in en_stop]
    # stem tokens
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
    # add tokens to list
    texts.append(stemmed_tokens)

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)

# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

# WIP (WORK IN PROGRESS)
# TRYING TO FIND OPTIMAL number of topics to use
x = range(10,101)
os.chdir("lda_resultsUM")

for num in [c for c in x if c%10==0]:
#for num in x:
	# generate LDA model
	ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num, id2word = dictionary, passes=20)

	result_model = ldamodel.print_topics(num_topics=num, num_words=10)	

	s = ""
	for topic in result_model:
		s += str(topic) + "\n"
	f= open (str(num)+".txt", 'w')
	f.write(s)
	f.close
	print str(num)+".txt"
