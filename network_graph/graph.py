import dill
import networkx as nx
import json
from networkx.readwrite import json_graph


# for every pair of people, count the number of mutual tags, set that as edge weight
# for each keyword, keep a list of people who have that keyword tag

def create_graph():
	graph = nx.Graph()
	#sample nodes and edges
	graph.add_nodes_from([2,5])
	graph.add_edges_from([(2,5)])
	#add edges and nodes to graph
	fd = open("graph.txt", "w")
	dill.dump(graph, fd)
	fd.close()

def plot_graph():
	fd = open("graph.txt", "rb")
	graph = dill.load(fd)
	# write json formatted data
	d = json_graph.node_link_data(graph) # node-link format to serialize
	# write json
	json.dump(d, open("/Users/Juhee/Documents/MEAN/network_graph/graph.json","wb"))

if __name__ == '__main__':
	create_graph()
	plot_graph()


