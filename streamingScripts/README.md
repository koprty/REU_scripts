# Streaming Scripts
* These scripts are the scripts used to access Twitter's Streaming API. 
* The App Keys and the App Secrets may not work. If not, make a Twitter account, log in to apps.twitter.com and make new app keys and tokens to access the twitter api. 
* It may be necessary to pip install twython/tweepy when running some of these scripts. 


## Files
* streamingIngest.py - This is the script to actively stream for marijuana dabbing tweets (adapted from Tony's version) 
  * Note that this streaming script may stop sometimes due to attributeErrors. (We have tried to fix this as best as possible, but there still 
* streamingForGeneralDistribution.py - This script actively streams for political tweets. We used to compare time with m-dab tweets.
  * The next step would beo to do the media and retweet analysis we did for m-dab tweets and compare it with this dataset.
  * The database with these tweets currently has ~ 1 week of these tweets.. but has a significantly larger number of tweets than the m-dab dataset. 