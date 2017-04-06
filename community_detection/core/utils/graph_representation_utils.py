import core.SubgraphMatching as sgm


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
    print graph_class_input

    return sgm.Graph(graph_class_input)


def convert_adj_mat_to_graph_obj(graph_adm, graph_labels, node_unique_ids=None):
    graph_adl = convert_adj_mat_to_adj_list(graph_adm)
    return convert_adj_list_to_graph_obj(graph_adl, graph_labels)

