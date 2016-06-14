import gensim
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models


tokenizer = RegexpTokenizer(r'\w+')
p_stemmer = PorterStemmer()

categories = ["individuals", "shops", "commercial_growers", "service_providers", "non-profits", "news", "interest_groups"]


def doc_to_bow(filename):
	en_stop = list(set(get_stop_words('en')) | set(stopwords.words('english'))) + ['u','oh', 'uh', 'im', 'n', 'dont', 'ur']
	data = open(filename, "r")
	text = data.read()
	data.close()
	#remove stopwords 
	raw = text.lower()
	tokens =tokenizer.tokenize(raw)
	stopped_tokens = [j for j in tokens if not j in stopwords.words('english')]
	stemmed_tokens = [p_stemmer.stem(j) for j in stopped_tokens]
	d = corpora.Dictionary.load("tweet_dict.dict")
	doc_bow = d.doc2bow(stemmed_tokens)
	return doc_bow

def string_topics(topic_list):
	s = ""
	for topic in topic_list:
		topic_num = topic[0]
		words_probs = topic[1]
		wp = words_probs.split(" + ")
		s += "Topic " + str(topic_num) + ":\t"
		for w in wp:
			word = w.split("*")
			s+= str(word[1]) + ": " + str(word[0]) + " || "
		s += "\n"
	return s

def pretty_topic_print(doc_dist = []):
	s = ""
	for topic in doc_dist:
		topic_num = topic[0]
		topic_dist = topic[1]
		s += "Topic " + str(topic_num) + ":\t" + str(topic_dist) + "\n"
	return s

def topic_dist(doc_bow, category = ""):
	lda = models.ldamodel.LdaModel.load("lda_9.ginsem")
	result_model = lda.print_topics(num_topics=9, num_words=10)	
	s = string_topics(result_model)
	print s
	doc_lda = lda[doc_bow]
	pp_doc = pretty_topic_print(doc_lda)
	if (category != ""):
		fout_name = category + "_topic_dist.txt"
		fout = open(fout_name, "w")
		fout.write(pp_doc)
		fout.close()
	print "\nTopic Distribution for " + category + ":\n"
	print pp_doc


for c in categories:
	file = c + ".txt"
	doc_bow = doc_to_bow(file)
	topic_dist(doc_bow, c)

