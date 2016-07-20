#Contents
* get_follower_count.py
  * updates database with number of followers and friends pulled from the Twitter API
* get_retweeters.py
  * gets the ids of up to the last 100 people to retweet a tweet and sticks them in the retweets table
* getFollowers.py
  * gets the list of ids of followers of a user and writes it to a file
* getFollowing.py
  * does pretty much the same as getFollowers but gets the ids of friends (people following the user) instead
* getTwitterInfo.py
  * gets the screename and description from Twitter and dumps it into a json file in an array of dictionaries
* updateFavsRetweets.py
  * 