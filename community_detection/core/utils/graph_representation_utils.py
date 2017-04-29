from .. import SubgraphMatching as sgm
import itertools
import os
import networkx as nx
from hac import GreedyAgglomerativeClusterer as Clusterer
import matplotlib.pyplot as plt
import time

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
    :param motifs_list: list of motifs where each motif is represented by a tuple of vertices.
    So this basically a list of typles. e.g. [(2,10,5), (5,19,34), .....] means that in the original graph (2,10,5) form
    one motif, (5, 19, 34) form another motif and so on
    :return: Graph where each motif is one single node. Graph returned is in form of adjacency list.
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


'''
    Function: convert_ego_network_files_into_adj_list
    Parameter: (String) file_location_dir A string representing the directory, not having a "/" appended
                containing the  EgoNetUIUC Files "label.txt", "network.txt","college.txt",
                "employer.txt", and "location.txt"

    Returns: A dict of the following structure:
    {
        "id" => ...
        "id" => {
            "adjacencies" => [{"id": "id1", "type":"L1-L8"},{"id":"id2","type":""}],
            "education" => ["Institution 1", ...],
            "employers" => ["Institution 1", ...],
            "location" => "some place"
        },
        "id" => ...
    }


    Edge Cases:
        Adjacencies MAY be an empty list
        The "type" attribute on an adjacency MAY be an empty string
        If an adjacency is present on one node, there MUST be another node in the dict with the adjacent ID
        The "education" and "employers" attributes MAY be an empty list
        The "location" attribute MAY be an empty string
'''
def convert_ego_network_files_into_adj_list(file_location_dir):
    assert os.path.isdir(file_location_dir), "Parameter file_location_dir must be a directory containing the EgoNetUIUC files"
    assert os.path.exists(file_location_dir + "/label.txt"), "Error, file 'label.txt' is missing"
    assert os.path.exists(file_location_dir + "/network.txt"), "Error, file 'network.txt' is missing"
    assert os.path.exists(file_location_dir + "/college.txt"), "Error, file 'colelge.txt' is missing"
    assert os.path.exists(file_location_dir + "/employer.txt"), "Error, file 'employer.txt' is missing"
    assert os.path.exists(file_location_dir + "/location.txt"), "Error, file 'location.txt' is missing"

    adj_list = {}

    #Building the initial network structure
    with open(file_location_dir + "/network.txt") as network:
        for line in network:
            edge = line.split()
            assert len(edge) == 3, "Error reading line " + line

            ego_id = edge[0]
            from_id = edge[1]
            to_id = edge[2]

            verify_exists = [from_id, to_id]

            for uid in verify_exists:
                if uid not in adj_list:
                    adj_list[uid] = {}
                    adj_list[uid]["adjacencies"] = []
                    adj_list[uid]["education"] = []
                    adj_list[uid]["employers"] = []
                    adj_list[uid]["location"] = ""

            relationship = {}
            relationship["type"] = ""
            relationship["id"] = to_id

            adj_list[from_id]["adjacencies"].append(relationship)

    #Adding relationship labeling on relations. Since it is ego centric,
    # there is no promise that the other side of the relationship views
    # the relationship in the same way, thus we need to only alter one relation dict
    with open(file_location_dir + "/label.txt") as labels:
        for line in labels:
            labeling = line.split()
            assert len(labeling) == 3

            from_id = labeling[0]
            to_id = labeling[1]
            label_id = labeling[2]

            assert from_id in adj_list, "Error, node " + from_id + " not in adj list"
            assert to_id in adj_list, "Error, node " + to_id + " not in adj list"

            for edge in adj_list[from_id]["adjacencies"]:
                if edge["id"] == to_id:
                    edge["type"] = label_id
                    break

    with open(file_location_dir + "/college.txt") as education:
        uid = education.readline().strip()
        while uid:
            count = education.readline().strip()

            for institution in range(0, int(count)):
                place = education.readline().strip()
                adj_list[uid]["education"].append(place)
            uid = education.readline().strip()

    with open(file_location_dir + "/employer.txt") as education:
        uid = education.readline().strip()
        while uid:
            count = education.readline().strip()

            for institution in range(0, int(count)):
                place = education.readline().strip()
                adj_list[uid]["employers"].append(place)
            uid = education.readline().strip()

    with open(file_location_dir + "/location.txt") as education:
        uid = education.readline().strip()
        while uid:
            count = education.readline().strip()

            for institution in range(0, int(count)):
                place = education.readline().strip()
                adj_list[uid]["location"] = place # only 1 location is present in the text file
            uid = education.readline().strip()

    return adj_list

# create a graph object
def get_graph_object(data):
    graph = {}
    for i in data:
        j = data[i]
        graph[i] = ([j["location"]] + j["education"] + j["employers"],\
                        [a["id"] for a in j["adjacencies"]])
    # print graph
    return sgm.Graph(graph)

# convert adjacency list to network x graph object
def convert_motif_graph_to_network_graph_object(adjacency_list):

    # map the motifs to integer
    table = {}
    cnt = 0
    for motif in adjacency_list:
        table[motif] = cnt
        cnt += 1

    # generate a networkx graph
    graph = nx.Graph()
    graph.add_nodes_from(range(cnt))
    for motif in adjacency_list:
        for neighbor, w in adjacency_list[motif].items():
            graph.add_edge(table[motif], table[neighbor], weight = w)

    # print nx.draw(graph)
    # plt.show()
    return graph, table

# generate clusters
# num_of_cluster = 0 if let the algorithm choose
def generate_graph_clusters(num_of_clusters, graph):
    start = time.clock()
    communities = Clusterer().cluster(graph)
    if num_of_clusters == 0:
        return communities.clusters(), communities.labels(),\
            "clustering finished in {}".format((time.clock()-start))
    else:
        return communities.clusters(num_of_clusters), communities.labels(),\
            "clustering finished in {}".format((time.clock()-start))


'''
    Function: convert_snap_comm_dataset_into_adj_list
    Parameter: (String) file_location_dir A string representing the directory, not having a "/" appended
                containing the desired dataset.

                (String) dataset_name A string representing the name of the dataset file

    Returns: A dict of the following structure:
    {
        "id" => ...
        "id" => ['toId1','toId2',...]
        "id" => ...
    }

    Wherein "id" represents the ID of a node and its corresponding list is the list of ID's


    Edge Cases:
        The snap community dataset data files typically includes about 4 lines of comments. Remove these lines first otherwise
        The below code will break.
'''
def convert_snap_comm_dataset_into_adj_list(file_location_dir, fileName):
    assert os.path.isdir(file_location_dir), "Parameter file_location_dir must be a directory containing the SNAP Dataset files"
    assert os.path.exists(file_location_dir + "/" + fileName), "Error, file '" + fileName +"' is missing"

    adj_list = {}

    with open(file_location_dir + "/" + fileName) as labels:
        for line in labels:
            ids = line.split()
            assert len(ids) is 2, "Oops, accidentally read this line:" + line + " , please remove it from the dataset file."
            fromId = ids[0]
            toId = ids[1]

            if not fromId in adj_list:
                adj_list[fromId] = []

            if not toId in adj_list:
                adj_list[toId] = []

            # These datasets are  undirected but the lines aren't isomorphic (we have a 0 1 relationship but not 1 0 in the dataset)
            adj_list[fromId].append(toId)
            adj_list[toId].append(fromId)

    return adj_list

'''
    Function: convert_snap_comm_dataset_into_adj_list
    Parameter: (String) file_location_dir A string representing the directory, not having a "/" appended
                containing the desired dataset.

                (String) dataset_name A string representing the name of the ground truth dataset file

    Returns: A dict of the following structure:
    {
        "id" => ...
        "id" => ['toId1','toId2',...]
        "id" => ...
    }

    Wherein "id" represents the ID of a node and its corresponding list is the list of ID's

    Edge Cases:
        Unknown at this time
'''
def convert_snap_ground_truth_comm_into_adj_list(file_location_dir, fileName):
    assert os.path.isdir(file_location_dir), "Parameter file_location_dir must be a directory containing the SNAP Dataset files"
    assert os.path.exists(file_location_dir + "/" + fileName), "Error, file '" + fileName +"' is missing"

    adj_list = {}
    count = 0
    with open(file_location_dir + "/" + fileName) as labels:
        for line in labels:
            count +=1
            ids = line.split()
            print "Community " + str(count) + " size of " + str(len(ids))
            for node_id in ids:
                for to_id in ids[ids.index(node_id)+1:]:

                    if not node_id in adj_list:
                        adj_list[node_id] = []

                    if not to_id in adj_list:
                        adj_list[to_id] = []

                    if not to_id in adj_list[node_id]:
                        adj_list[node_id].append(to_id)

                    if not node_id in adj_list[to_id]:
                        adj_list[to_id].append(node_id)

    return adj_list

