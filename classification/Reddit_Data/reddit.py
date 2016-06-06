import requests
import sys
import os


# subreddits may have liberals in them but they are most likely not going to be a large factor in most of the lengthy rants on Reddit

#gets 25*times comments from a certain subreddit_title
def getrequest(folder_name,con_last_comment_name = None, lib_last_comment_name = None):
    print "TIMES = " + str(times)
    if times <= 0:
        print "End of Data Collection"
        return
    
    #r/conservative
    if con_last_comment_name == None:
        r_con = requests.get("https://reddit.com/r/Conservative/comments.json?", headers={'User-agent':'Comment Bot 0.1'})
        #r.text

    else:
        r_con = requests.get("https://reddit.com/r/Conservative/comments.json?" + "after="+con_last_comment_name, headers={'User-agent':'Comment Bot 0.1'})
    

    con_request_json = r_con.json()
    con_comments = con_request_json['data']['children']

    count = 0    
    con_comment = ""
    con_comment_name = ""
    for q in con_comments:
        c_score = q['data']['score'].encode("ascii","ignore").decode("ascii")
        con_comment = q['data']['body'].encode("ascii","ignore").decode("ascii")
        con_comment_name = q['data']['name'].encode("ascii","ignore").decode("ascii")
        if (len(con_comment) > 100 and c_score > 0):
            count += 1
            file_name = folder_name + "/train/con/" + con_comment_name + ".txt"
            #save comment
            if count % 5 == 0:
                file_name = folder_name + "/test/" + con_comment_name + "_Conservative.txt"
            target = open(file_name, "a+")
            target.write(con_comment)
            target.write("\n")
            target.close()

    #r/liberal
     if lib_last_comment_name == None:
        r_lib = requests.get("https://reddit.com/r/Liberal/comments.json?", headers={'User-agent':'Comment Bot 0.1'})
        #r.text

    else:
        r_lib = requests.get("https://reddit.com/r/Liberal/comments.json?" + "after="+lib_last_comment_name, headers={'User-agent':'Comment Bot 0.1'})
    

    lib_request_json = r_lib.json()
    lib_comments = lib_request_json['data']['children']


    count = 0    
    l_comment = ""
    l_comment_name = ""
    for q in lib_comments:
        l_score = q['data']['score'].encode("ascii","ignore").decode("ascii")
        l_comment = q['data']['body'].encode("ascii","ignore").decode("ascii")
        l_comment_name = q['data']['name'].encode("ascii","ignore").decode("ascii")
        if (len(l_comment) > 100 and l_score > 0 ):
            count += 1
            file_name = folder_name + "/train/lib/" + l_comment_name + ".txt"
            #save comment
            if count % 5 == 0:
                file_name = folder_name + "/test/" + l_comment_name + "_Liberal.txt"
            target = open(file_name, "a+")
            target.write(l_comment)
            target.write("\n")
            target.close()
    getrequest(folder_name,con_comment_name, l_comment_name)

def setup():
    folder_name = sys.argv[1]
    if (os.path.exists(folder_name)):
        print "Folder already exists"
        exit(0)
    if (folder_name == ""):
        print "Please run program with desired file name as argument"
        exit(0)
    os.makedirs(folder_name)
    os.makedirs(folder_name + "/train")
    os.makedirs(folder_name + "/train/con")
    os.makedirs(folder_name + "/train/lib")
    os.makedirs(folder_name + "/test")
    getrequest(folder_name)

setup()

