from .. import SubgraphMatching as sgm
import itertools

def convert_adj_mat_to_adj_list(graph_adm):
    adj_lists = []
    for i in range(graph_adm.shape[0]):
        connections = graph_adm[i]
        adj_list = []
        for j in range(connections.shape[0]):
            if connections[j] == 1:
                adj_list.append(j)
        adj_lists.append(adj_list)
    return adj_lists


def convert_adj_list_to_graph_obj(graph_adl, node_labels, node_unique_ids=None):
    # Defaults
    if node_unique_ids is None:
        node_unique_ids = range(len(graph_adl))

    graph_class_input = {}
    for i in range(len(graph_adl)):
        # We are picking any element of set for now. Our set should only have one element.
        # label = next(iter(node_labels[i])) if len(node_labels[i]) > 0 else ''
        graph_class_input[node_unique_ids[i]] = (list(node_labels[i]), graph_adl[i])
    # print graph_class_input

    return sgm.Graph(graph_class_input)


def convert_adj_mat_to_graph_obj(graph_adm, graph_labels, node_unique_ids=None):
    graph_adl = convert_adj_mat_to_adj_list(graph_adm)
    return convert_adj_list_to_graph_obj(graph_adl, graph_labels, node_unique_ids)


def convert_motifs_into_motif_graph(motifs_list):
    """ Convert a list of motifs into weighted motif graph.

    Eah motif in the provided list is a node in the new graph and weight of edge between two motifs indicates number
    of vertices two motifs share.
    The returned graph will be in an adjacency matrix notation of size nxn where n is size of motifs list.
    Row(or column) index of matrix will directly match with index in the provided list.
    :param motifs_list: list of motifs where each motif is represented by a tuple of vertices.
    So this basically a list of typles. e.g. [(2,10,5), (5,19,34), .....] means that in the original graph (2,10,5) form
    one motif, (5, 19, 34) form another motif and so on
    :return: Graph where each motif is one single node. Graph returned is in form of adjacency matrix as described above.
    """
    # This code is linear in size of motifs_list
    # 1. First build a dictionary mapping vertex to set of motifs it occurs in.
    # 2. Iterate over dictionary and create final motif graph.
    vertex_to_motif_set_mapping = __build_vertex_to_motif_set_dict(motifs_list)
    motif_graph = {}
    for vertex, motifs_set in vertex_to_motif_set_mapping.iteritems():
        # all motifs in motifs_set share vertex, so they should be connected in the final graph.
        __update_adjcency_list(motif_graph, motifs_set)
    return motif_graph


def __update_adjcency_list(motif_graph, motifs_set):
    """For all the pairs (a,b) of motifs in motif_set, create an edge from a to b, and from b to a in the motif_graph.

    If edge already exists, increment the weight.

    :param motif_graph: adjacency list representation of graph where each node is a motif.
    :param motifs_set: set of motifs.
    :return: None. updates the graph in place.
    """
    for motif_pair in itertools.combinations(motifs_set, 2):
        motif_1 = motif_pair[0]
        motif_2 = motif_pair[1]
        # We got both way because motif graph is undirected.
        __increment_edge_weight(motif_graph, motif_1, motif_2)
        __increment_edge_weight(motif_graph, motif_2, motif_1)


def __increment_edge_weight(motif_graph, from_v, to_v):
    """Increment edge weight between from_v and to_v in the graph.

    Creates an edge with weight 1 if it doesn't exist already.

    :param motif_graph: motif graph.
    :param from_v: from vertex.
    :param to_v: to vertex
    :return: None. updates graph in place.
    """
    # Initialize
    if from_v in motif_graph:
        from_v_adj_dict = motif_graph[from_v]
    else:
        from_v_adj_dict = {}
        # Add
        motif_graph[from_v] = from_v_adj_dict

    # If there is already an edge from from_v to to_v, then just increment the weight of the edge.
    # Otherwise create a new edge from from_v to to_v.
    if to_v in from_v_adj_dict:
        from_v_adj_dict[to_v] += 1
    else:
        from_v_adj_dict[to_v] = 1


def __build_vertex_to_motif_set_dict(motifs_list):
    """ Builds a dictionary, mapping each vertex to set of motifs it participates in.

    :param motifs_list: list of motifs where each motif is represented by a tuple of vertices.
    So this basically a list of typles. e.g. [(2,10,5), (5,19,34), .....] means that in the original graph (2,10,5) form
    one motif, (5, 19, 34) form another motif and so on
    :return: dictionary, mapping each vertex to set of motifs it participates in.
    """
    vertex_to_motif_set_mapping = {}
    for motif in motifs_list:
        # motif is a tuple of vetices.
        for vertex in motif:
            if vertex in vertex_to_motif_set_mapping:
                vertex_to_motif_set_mapping[vertex].add(motif)
            else:
                motifs_set = set()
                motifs_set.add(motif)
                vertex_to_motif_set_mapping[vertex] = motifs_set
    return vertex_to_motif_set_mapping


