# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 21:02:56 2016

@author: tony
"""

import tweepy
import sqlite3
import json
import pprint
from datetime import datetime
import time


#tweepy connection stuff
try:
    consumer_key = ""
    consumer_secret = ""
    access_token = ""
    access_token_secret = ""
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    keyword_list = ['dab weed','dabs','dabbing','dab weed', 'dabs weed',\
    'dabbing weed', 'dab smoke', 'dabs smoke','dabbing smoke', 'dabs wax',\
    'dab wax', 'dabbing wax', 'dab high', 'dabs high', 'dabbing high', \
    'dab oil', 'dabs oil', 'dabbing oil']

except:
    pass

class DabStreamListener (tweepy.StreamListener):
    
    def __init__(self): 
        self.database = sqlite3.connect('sql_db/tweetDB.sqlite', timeout = 10)
        self.pp = pprint.PrettyPrinter()
        self.count = 0
        self.counter  = 0
    def on_data(self,data):
        try:
            #create string for sql execution
            t = json.loads(data)
            self.pp.pprint(t)
            
            #filter out unwanted tweets such as retweets and non english
            if('retweeted_status' in t):
                print("rt")
                return
            if( 'lang' in t and t['lang'] != 'en'):
                return
            created = t['created_at'].encode('ascii','ignore')
            try: 
                createdAt = datetime.strptime(created, '%Y-%m-%d %X')
            except ValueError:
                created_list = created.split(" ")
                created_list = created_list[:4] + created_list[5:]
                created = " ".join(created_list)
                createdAt = datetime.strptime(created, '%c')

            sql_exec_string = """INSERT INTO TWEETS11_STREAMING (
            Tweet_ID, 
            Longitude,  
            Latitude,         
            Lang,         
            TwtCreatedAt,      
            FavoriteCount,     
            RetweetCount, 
            Tweet_Text,    
            Media,        
            Media_URL,        
            Usr_ID,    
            Usrname,    
            Usr_Screename,
            Usr_NumOfTweets,    
            Usr_Timezone,    
            Usr_URL,         
            Usr_Protected,     
            Usr_Location,     
            Usr_Lang,         
            Usr_Description,
            Usr_FollowersCount,
            Usr_FollowingCount,
            ImpureQuery)
            VALUES ("""+\
            str(t['id'])+", "+\
            "NULL" + ", " + \
            "NULL" + ", " + \
            "'"+(t['lang'].encode('ascii','ignore') if 'lang' in t  and t['lang'] != None else "NULL") + "', " + \
            "'"+str(createdAt) + "', " + \
            (str(t['favorite_count']) if t['favorite_count'] != None else "NULL") + ", " + \
            str(t['retweet_count']) + ", " + \
            "'"+str.replace((t['text']).encode('ascii','ignore'),"'","''") + "', " + \
            ("'"+str(t['entities']['media'][0]['type'])+"'" if 'media' in t['entities'] else "NULL") + ", " + \
            ("'"+(t['entities']['media'][0]['media_url'])+"'" if 'media' in t['entities'] else "NULL") + ", " + \
            str(t['user']['id']) + ", " + \
            ("'"+str.replace(t['user']['name'].encode('ascii','ignore'),"'","''")+"'" if 'name' in t['user'] and t['user']['name'] != None else "NULL")  + ", " + \
            ("'"+str.replace(str(t['user']['screen_name']),"'","''")+"'" if 'screen_name' in t['user'] else "NULL") + ", " + \
            (str(t['user']['statuses_count']) if 'statuses_count' in t['user'] else "NULL") + ", " + \
            ("'"+(t['user']['time_zone']).encode('ascii','ignore')+"'" if 'time_zone' in t['user'] and t['user']['time_zone'] != None  else "NULL") + ", " + \
            ("'"+(t['user']['url']).encode('ascii','ignore')+"'" if 'url' in t['user'] and t['user']['url'] != None  else "NULL") + ", " + \
            "'"+str(t['user']['protected']) + "', " + \
            ("'"+str.replace(t['user']['location'].encode('ascii','ignore'),"'","''")+"'" if 'location' in t['user'] and t['user']['location'] != None else "NULL") + ", " + \
            ("'"+(t['user']['lang']).encode('ascii','ignore')+"'" if 'lang' in t['user'] and t['user']['lang'] != None else "NULL") + ", " + \
            ("'"+str.replace(t['user']['description'].encode('ascii','ignore'),"'","''")+"'" if 'description' in t['user'] and t['user']['description'] != None else "NULL") + ", " + \
            ("'"+str(t['user']['followers_count'])+"'" if 'followers_count' in t['user'] else "NULL") + ", " + \
            ("'"+str(t['user']['friends_count'])+"'" if 'friends_count' in t['user'] else "NULL") + "," +\
            " 2 );"  #remember to change this in according to your query!!!!!          
              
            #print(sql_exec_string)
            #save to SQlite DB
            self.database.execute(sql_exec_string)
            self.database.commit()
            
            self.count += 1
            print("count: "+str(self.count))
            
        except Exception as e:
            if "database is locked" in e:
                self.counter+=1
            f = open ("databaselocked.txt", "a")
            f.write(str(self.counter) + str(datetime.now()))
            f.close()
            time.sleep(5)
            print e
            print("exception")
            

dab_stream = tweepy.Stream(auth=auth, listener=DabStreamListener())
print ("__________________ After tweepy Stream CALL _______________________")
try:
    dab_stream.filter(track=keyword_list, languages=['en'])
except AttributeError as e:
    f = open("errors.txt", "a")
    f.write(", ".join(keyword_list) + str(e) + "\n")
    f.close()
    dab_stream.filter(track=keyword_list, languages=['en'])

print("end")
