import sqlite3
import json

## convert sql query result into a dictionary
def dict_factory(cursor, row):
      d = {}
      for ids,col in enumerate(cursor.description):
        d[col[0]] = row[ids]
      return d

conn = sqlite3.connect('tweets.sqlite')

tablename = "posdab_tweets"
sql_query = """select * from [{0}] """.format(tablename)

conn.row_factory = dict_factory
cur = conn.cursor()
cur.execute(sql_query)
twitterdata = cur.fetchall()
conn.close()
print twitterdata # <- the data in array format
print twitterdata[0].keys() # the keys of the dictionary... yea the array is pretty messy -_-

with open("tweet_dict",'w') as fout:
	json.dump(twitterdata,fout)