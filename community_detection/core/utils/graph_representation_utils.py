import core.SubgraphMatching as sgm
import os
import re

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
    return convert_adj_list_to_graph_obj(graph_adl, graph_labels)

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
