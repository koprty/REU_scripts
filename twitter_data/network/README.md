# Network subdirectory 
* This directory containes the scripts used to parse the database table and create network visualizations via networkx
* This directory uses the "tweets.sqlite" database in the directory above this one. Change the dbpath as needed. 
* The weighted_network_fiddlings.py script is the main script and should be used after the follower and following tables are made by the "fillFollow_ing2SeparateTables.py" script in the directory above this one. 

##Scripts
* weighted_network_fiddlings.py <- weighted edge graph
* networkFiddlings.py  <- drawing all connections (following and follower wise... did not turn out to be anything very substantial telling... renders a very large dense donut graph...)


## Graphs
### Graph Naming Convention
* suffix indicates which database the network was built off of 
  * **Followers** - an arrow indicates a user from one category following user in the category on the end of the arrowhead
  * **Followings** - an arrow indicats a user being followers from a user in the category on the end of the arrowhead
* ***PREFIX*** indicates what dataset it was pulled from
  * **total** uses data from the training set (Set A-F) dataset and the tweets9 dataset
  * **old/new** uses data from these sets as well but do not have some of the updated user categories (old charts look at 'total' for better look at network)

###


