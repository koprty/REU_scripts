import networkx as nx
import matplotlib.pyplot as plt
import sqlite3
'''
Dependencies for this python script: 
pip install networkx

The goal of this script is to contruct a dabbing user network (meaning who is following who)
This is the messy version of the graph (unweighted)
'''

'''
G = nx.cubical_graph()

pos=nx.spring_layout(G) # positions for all nodes
nx.draw_networkx_nodes(G,pos,
                       nodelist=[1,2,3,'sp','s','a','m','p'],
                       node_color='b',
                       node_size=500,
                   alpha=0.8)

nx.draw_networkx_edges(G,pos,width=1.0,alpha=0.5)
nx.draw_networkx_edges(G,pos,
                       edgelist=[(1,3),('sp','s'),('sp','a'),(3,'a')],
                       width=8,alpha=0.5,edge_color='r')
'''

#categories = ['individuals', 'shops', 'commercial_growers', 'service_providers', 'non-profits', 'news', 'interest_groups']

categories = [("individuals", "c"), ("shops", "r"), ("commercial_growers", "g"), ("service_providers", "k"), ("non-profits", "m"), ("news", "y"), ("interest_groups", "b")]

def add_nodes (G, category ="", color="w"):
	conn = sqlite3.connect("tweets.sqlite")
	cursor = conn.cursor()
	query = "select screename from users where category = '%s'"%(category)
	cursor.execute(query)
	db_output = cursor.fetchall()
	sn = []
	for x in db_output:
		if len(x[0]) > 0:
			sn.append(x[0])
	'''
	if "HIGH_TIMES_Mag" in sn:
		print sn
		print category
		print query
		exit()
	'''
	G.add_nodes_from(sn)
	pos=nx.spring_layout(G) 
	nx.draw_networkx_nodes(G, pos, node_color= color, node_size=6, alpha =0.8 )
	conn.close()


def add_edges (G, category ="", color = "k"):
	conn = sqlite3.connect("tweets.sqlite")
	cursor = conn.cursor()
	query = "select screename, following from users where category = '%s'"%(category)
	cursor.execute(query)
	g = []
	connections = cursor.fetchall()
	for c in connections:
		friends = c[1].strip().split(" ")
		for x in friends: 
			print x
			if not (x == "null"):
				q = "select screename from users where Usr_ID = %s;"% x
				cursor.execute(q)
				friend = cursor.fetchall()
				for screenname in friend:
					if len(screenname[0]) > 0:
						g.append( (c[0],screenname[0]) ) 
	#pos=nx.spring_layout(G) 
	#nx.draw_networkx_nodes(G, pos, node_color= color, node_size=10, alpha =0.8 )
	conn.close()
	return g
G=nx.Graph()
# add_nodes(G)
edges = []
for x in categories:
	add_nodes(G, x[0], x[1])

print "nodes have all been added"
j = 0
y = categories[0]
edges.append(add_edges (G, y[0], y[1]))
'''
for y in categories:
	edges.append(add_edges (G, y[0], y[1]))
	print str (y) + "   " + str(j) + "th set of edges have been added"
	j+=1
'''
pos=nx.spectral_layout(G) 

i = 0
while i < len(categories) and i < len(edges):
	#print edges[i]
	#print i
	nx.draw_networkx_edges(G,pos,edgelist = edges[i], width=1.0,alpha=0.5,edge_color=categories[i][1])

	i +=1

	
'''
G.add_nodes_from("qwertyasp")
G.add_edge('a', 's')
G.add_edge('a', 'p')
G.add_edge('a', 'q')

# edges
G.add_edge('s', 'p')
G.add_edge('p', 'q')
pos=nx.spring_layout(G) # positions for all nodes


# nodes

nx.draw_networkx_nodes(G,pos,
                       node_color='r',
                       node_size=50,
                   alpha=0.8)
nx.draw_networkx_edges(G,pos,edgelist = [('a', 's'), ('a','p')], width=10.0,alpha=0.5,edge_color='c')




nx.draw_networkx_edges(G,pos,edgelist = [('s', 'p'), ('p','q')],width=10.0,alpha=0.5,edge_color='r')

'''
print "rendering is complete"
plt.axis('off')
plt.savefig("individuals_test_spectral.png")
'''



print G

#plt.savefig("edge_colormap.png") # save as png
#plt.show() # display
'''



def calculate_counts (categories, types="following", users_table = "users"):
	conn = sqlite3.connect("../tweets.sqlite")
	cursor = conn.cursor()
	weights = []
	for category in categories:
		query = "select %s from %s where category = '%s'"%(types,users_table, category)
		cursor.execute(query)
		results = cursor.fetchall()
		distinct_follow = []
		for x in results:
			try:
				ids = x[0].split(" ")
				for y in ids:
					if y.strip() != "null" and int(y) not in distinct_follow:
						query = "select * from %s where Usr_ID = %d"%(users_table,int(y))
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



	