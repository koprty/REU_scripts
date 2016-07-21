# Network subdirectory 
* This directory containes the scripts used to parse the database table and create network visualizations via networkx

##Scripts
* weighted_network_fiddlings.py <- weighted node graph and weighted edge graph (weighted edge graph is still incomplete)
* networkFiddlings.py  <- drawing all connections (following and follower wise... did not turn out to be anything very substantial telling)


## Graphs
### Graph Naming Convention
* suffix indicates which database the network was built off of 
  * **Followers** - an arrow indicates a user from one category following user in the category on the end of the arrowhead
  * **Followings** - an arrow indicats a user being followers from a user in the category on the end of the arrowhead
* ***PREFIX*** indicates what dataset it was pulled from
  * **total** uses data from the training set (Set A-F) dataset and the tweets9 dataset
  * **old/new** uses data from these sets as well but do not have some of the updated user categories (old charts look at 'total' for better look at network)

###


