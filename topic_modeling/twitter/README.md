# Topic_modeling Tweets by Categorized Users
* Using the topic distribution from the 9 topics - topic model to categorize the tweets using topics  
* There are 7 categories of screenames: individual, shops, interest_groups, news, service_providers, non-profits. 
* This will be done using three metrics
  * Sticking all the tweets of screenames of each distinct category into distinct files and then runinng the LDA model to get the probability distribution of each category
  * Running the LDA model on each tweet and then normalizing the distribution (for each category) 
  * Running the LDA model on each tweet and then seeing which topic has the most 'maxes'
# Contents
* high_rts.py
  * finds topic model distribution of tweets with retweet count above a certain threshold using topic_dist2
* timeline_comp.py
  * using the topic distribution of a user's timeline as vectors for that user, it calculates the cosine distance between two users' vectors and if it is below a certain number, then they have an edge (writes the csvs for nodes and edges for the gephi graphs)
* timeline_topic_modeling.py
  * gets the 100 most recent tweets of the users in our database, runs the topic model on them to get their topic distribution
* topic_dist.py
  * method 1 of getting the topic distribution of a collection of tweets
* topic_dist2.py
  * method 2
* topic_dist3.py
  * i think you get it by now