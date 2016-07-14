from scipy.spatial.distance import cosine
import sqlite3

conn = sqlite3.connect("../tweets.sqlite")
cursor = conn.cursor()
query = "Select User_ID, Screename, Category, Topic_dist from timeline_dist"
cursor.execute(query)
users = cursor.fetchall()

node_csv = open("nodes","w")
node_csv.write("Id,Label,Category\n")

for user in users:
	s = str(user[0]) + "," + user[1] + "," + user[2]+"\n"
	node_csv.write(s)
node_csv.close()

edge_csv = open("edges","w")
edge_csv.write("Source,Target,Weight\n")

print len(users)
i = 0
while (i <len(users)):
	user = users[i]
	topic_dist_i = [float(j) for j in user[3].split(" ")]
	j = i+1
	while (j < len(users)):
		com_user = users[j]
		topic_dist_j = [float(k) for k in com_user[3].split(" ")]
		sp_dist = cosine(topic_dist_i,topic_dist_j)
		if sp_dist < .0015:
			weight = 1 - sp_dist
			s = str(user[0])+","+str(com_user[0])+","+str(weight)+"\n"
			edge_csv.write(s)
		j+=1
	print i
	i += 1

edge_csv.close()