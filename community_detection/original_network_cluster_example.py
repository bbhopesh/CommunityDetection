import time
import networkx as nx
import core.utils.graph_representation_utils as gru
from hac import GreedyAgglomerativeClusterer as Clusterer
import matplotlib.pyplot as plt

adj_list = gru.convert_ego_network_files_into_adj_list("./core/ego_dataset")
print "# nodes: {}, # edges: {}".format(len(adj_list), sum([len(j) for i,j in adj_list.items()])/2)

table = {}
cnt = 0
for motif in adj_list:
    table[motif] = cnt
    cnt += 1

start = time.clock()
graph = nx.Graph()
for motif in adj_list:
    for neighbor in adj_list[motif]["adjacencies"]:
        graph.add_edge(table[motif], table[neighbor["id"]])

print nx.draw(graph)
plt.show()
# communities = Clusterer().cluster(graph).clusters()
# print communities, "clustering time: {}, # of clusters: {}".format(time.clock()-start, len(communities))
