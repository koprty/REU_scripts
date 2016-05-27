import requests
import sys
import os


# subreddits may have liberals in them but they are most likely not going to be a large factor in most of the lengthy rants on Reddit

#gets 25*times comments from a certain subreddit_title
def getrequest(subreddit_title,folder_name = "",last_comment_name = None, times=10):
    print "TIMES = " + str(times)
    if times <= 0:
        print "End of Data Collection"
        return
    

    if last_comment_name == None:
        r = requests.get("https://reddit.com/r/{0}/comments.json?".format(subreddit_title), headers={'User-agent':'Comment Bot 0.1'})
        #r.text

    else:
        r = requests.get("https://reddit.com/r/{0}/comments.json?".format(subreddit_title) + "after="+last_comment_name, headers={'User-agent':'Comment Bot 0.1'})
    

    request_json = r.json()
    comments = request_json['data']['children']


    count = 0    
    comment = ""
    comment_name = ""
    for q in comments:
        comment = q['data']['body'].encode("ascii","ignore").decode("ascii")
        comment_name = q['data']['name'].encode("ascii","ignore").decode("ascii")
        if (len(comment) > 100):
            count += 1
            file_name= ""
            if (subreddit_title=="Conservative"):
                file_name = folder_name + "/train/con/" + comment_name + ".txt"
            else:
                file_name = folder_name + "/train/lib/" + comment_name + ".txt"
            #save comment
            if count % 5 == 0:
                file_name = folder_name + "/test/" + comment_name + "_" + subreddit_title + ".txt"
            target = open(file_name, "a+")
            target.write(comment)
            target.write("\n")
            target.close()
    getrequest(subreddit_title, folder_name,comment_name, times-1)

def setup():
    folder_name = sys.argv[1]
    if (os.path.exists(folder_name)):
        print "Folder already exists"
        exit(0)
    os.makedirs(folder_name)
    os.makedirs(folder_name + "/train")
    os.makedirs(folder_name + "/train/con")
    os.makedirs(folder_name + "/train/lib")
    os.makedirs(folder_name + "/test")
    getrequest("Conservative",folder_name)
    getrequest("Liberal",folder_name)

setup()

