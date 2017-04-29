import core.utils.graph_representation_utils as gru
import core.SubgraphMatching as sm

adj_list = gru.convert_ego_network_files_into_adj_list("./core/ego_dataset")
graph = gru.get_graph_object(adj_list)

motif_list = sm.SubgraphMatching(graph, [["university of illinois at urbana-champaign",\
                                              ["shanghai jiao tong university", "google"]],\
                                             ["shanghai jiao tong university", ["google"]]])
motif_graph = gru.convert_motifs_into_motif_graph(motif_list)

networkx_graph_object, table = gru.convert_motif_graph_to_network_graph_object(motif_graph)
clusters = gru.generate_graph_clusters(5, networkx_graph_object)
print clusters
