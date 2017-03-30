import csv


def write_each_edge_as_csv_row(graph_adm, csv_file, from_vertex_lab="from_vertex", to_vertex_lab="to_vertex"):
    """Write all edges in the graph to a csv file.

    CSV file has two columns <from_vertex_lab, to_vertex_lab>. First column contains id of source vertex and second
    column contains id of destination vertex. id of a vertex is it's index in the provided adjacency matrix.

    :param graph_adm: Adjacency matrix representing graph.(a 2-d numpy array)
    :param csv_file: path of output csv file.
    :param from_vertex_lab: label of the from vertex column. Default: "from_vertex"
    :param to_vertex_lab: label of the to vertex column. Default: "to_vertex"
    :return: None. Just writes the file.
    """
    with open(csv_file, 'wb') as outcsv:
        writer = csv.writer(outcsv)
        # Write header.
        writer.writerow([from_vertex_lab, to_vertex_lab])
        # Write edges.
        num_vertices = graph_adm.shape[0]
        for row_index in range(num_vertices):
            for col_index in range(num_vertices):
                if graph_adm[row_index][col_index] != 0:
                    writer.writerow([row_index, col_index])


def write_node_names_to_csv(node_names, graph_labels, csv_file, node_ids=None,
                            id_lab="id", name_lab="name", labels_lab="labels"):
    """Write node names to a csv file.

    Csv file has two columns. First column contains id of the node/vertex. Second column contains the name of the node.
    id of a node is the index in the node_names list.

    :param node_names: a list like object containing names of the nodes.
    :param graph_labels: a list of sets where each element of set has labels of that node.
    :param csv_file: path of output csv file.
    :param id_lab: label of the id column. Default = "id"
    :param name_lab: label of the name column. Default = "name"
    :return: None. Just writes to csv.
    """
    # Default
    if node_ids is None:
        node_ids = range(len(node_names))

    with open(csv_file, 'wb') as outcsv:
        writer = csv.writer(outcsv)
        # Write header.
        writer.writerow([id_lab, name_lab, labels_lab])
        for i in range(len(node_names)):
            labels_str = ', '.join(str(e) for e in graph_labels[i])
            writer.writerow([node_ids[i], node_names[i], labels_str])

