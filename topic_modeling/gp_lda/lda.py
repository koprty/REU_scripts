import gensim
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models


#USE lda_nltk.py in alt file

def corpus_and_d():

	tokenizer = RegexpTokenizer(r'\w+')
	p_stemmer = PorterStemmer()

	stoplist = ['for', 'a', 'of', 'the', 'and', 'to', 'in']
	data = open("data.txt", "r")
	text = data.readlines()
	data.close()
	tweets = []
	#remove stopwords 
	for i in text:
		raw = i.lower()
		tokens =tokenizer.tokenize(raw)
		stopped_tokens = [j for j in tokens if not j in stopwords.words('english')]
		stemmed_tokens = [p_stemmer.stem(j) for j in stopped_tokens]
		tweets.append(stemmed_tokens)
	d = corpora.Dictionary(tweets)
	print(d)
	d.save("tweet_dict.dict")

	corpus = [d.doc2bow(tweet) for tweet in tweets]
	corpora.MmCorpus.serialize("tweet_corpus.mm", corpus)


def lda():
	corpus=corpora.MmCorpus("tweet_corpus.mm")
	d = corpora.Dictionary.load("tweet_dict.dict")
	lda = models.ldamodel.LdaModel(corpus, num_topics = 9, id2word=d)
	lda.save("lda.ginsem")

def print_topics(topic_list):
	for topic in topic_list:
		topic_num = topic[0]
		words_probs = topic[1]
		wp = words_probs.split(" + ")
		s = "Topic " + str(topic_num) + ":\t"
		for w in wp:
			word = w.split("*")
			s+= str(word[1]) + ": " + str(word[0]) + "\t"
		print s
		

lda = models.ldamodel.LdaModel.load("lda.ginsem")
print_topics(lda.show_topics())