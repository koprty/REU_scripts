#Contents
* bigrams.py
  * gets the top 10 bigrams and trigrams of a certain subset of tweets based on retweet count
* edit_excel.py
  * adds empty rows to separate the different clusters of similar tweets and also calculates the percentage of tweets with higher retweet counts than similar tweets that came first
* retweeted_user_info.py
  * writes subset of tweets to excel file grouped by user who created the tweet and sorted by retweet count
* tweet_similarity.py
  * compares highly retweeted tweets with similar tweets using a tfidf vectorizer and writes it to an excel file