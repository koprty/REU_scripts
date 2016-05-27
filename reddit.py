import requests



# subreddits may have liberals in them but they are most likely not going to be a large factor in most of the lengthy rants on Reddit

#gets 25*times comments from a certain subreddit_title
def getrequest(subreddit_title,last_comment_name = None, times=5):
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

    print len(comments)
    print ("")

        
    comment = ""
    comment_name = ""
    for q in comments:
        comment = q['data']['body']
        comment_name = q['data']['name']
        if (len(comment) > 50):
            #save comment
            print comment

    getrequest(subreddit_title,comment_name, times-1)


getrequest("Conservative")
getrequest("Liberal")

