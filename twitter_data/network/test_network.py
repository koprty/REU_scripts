import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()


G.add_nodes_from("spam")
G.add_nodes_from([1,2,3])
G.add_edge('p','s')
G['p']['s']["color"] = "c"
G['p']['s']["width"] = 20
pos=nx.spring_layout(G) # positions for all nodes


nx.draw_networkx_nodes(G,pos,
                       nodelist=[1,2,3,'s','a','m','p'],
                       node_color='b',
                       node_size=4,
                   		alpha=0.8)

nx.draw_networkx_edges(G,pos,width=1.0,alpha=0.5)

'''
nx.draw_networkx_edges(G,pos,
                       edgelist=[(1,3),('p','a'),(3,'a')],
                       width=1,alpha=0.5)

'''
plt.axis('off')
plt.savefig("test.png")