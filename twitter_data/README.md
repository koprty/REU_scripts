#Contents
## Folders
* network
* retweet_analysis
  * Folder containing all the Retweet Analysis (scripts and excel files)
* tweet_classifier
  * This folder contains the final tweet classifiers we used to classify streaming dab tweets
* tweet_calls
  * Twitter API call scripts
* user_classifier
  * The final user classifier we used and scripts to ease manually relabeling of non-individuals



##Files
**Note many of these files link to a database in this directory. So be sure to change the dbpath as needed.**
* fillFollower_ing.py:
  * using followers.txt and following.txt which contain the dictionaries with the followers and followings of a particular screename, this file inserts followers/following Twitter id in the database in a space separated string into each twitter_id (using the users table) 
* fillFollower_ing2SeparateTables.py
  * preprocessing followers and friends from the 'followers' and 'following' columns in a user table to two separate tables with a row for each connection (i.e. user A follows user B) 
  * designed for easing network creation
* fillScreename.py
  * Takes the manually categorized screename from xlsx files and inserts them into the table in the database
* finddb.py
  * populate the DB with the positive m-dab tweets from SETS A-F (from the tables in the same database) 
* findunmatched.py 
  * fill in the missing 23 tweets into the database (UNUSED)
* gather_favs.py
  * has methods to find totals and averages of favorite and retweet counts of each category, as well as methods to find the number of tweets above a certain number of favorites or retweets, to return a list of the top favorited n tweets, and to return a list of the top retweeted n tweets
* getFollowersintoDB.py
  * Gets the followers and following of distinct users from the Twitter API into the actual database
* getScreenname.py
  * Parses the dictionary file (i.e. all_tweets_dict_fully_checked) and gets all the Screenames, distinct Screenames 
* getTweetsInArrayOfDictionary.py
  * precisely what the name of the file says. Short script to write tweets in an array of dictionaries
* keywords.py 
  * does smokeshop versus ppl division using user descriptions (deprecated since screename categories are not that binary) 
* match_excel_db.py
  * An attempt to match the positive tweets from the excel file to the database using the preprocessing algorithm used (failed for tweets with newlines since the preprocessing that rendered the excel files did not replace newlines in the tsv formatted file....) 
* shop_v_ppl.py 
  * 2nd method in addition to the keywords.py script to separate smoke shops versus people (deprecated since there are more catgeories - see topic-modeling/twitter and transferCategoriesToTxt.py)
* transferCategoriesToTxt.py
  * transfer categories from filled in db to 7 different text files which will then be sent to the topic modeling lda script in topic_modeling/twitter/topic_dist.py / 
* updateDates.py
  * update Dates of TweetCreationTime for Tweets (topics and streaming tables) in database [i.e. Columns: TwtCreatedAt, CreatedAt]



