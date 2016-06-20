#!/usr/bin/env python
import matplotlib.pyplot as plt
import networkx as nx
import sqlite3
import sys

"""
install networkx
(virtual environments may not be possible with this script)
In this script we will count how many people they follow
"""

#categories = [("individuals", "c"), ("shops", "r"), ("commercial_growers", "g"), ("service_providers", "k"), ("non-profits", "m"), ("news", "y"), ("interest_groups", "b")]
categories = ['individuals', 'shops', 'commercial_growers', 'service_providers', 'non-profits', 'news', 'interest_groups']
cm = {"individuals":"c", # cyan
		"shops": "r", # red
		"commercial_growers":"g", # greem
		"service_providers":"w", # white
		"non-profits":"m", #magenta
		"news":"y", # yellow
		"interest_groups":"b"} # blue


def calculate_counts (categories, types="following"):
	conn = sqlite3.connect("../tweets.sqlite")
	cursor = conn.cursor()
	weights = []
	for category in categories:
		query = "select %s from users where category = '%s'"%(types, category)
		cursor.execute(query)
		results = cursor.fetchall()
		distinct_follow = []
		for x in results:
			try:
				ids = x[0].split(" ")
				for y in ids:
					if y.strip() != "null" and int(y) not in distinct_follow:
						query = "select * from users where Usr_ID = %d"%(int(y))
						cursor.execute(query)
						results = cursor.fetchall()	
						if len(results) > 0:
							distinct_follow.append(int(y))
			except:
				e = sys.exc_info()[0]
				print e
				exit()
		weights.append(len(distinct_follow))
	conn.close()
	return weights
# returns the nodes weighted (size proportional to their following count )
# haha not really that useful
# gets weights by distinct users with connections to another twitter database
def weighted_nodes ():

	weights = calculate_counts(categories)
	print weights # [1047, 369, 131, 250, 7, 206, 350]

	G=nx.Graph()
	i = 0
	labels = {}
	while i < len(weights) and i < len(categories):
		G.add_node(categories[i], color = cm[categories[i]], size = int(weights[i]))
		labels[categories[i]] = str(weights[i])
		i+=1
	pos=nx.spring_layout(G)
	print cm
	print G.node
	maxweight = max(weights) 
	
	print
	nx.draw(G,pos,node_color =[G.node[node]["color"] for node in G], node_size=[int(G.node[node]["size"])*1.0/maxweight*10000 + 100  for node in G ] )
	nx.draw_networkx_labels(G,pos, labels)
	plt.axis('off')
	plt.savefig("weighted_graph.png") # save as png
	print "Saved image into weighted_graph.png"



def users_count (category, table_type="followings"):
	conn2 = sqlite3.connect("../tweets.sqlite")
	cursor = conn2.cursor()
	weights = []

	query = "select count(distinct %s.screename) from %s inner join users on users.Usr_ID = %s.Usr_ID where users.category= '%s'"%(table_type,table_type, table_type,category)
	print query
	cursor.execute(query)

	results = cursor.fetchall()
	weight = results[0][0]
	conn2.close()
	return weight

# calculate edge counts
def calculate_edge_counts ( table_type="followings"):
	conn = sqlite3.connect("../tweets.sqlite")
	cursor = conn.cursor()
	weights = []
	for category in categories:
		for category2 in categories:
			#query = "select %s from users where category = '%s'"%(types, category)
			query = "select count(*) from %s where %s_id in (select Usr_ID from users where category ='%s') and Usr_id in (select Usr_ID from users where category = '%s');"% (table_type, table_type[:-1], category, category2)
			print query
			cursor.execute(query)
			results = cursor.fetchall()
			
			weights.append((category, category2, results[0][0], table_type))
	conn.close()
	return weights

def weighted_edges(weight_tuples, table_type, categories = categories):
	G=nx.MultiDiGraph()
	el = {}
	for x in categories:
		G.add_node(    x , label = x + " ["+ str(users_count(x, table_type))  + "]"   )
	for w in weight_tuples:
		G.add_edge(w[0], w[1], label=str(w[2]))
		el[(w[0], w[1])] = int(w[2])
	pos = nx.circular_layout(G) # positions for all nodes
	pos = nx.spectral_layout(G)
	pos = nx.shell_layout(G)
	pos = nx.fruchterman_reingold_layout(G)
	#pos = nx.circular_layout(G)
	# nodes
	nx.draw_networkx_nodes(G,pos,node_list=categories, node_size=700)
	nx.draw_networkx_labels(G,pos,font_size=7,font_family='sans-serif')
	
	# edges
	nx.draw_networkx_edges(G,pos,
	                    width=1)
	nx.draw_networkx_edge_labels(G,pos, edge_labels = el, font_size=8, alpha=0.8)
	#plt.axis('off')
	#plt.savefig("edges.png")
	nx.write_dot(G,table_type+'.dot')
	print "done :D "
	print "dot file in " + table_type+".dot :D :D :D"


categories = ['individuals', 'shops', 'commercial_growers', 'service_providers', 'non-profits', 'news', 'interest_groups']

followingweights = calculate_edge_counts()
weighted_edges (followingweights, "followings")

followingweights = calculate_edge_counts("followers")
weighted_edges (followingweights, "followers")

