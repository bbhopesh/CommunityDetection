import core.utils.graph_representation_utils as gru
import core.SubgraphMatching as sm
import time

adj_list = gru.convert_ego_network_files_into_adj_list("./core/ego_dataset")
# print "# nodes: {}, # edges: {}".format(len(adj_list), sum([len(j) for i,j in adj_list.items()])/2)
graph = gru.get_graph_object(adj_list)

motif_list = sm.SubgraphMatching(graph, [["university of illinois at urbana-champaign",\
                                              ["shanghai jiao tong university", "google"]],\
                                             ["shanghai jiao tong university", ["google"]]], True)

'''motif_list = sm.SubgraphMatching(graph, [["university of illinois at urbana-champaign",\
                                              ["facebook", "google"]],\
                                             ["facebook", ["google"]]], True)'''

'''motif_list = sm.SubgraphMatching(graph, [["university of illinois at urbana-champaign",\
                                              ["university of illinois at urbana-champaign", "google"]],\
                                             ["university of illinois at urbana-champaign", ["google"]]], True)'''

'''motif_list = sm.SubgraphMatching(graph, [["facebook", ["facebook","facebook","facebook", "facebook"]]], True, "star", 5)'''

start = time.clock()
motif_graph = gru.convert_motifs_into_motif_graph(motif_list)
print "network construction time: {}".format(time.clock()-start)

networkx_graph_object, table, table_inv = gru.convert_motif_graph_to_network_graph_object(motif_graph)

mid = time.clock()
clusters = gru.generate_graph_clusters(0, networkx_graph_object, table_inv)
print clusters
print "clustering time: {} , # clusters: {}".format(time.clock()-mid, len(clusters[0]))
