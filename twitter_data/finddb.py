
"""
Written by Lise Ho
This script is created to match elements in the A-F excel sets to their database counterparts to get the correct screenname for further analysis.
Due to the unavailability of the pre-processing scripts, there is a degress of error in this script in that ~23 'positive' elements were not matched from the
      tsv file to the database.
      Thus to supplement this script, use the "findunmatched.py" that does direct text cross validation to determine these matches.
            The unmatched strings were manually found so it may be necessary to edit the findunmatched.py file
"""

import tweepy
import sqlite3
import json
import pprint

######## taken <- AND Edited from parse_text.py python file #########
# parses all lines with a positive result to it
def parsePosText(fname):
      #text = ""
      text = []
      f = open (fname, 'r')
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
                        
                        text.append(phrase)
            except IndexError as e:
                  pass
                  #print str(content)+ " <-- " + fname 
      f.close()

      return text
########### End adapted code from parse_text.py ##########

### Take out hashtags and all mentions from tweet text given a tweettext
def formatSQLresults (obj):
      tweettxt = obj["Tweet_Text"]
      
      words = []

      if (tweettxt != None ):
            spun = ["\n", "\t"]
            for s in spun:
                  tweettxt = tweettxt.replace (s, " ")
            
            words = tweettxt.split(" ") 

     
      formated_words = []
      #mentions = []

      hashtags = []
      
      for x in words:
            if "#" in x: 
                  hashtags.append(x)
                  x = x.replace("#", "")

            if ("https://" not in x and "http://" not in x):
                  
                  x = x.replace("&lt", "lt")
                  x = x.replace("&gt", "gt")

                  pun = [ "\\", "/", "?",  "|", "$", "`", "*", "(", "-", "_", "[", "]", "{", "}", "+", "=", "!", "%", "^", ",", ";", "~"]
                  
                  for p in pun:
                        x = x.replace (p, "")

                  if len(x) > 0 and x[0] == ".":
                        x = x[1:]
                  #print x
                  if "&" == x or "&amp" == x:
                        pass
                        #x = x.replace ("&amp", "")
                        formated_words.append("?!_")
                        #print x
                        #print formated_words
                  elif "&" in x:
                        x = x.replace(".", "")
                        x = x.replace('"', "")
                        x = x.replace(')', "")
                        x = x.replace("'", "")
                        x = x.replace(":", "")
                        x = x.replace("&", "")
                        print x
                        formated_words.append(x.lower())
                        #print "hi"
                  else:
                        if len(x) > 0 and x[0] == "@" and "." not in x and not x.count("@") > 1  and ")" not in x and not ":" == x[-1] and not "," == x[-1]:
                              pass
                        else:
                              x = x.replace(".", "")
                              x = x.replace("@", "")
                              x = x.replace('"', "")
                              x = x.replace(')', "")
                              x = x.replace("'", "")
                              x = x.replace(":", "")
                              x = x.replace(",", "")
                              formated_words.append(x.lower())
            else:
                  formated_words.append("")
            #print formated_words
      if "smokecartel" in tweettxt.lower():
            print tweettxt
            print formated_words
            #formated_words = " ".join(formated_words).replace (" ?!_ ", "")
            #print formated_words
            print "_"
            #exit()
      formated_words = " ".join(formated_words).replace (" ?!_ ", "")
      return [formated_words, " ".join(hashtags)]



## convert sql query result into a dictionary
def dict_factory(cursor, row):
      d = {}
      for ids,col in enumerate(cursor.description):
        d[col[0]] = row[ids]
      return d

tablenames = ["SET_A", "SET_B", "SET_C", "SET_D", "SET_E", "SET_F"]
conn = sqlite3.connect('tweets.sqlite')
masterlist = []
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

      excel_data = parsePosText(z + "__.txt") 
      # 4533 positivess

      i = 0
      print "number of positives in excel_data"
      print len(excel_data)
      print len(twitterdata)
      data = []
      for u in twitterdata:
            formateed= formatSQLresults (u)
            htags = formateed[1]
            d = u
            d['Tweet_Text'] = formateed[0] 
            #print d['Tweet_Text']
            d['hashtags'] = htags
            data.append(d)
            
      #print data

      datanah = []
      for x in data:
            
            if x['Tweet_Text'].strip().lower() in excel_data:
                  #print
                  #print x["Tweet_Text"]
                  #print
                  masterlist.append(x)
                  excel_data.remove(x['Tweet_Text'].strip().lower())
                  i+=1
            else:
                  datanah.append(x)
                  #print x
                  #print x["Tweet_Text"]
            #print x["Tweet_Text"]

      print i

      if z == tablenames[0]:
            if inp.strip() == "x":
                  db = not db
            if db:
                  f = open ("output.txt", "w").close()
            else:
                  f2 = open ("output2.txt", "w").close()
      if db:
            print "SQL DB DATA"
            print "length of all data not positive / errors in db parsing"
            print len(datanah)
            print "excel data length"
            print len(excel_data)


            f = open ("output.txt", "a")
            

            for o in datanah:
                  f.write( o['Tweet_Text'] + "\n")
            f.close()
            
            #print twitterdata
      else:
            print "EXCEL DATA"
            print "length of all data not positive / errors in db parsing"
            print len(datanah)
            print "excel data length"
            print len(excel_data)
            print z
            f2 = open ("output2.txt", "a")

            f2.write(str(excel_data) + "\n" + str(len(excel_data)) + "\n")
            f2.close()
            #print excel_data
      totalloss += len(excel_data)

dbname = str(raw_input("Write stuff into database (type tablename if yes; 'n' if no \n"))
if dbname == "n":
      exit()
else:
      dbname = dbname.strip()
print "TOTAL LOSS"
print totalloss
print len(masterlist)
g = 1
for x in masterlist:
      x['ImpureQuery'] = 77
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


