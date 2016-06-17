# Topic_modeling Tweets by Categorized Users
* Using the topic distribution from the 9 topics - topic model to categorize the tweets using topics  
* There are 7 categories of screenames: individual, shops, interest_groups, news, service_providers, non-profits. 
* This will be done using three metrics
  * Sticking all the tweets of screenames of each distinct category into distinct files and then runinng the LDA model to get the probability distribution of each category
  * Running the LDA model on each tweet and then normalizing the distribution (for each category) 
  * Running the LDA model on each tweet and then seeing which topic has the most 'maxes'
