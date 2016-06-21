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
categories = ['individuals', 'shops', 'commercial_growers', 'service_providers', 'news', 'interest_groups'] #'non-profits', 

cm = {"individuals":"c", # cyan
		"shops": "r", # red
		"commercial_growers":"g", # greem
		"service_providers":"w", # white
		"non-profits":"m", #magenta
		"news":"y", # yellow
		"interest_groups":"b"} # blue


cat_colors = {"individuals":"#ff3ce5", # light orange
		"shops": "#ffcbc3", # light red
		"commercial_growers":"#c3ffd5", # light green
		"service_providers":"#eec5ff", # light purple
		"non-profits":"#ff3ce5", # light pink
		"news":"#fffac3", # light yellow
		"interest_groups":" #c5f2ff"} # light blue

edge_colors = {"individuals":"#FF82C9", # orange
		"shops": "#FF9180", # red
		"commercial_growers":"#5EFF8F", # green
		"service_providers":"#D266FF", # purple
		"non-profits":"#FF82C9", # pink
		"news":"#FCF172", # yellow
		"interest_groups":" #69DDFF"} # blue

label_colors = {"individuals":"#B80068", # dark ORANGE
		"shops": "#B51800", # dark red
		"commercial_growers":"#008C2B", # dark green
		"service_providers":"#690394", # dark purple
		"non-profits":"#B80068", # dark fuchsia
		"news":"#B8AC00", # dark yellow
		"interest_groups":" #007496"} # dark blue


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
			cursor.execute(query)
			results = cursor.fetchall()
			
			weights.append((category, category2, results[0][0], table_type))
	conn.close()
	return weights


def weighted_edges(weight_tuples, table_type, categories = categories, colors = cat_colors, e_colors = edge_colors, l_colors = label_colors):
	G=nx.MultiDiGraph()
	el = {}
	for x in categories:
		G.add_node( x , label = x + " ["+ str(users_count(x, table_type))  + "]",  style='filled' , fillcolor=colors[x])
	max_weight = max(weight_tuples,key=lambda item:item[2])[2]
	for w in weight_tuples:

		weight = w[2]
		edge_weight = 9.0*weight/max_weight + 1
		
		
		'''
		if weight > 1000:
			edge_weight = 10
		elif weight > 100:
			edge_weight = 7
		elif weight > 50:
			edge_weight = 3
		'''
		G.add_edge(w[0], w[1], label=str(weight), fontcolor = l_colors[w[0]], style="bold", color= e_colors[w[0]], fontsize=13, fontweight=10, penwidth=edge_weight)
		el[(w[0], w[1])] = int(weight)
	pos = nx.circular_layout(G) # positions for all nodes
	pos = nx.spectral_layout(G)
	pos = nx.shell_layout(G)
	pos = nx.fruchterman_reingold_layout(G)
	#pos = nx.circular_layout(G)
	# nodes
	nx.draw_networkx_nodes(G,pos,node_list=categories)
	nx.draw_networkx_labels(G,pos,font_size=7,font_family='sans-serif')
	
	# edges
	nx.draw_networkx_edges(G,pos)
	nx.draw_networkx_edge_labels(G,pos, edge_labels = el,)
	#plt.axis('off')
	#plt.savefig("edges.png")
	nx.write_dot(G,table_type+'.dot')
	print "done :D "
	print "dot file in " + table_type+".dot :D :D :D"

followingweights = calculate_edge_counts()
weighted_edges (followingweights, "followings")

#followingweights = calculate_edge_counts("followers")
#weighted_edges (followingweights, "followers")

