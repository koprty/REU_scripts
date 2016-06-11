"""
Written by Lise Ho
This script is created to match elements in the A-F excel sets to their database counterparts to get the correct screenname for further analysis.
Uses the preprocessing implemented on database tweets to get the text of the tweets in the provided excel and text files

"""

import tweepy
import sqlite3
import json
import re
import string
import time


######## taken <- AND Edited from parse_text.py python file #########
# parses all lines with a positive result to it
def parsePosText(fname):
      #text = ""
      text = []
      f = open (fname, 'r')
      i = 0
      for line in f:
            content = line.split('\t')
            try:
                  if (content[2].lower() == "positive"):
                        #text += content[3]
                        z = content[3].strip().lower().split(" ")
                        phrase = []
                        for y in z: 
                              if y != " " and y != "\t" and y != "\n":
                                    phrase.append(y)
                        phrase = " ".join(phrase)
                        
                        if len(content) > 4:
                              i= 4
                              while i < len(content):
                                    phrase += "\t"+content[i]
                                    i+=1
                       
                        phrase =  phrase.split("\n")[0]
                        text.append(phrase.replace("\r", " ").replace("\n", " ").replace("\t", " ").strip())
                        #text.append(phrase.split("\n")[0].strip())

            except IndexError as e:
                  #int("asdfads")
                 
                  print str(content[0]) + " ____ " + str(i)

                  
                  if len(text) > 0:
                        '''
                        for r in content:
                              text[-1] = text[-1] + "\n" + str(r)
                        '''
                        pass
                              #text[-1] = text[-1].replace("\n"," ")
                  
                  #print line
                  
                  pass
            i+=1
                  #print str(content)+ " <-- " + fname 
      f.close()

      return text
########### End adapted code from parse_text.py ##########

##

def clean_str(string, TREC=False):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Every dataset is lower cased except for TREC
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)     
    string = re.sub(r"\'s", " \'s", string) 
    string = re.sub(r"\'ve", " \'ve", string) 
    string = re.sub(r"n\'t", " n\'t", string) 
    string = re.sub(r"\'re", " \'re", string) 
    string = re.sub(r"\'d", " \'d", string) 
    string = re.sub(r"\'ll", " \'ll", string) 
    string = re.sub(r",", " , ", string) 
    string = re.sub(r"!", " ! ", string) 
    string = re.sub(r"\(", " \( ", string) 
    string = re.sub(r"\)", " \) ", string) 
    string = re.sub(r"\?", " \? ", string) 
    string = re.sub(r"\s{2,}", " ", string)    
    return string.strip() if TREC else string.strip().lower()


    ##


#these will be used to cleanse the tweets
removal_pattern1 = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
removal_pattern2 = re.compile('//t.co(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
removal_pattern3 = re.compile('\n')
removal_pattern4 = re.compile(' amp ')
removal_pattern5 = re.compile('@[\w]* ')

#removal_pattern6 = re.compile(r'\\')

### Take out hashtags and all mentions from tweet text given a tweettext
def formatSQLresults (obj):
      s = obj["Tweet_Text"]
      
      words = s.split(" ") 

     
      formated_words = []
      #mentions = []

      hashtags = []
      
      for x in words:
            if "#" in x: 
                  hashtags.append(x)

      s = s.encode('ascii','ignore')
      s = s+" "
      s = removal_pattern5.sub('', s)
      s = removal_pattern1.sub('', s)
      s = removal_pattern2.sub('', s)
      s = removal_pattern3.sub(' ', s)
      s = s.translate(None, string.punctuation)
      s = s.lower()
      s = removal_pattern4.sub('',s)
     
      formated_words = s.replace("\r", " ").replace("\n", " ").replace("\t", " ")
      print formated_words

      print [formated_words.strip(), " ".join(hashtags)]
      return [formated_words.strip(), " ".join(hashtags)]



## convert sql query result into a dictionary
def dict_factory(cursor, row):
      d = {}
      for ids,col in enumerate(cursor.description):
        d[col[0]] = row[ids]
      return d

tablenames = ["SET_A", "SET_B", "SET_C", "SET_D", "SET_E", "SET_F"]
conn = sqlite3.connect('tweets.sqlite')
masterlist = []
unmatched = []
negatives = []
total = 0
totalloss = 0
inp = ""
db = True
if len(inp) < 1:
      inp = str(raw_input("excel or db? x for excel \n"))
      print inp


for z in tablenames:
      print z
      sql_query = """select * from [{0}] """.format(z)

      conn.row_factory = dict_factory
      cur = conn.cursor()
      cur.execute(sql_query)
      twitterdata = cur.fetchall()

      excel_data = parsePosText(z + ".txt") 
      # 4533 positives

      i = 0
      data = []
      for u in twitterdata:
            formateed= formatSQLresults (u)
            htags = formateed[1]
            d = u
            d['Tweet_Text'] = formateed[0] 
            d['hashtags'] = htags
            data.append(d)
            
      #print data

      datanah = []
      for x in data:
            if  x['Tweet_Text'].strip() in excel_data:
                  masterlist.append(x)
                  print x["Tweet_Text"] + ":) "
                  excel_data.remove(x['Tweet_Text'])
                  i+=1
            else:
                  datanah.append(x)
                  #print "boooo"
                  #print x
                  #print x["Tweet_Text"]
            #print x["Tweet_Text"]
            if "followfor" in x['Tweet_Text'].strip():
                  l = []
                  l.append(x['Tweet_Text'].strip())
                  print "mooooo"
                  print l
                  #exit()

      print i

      if z == tablenames[0]:
            if inp.strip() == "x":
                  db = not db
            if db:
                  f = open ("output_a.txt", "w").close()
            else:
                  f2 = open ("output_b.txt", "w").close()
      unmatched += excel_data
      if db:
            print "SQL DB DATA"
            print "length of all data not positive / errors in db parsing"
            print len(datanah)
            print "excel data length"
            print len(excel_data)
            f = open ("output_a.txt", "a")
            print unmatched
            f.write(str(unmatched) + "\n" + str(len(unmatched)) + "\n" + z + "\n")
            
            f.close()
            
            #print twitterdata
      else:
            print "EXCEL DATA"
            print "length of all data not positive / errors in db parsing"
            print len(datanah)
            print "excel data length"
            print len(excel_data)
            print z
            f2 = open ("output_b.txt", "a")

            f2.write(str(excel_data) + "\n" + str(len(excel_data)) + "\n")
            f2.close()
            #print excel_data
      totalloss += len(excel_data)
      
      negatives += datanah
      print totalloss
      print len(masterlist)
      #time.sleep(60)
#print datanah
            #print y["Tweet_Text"].split("\t")[0]
dbname = str(raw_input("Write stuff into database (type tablename if yes; 'n' if no \n"))
if dbname == "n":
      print "TOTAL LOSS"
      print len(unmatched)
      print unmatched
      print totalloss
      print len(masterlist)
      exit()
else:
      dbname = dbname.strip()
print "TOTAL LOSS"
print len(unmatched)
print totalloss
print len(masterlist)
g = 1
for x in masterlist:
      x['ImpureQuery'] = 88
      x['element_id'] = g
      columns = ', '.join(x.keys())
      placeholders = ':'+', :'.join(x.keys())
      #positivedabtweets 
      #dbname = "posdab_tweets"
      #dbname = "positivedabtweets"
      query = 'INSERT INTO %s (%s) VALUES (%s)' % (dbname,columns, placeholders)
      print query
      cur.execute(query, x)
      conn.commit()
      print str(i) + " <- nth of " + z
      print total
      g+=1
      i+=1
      total += 1
            
      #if y in excel_data:
      #      masterlist.append(y)
print "_____ END _____ " + z
print total
print len(masterlist)
conn.close()


