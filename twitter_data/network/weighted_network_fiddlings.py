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
	conn = sqlite3.connect("tweets.sqlite")
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


# calculate edge counts
def calculate_edge_counts (category1, category2 types="following"):
	conn = sqlite3.connect("tweets.sqlite")
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

	exit()


	G.add_edge('a','b',weight=0.6)
	G.add_edge('a','c',weight=0.2)
	G.add_edge('c','d',weight=0.1)
	G.add_edge('c','e',weight=0.7)
	G.add_edge('c','f',weight=0.9)
	G.add_edge('a','d',weight=0.3)

	elarge=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] >0.5]
	esmall=[(u,v) for (u,v,d) in G.edges(data=True) if d['weight'] <=0.5]

	pos=nx.spring_layout(G) # positions for all nodes

	# nodes
	nx.draw_networkx_nodes(G,pos,node_size=700)

	# edges
	nx.draw_networkx_edges(G,pos,edgelist=elarge,
	                    width=6)
	nx.draw_networkx_edges(G,pos,edgelist=esmall,
	                    width=6,alpha=0.5,edge_color='b',style='dashed')

	# labels
	nx.draw_networkx_labels(G,pos,font_size=20,font_family='sans-serif')

def weighted_edges():
	pass
#weighted_nodes()
