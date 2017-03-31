import numpy as np


def create_graph_with_motif(graph_size, motif_adm, motif_labels, motif_pos_chooser, num_motif, prob=0.5):
    """Creates an empty graph of given size and inserts num_motif motifs of type motif_adm.

    Positions at which motifs have to be inserted in graph is chosen by using motif_pos_chooser.
    Once provided number of motifs are inserted in the graph, we create edges between any two pair of vertices with
    probability=prob.

    :param graph_size: Size of the graph.
    :param motif_adm: Adjacency matrix representing motif.(a 2-d numpy array)
    :param motif_labels: a list of set containing labels for each node in the motif.
    Outer list size should be equal to size of motif and each inner set contains labels for a node in the motif.
     e.g. if the motif size is 3 and this param is [{boy, student, player}, {girl, student}, {college}],
     then first node in motif has labels boy, student and player, second node in motif has labels girl,student,
     and third node in motif has label college.
    :param motif_pos_chooser: Object with which we choose positions to insert motifs.
    :param num_motif: number of motifs to be inserted in the graph.
    :param prob: Probability with which edges should be created in graph after inserting motifs.
    :return: Return a 2-tuple where
    first element is an adjacency (square) matrix of size graph_size*graph_size.(a 2-d numpy array)
    and second element is a list of sets denoting labels of each node in the graph.
    """
    # Initialize a empty graph. Adjacency matrix of size graph_size*graph_size
    graph_adm = np.zeros([graph_size, graph_size])
    # Initialize list of set to store labels of each node in the graph.
    graph_labels = np.array([set() for _ in range(graph_size)])

    # Repeatedly insert motifs in the graph.
    for i in range(num_motif):
        # choose next position for inserting motif.
        motif_pos = motif_pos_chooser.next_motif_position()
        # Insert motif
        insert_motif(graph_adm, graph_labels, motif_adm, motif_labels, motif_pos)
    # Set edges not involved in any motif with probability = prob
    graph_adm = set_edges(graph_adm, prob)
    return graph_adm, graph_labels


def insert_motif(graph_adm, graph_labels, motif_adm, motif_labels, motif_pos):
    """Insert given motif in the given graph at the given position.

    :param graph_adm: Adjacency matrix representing graph.(a 2-d numpy array)
    :param graph_labels list of sets containing labels of each node in the graph.
    :param motif_adm: Adjacency matrix representing motif.(a 2-d numpy array)
    :param motif_labels: a list of set containing labels for each node in the motif.
    Outer list size should be equal to size of motif and each inner set contains labels for a node in the motif.
     e.g. if the motif size is 3 and this param is [{boy, student, player}, {girl, student}, {college}],
     then first node in motif has labels boy, student and player, second node in motif has labels girl,student,
     and third node in motif has label college.
    :param motif_pos: position at which motif is to be inserted. This should be a tuple of size equal to motif size.
    :return: None. Changes provided graph in place.
    """
    # both adjacency matrices are supposed to be square matrices.
    motif_dim = motif_adm.shape[0]
    for motif_row_index in range(motif_dim):
        graph_row_index = motif_pos[motif_row_index]
        # add edges
        for motif_col_index in range(motif_dim):
            graph_col_index = motif_pos[motif_col_index]
            # Set value if necessary.
            # We never set an edge to be 0 because even if it doesn't exist in current motif,
            # it might be set from some other motif.
            if motif_adm[motif_row_index][motif_col_index] != 0:
                graph_adm[graph_row_index][graph_col_index] = motif_adm[motif_row_index][motif_col_index]
        # add labels.
        labels_curr_node = graph_labels[graph_row_index] # labels of current node.
        labels_curr_node.update(motif_labels[motif_row_index])




def set_edges(graph_adm, prob):
    """Set edges in the graph with probability=prob.

    :param graph_adm: (a 2-d numpy array)
    :param prob: Probability with which edges should be inserted.
    :return: New graph.(a 2-d numpy array)
    """
    # Element wise op will be called for each element of graph adjacency matrix.
    # If edge doesn't exist, we create it with probability=prob
    def element_wise_op(x):
        # Draw a random number between 0 and 1. Set edge only if number is less than prob.
        p = np.random.random()
        return 1 if (x == 0 and p < prob) else x
    vectorized_element_wise_op = np.vectorize(element_wise_op, otypes=[np.float])
    return vectorized_element_wise_op(graph_adm)
