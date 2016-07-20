#Contents
* classify.py
  * vectorizer, transforms, and classifies tweets as positive or negative
* correlation.py
  * compares SVC and SVR machines by finding various rank correlation coefficients and also compares SVC to multiple random rankings, uses sum of squares of difference in ranks, spearman's foot rule, and kendall's tau
* import.py
  *
* svm_testing.py
  * runs SVC on testing data, calculates scores and pearson r correlation coefficients between SVC and SVR and has a method to find thresholds for having certain percentage of positive tweets
* svm_training.py
  * trains the SVC classifier on the training data
* weights.py
  * finds weights of certain words, finds words above or below a certain weight
