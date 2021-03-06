import numpy as np
import core.data_gen.data_gen as dg
import core.data_gen.motif_position_chooser as mpc
import core.utils.neo4j_utils as nu
import core.utils.graph_representation_utils as gru
import core.SubgraphMatching as sm


# Output files. These files will be written by this script and can be loaded into neo4j for visualization.
vertices_file = "vertices.csv"
edges_file = "edges.csv"

# Constants.
triangle_motif_adm = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]]) # adm means adjacency matrix.
graph_size = 1000
num_motifs = 300 # number of motifs to be inserted in graph.

motif_size = triangle_motif_adm.shape[0]

# Prepare motif labels. Each element of list is set. First set will contain labels for first node,
# second set for second node and so on.
# Currently each set has just one label because our initial algorithm can only handle one label per node.
triangle_motif_labels = [set() for _ in range(3)]
triangle_motif_labels[0].add('A')
triangle_motif_labels[0].add('D')
triangle_motif_labels[1].add('B')
triangle_motif_labels[1].add('E')
triangle_motif_labels[2].add('C')
triangle_motif_labels[2].add('F')


# Create a motif position chooser. This object will be called repeatedly to get the positions where motif should be
# inserted. In this example, we are using a chooser which makes a node part of any motif atmost once.
# This is because our initial algorithm can only handle one label per node.
# no_overlap_mpc = mpc.NoOverlappingVerticesPositionChooser(graph_size, motif_size)
overlap_mpc = mpc.UniformDistMotifPositionChooser(graph_size, motif_size)

# Create graph. adm means adjacency matrix. Change prob to create edges other than motif(check function docs)
# graph_adm, graph_labels = dg.create_graph_with_motif(graph_size, triangle_motif_adm, triangle_motif_labels, no_overlap_mpc, num_motifs, prob=0.002)
graph_adm, graph_labels = dg.create_graph_with_motif(graph_size, triangle_motif_adm, triangle_motif_labels, overlap_mpc, num_motifs, prob=0.002)

# Save graph.
# Write edges.
nu.write_each_edge_as_csv_row(graph_adm, edges_file)
# Write vertices. Name vertices like Node0, Node1, Node2....
vertices_names = []
for i in range(graph_adm.shape[0]):
    vertices_names.append("Node{0}".format(i))
nu.write_node_names_to_csv(vertices_names, graph_labels, vertices_file)

'''
# That's how you create Graph object
adj_list = gru.convert_ego_network_files_into_adj_list("./core/ego_dataset")
# tian_graph_obj = gru.convert_adj_mat_to_graph_obj(graph_adm, graph_labels)
graph = gru.get_graph_object(adj_list)

# motif_list = sm.SubgraphMatching(graph, [["A",["B", "C"]], ["B", ["C"]]])
motif_list = sm.SubgraphMatching(graph, [["university of illinois at urbana-champaign",\
                                              ["shanghai jiao tong university", "google"]],\
                                             ["shanghai jiao tong university", ["google"]]])
motif_graph = gru.convert_motifs_into_motif_graph(motif_list)
# print motif_graph

# motif_graph = None
networkx_graph_object = gru.convert_motif_graph_to_network_graph_object(motif_graph)
clusters = gru.generate_graph_clusters(5, networkx_graph_object)
print clusters
'''
# Look at load_neo4j.cypher next.
