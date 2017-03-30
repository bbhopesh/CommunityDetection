import numpy as np
import core.data_gen.data_gen as dg
import core.data_gen.motif_position_chooser as mpc
import core.utils.neo4j_utils as nu

# Output files. These files will be written by this script and can be loaded into neo4j for visualization.
vertices_file = "vertices.csv"
edges_file = "edges.csv"

# Constants.
triangle_motif_adm = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]]) # adm means adjacency matrix.
graph_size = 1000
num_motifs = 100 # number of motifs to be inserted in graph.

motif_size = triangle_motif_adm.shape[0]

# Create a motif position chooser. This object will be called repeatedly to get the positions where motif should be
# inserted. In this example, we are using uniform chooser which picks position from a uniform distribution over all
# available positions. I will soon implement one which picks from a distribution that prefers already chosen positions.
# This new chooser can be used to create strongly connected communities.
uni_mpc = mpc.UniformDistMotifPositionChooser(graph_size, motif_size)

# Create graph. adm means adjacency matrix. Change prob to create edges other than motif(check function docs)
graph_adm = dg.create_graph_with_motif(graph_size, triangle_motif_adm, uni_mpc, num_motifs, prob=0.0001)

# Save graph.
# Write edges.
nu.write_each_edge_as_csv_row(graph_adm, edges_file)
# Write vertices. Name vertices like Node0, Node1, Node2....
vertices_names = []
for i in range(graph_adm.shape[0]):
    vertices_names.append("Node{0}".format(i))
nu.write_node_names_to_csv(vertices_names, vertices_file)

# Look at load_neo4j.cypher next.

