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


def convert_adj_list_to_graph_obj(graph_adl, node_unique_ids=None, node_labels=None):
    # Defaults
    if node_unique_ids is None:
        node_unique_ids = range(len(graph_adl))
    if node_labels is None:
        node_labels = ['' for i in range(len(graph_adl))]

    graph_class_input = {}
    for i in range(len(graph_adl)):
        graph_class_input[node_unique_ids[i]] = (node_labels[i], graph_adl[i])

    return sgm.Graph(graph_class_input)

def convert_adj_mat_to_graph_obj(graph_adm, node_unique_ids=None, node_labels=None):
    graph_adl = convert_adj_mat_to_adj_list(graph_adm)
    return convert_adj_list_to_graph_obj(graph_adl)

