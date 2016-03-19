__author__ = 'ssatpati'
import networkx as nx
import ast, sys
from networkx import algorithms
import matplotlib.pyplot as plt

# Flexible Load Data Function
def load_data(filename):
    nodes = set()
    edges = set()
    with open (filename, 'r') as myfile:
        for line in myfile:
            line = line.split('\t')
            node = line[0]
            if node not in nodes:
                nodes.add(node)
            node_neighbors = ast.literal_eval(line[1])
            for k in node_neighbors.keys():
                edges.add((node, k, node_neighbors[k]))
                if k not in nodes:
                    nodes.add(k)
    return nodes, edges

# Plot Undirected Graph
G=nx.Graph()
nodes, edges = load_data('/Users/ssatpati/0-DATASCIENCE/DEV/github/ml/w261/wk7/synNet.txt')

#print "#Total Nodes: {0}".format(len(nodes))
#print "#Total Edges: {0}".format(len(edges))

# Load into networkx
for node in nodes:
    G.add_node(node)
for edge in edges:
    G.add_edge(edge[0], edge[1], weight=edge[2])

print G.number_of_nodes()
print G.number_of_edges()
print G.number_of_selfloops()

#print G.get_edge_data('1', '8233')
print algorithms.has_path(G,'1', '1042')
print algorithms.shortest_path(G,'1', '1042', 1)
print algorithms.has_path(G,'1', '8233')
sys.exit(1)

# Plot network
pos=nx.spring_layout(G)
nx.draw(G,pos, with_labels = True, node_color='g', node_size = 800)
# Specifiy Edge Labels
edge_labels=dict([((u,v,),d['weight']) for u,v,d in G.edges(data=True)])
nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
plt.title("Undirected Toy Example with Weights")
plt.show()

