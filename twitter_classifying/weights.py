from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.svm import SVC
from scipy.sparse import lil_matrix
import cPickle


transformer = cPickle.load(open('new_tf2.pickle','rb'))
SVC = cPickle.load(open('SVC2.pickle','rb'))
vectorizer = cPickle.load(open('new_vect2.pickle','rb'))

coeff_i =  SVC.coef_.indices
coeff_d = SVC.coef_.data
vocab =  vectorizer.vocabulary_

index = vocab['tree oil']
i=0
for c in coeff_i:
	if c == index:
		print coeff_d[i]
	i += 1
'''
i=0
coeff = []
for c in coeff_i:
	if abs(coeff_d[i])>.4
		tup = (coeff_i[i],coeff_d[i])
		coeff.append(tup)
	i+=1


for c in coeff: 
'''
'''
for v in vocab:
	if "high" in v or "oil" in v:
		index = vocab[v]
		i=0
		for c in coeff_i:
			if c == index:
				if abs(coeff_d[i])>.15:
					print v + " "+ str(coeff_d[i])
			i +=1

'''
