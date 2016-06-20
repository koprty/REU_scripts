#Contents
* fillFollower_ing.py:
  * using followers.txt and following.txt which contain the dictionaries with the followers and followings of a particular screename, this file inserts followers/following Twitter id in the database in a space separated string into each twitter_id (using the users table) 
* fillScreename.py
  * Takes the manually categorized screename from xlsx files and inserts them into the table in the database
* finddb.py
  * populate the DB with the positive m-dab tweets from SETS A-F (from the tables in the same database) 
* fillunmatched.py 
  * fill in the missing 23 tweets into the database.
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



