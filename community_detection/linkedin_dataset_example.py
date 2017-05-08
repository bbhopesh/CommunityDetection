import core.utils.graph_representation_utils as gru
import core.SubgraphMatching as sm
import time

adj_list = gru.convert_ego_network_files_into_adj_list("./core/ego_dataset")
# print "# nodes: {}, # edges: {}".format(len(adj_list), sum([len(j) for i,j in adj_list.items()])/2)
graph = gru.get_graph_object(adj_list)


'''motif_list = sm.SubgraphMatching(graph, [["university of illinois at urbana-champaign",\
                                              ["shanghai jiao tong university", "google"]],\
                                             ["shanghai jiao tong university", ["google"]]], True)'''

'''motif_list = sm.SubgraphMatching(graph, [["university of illinois at urbana-champaign",\
                                              ["facebook", "google"]],\
                                             ["facebook", ["google"]]], True)'''

'''motif_list = sm.SubgraphMatching(graph, [["university of illinois at urbana-champaign",\
                                              ["university of illinois at urbana-champaign", "google"]],\
                                             ["university of illinois at urbana-champaign", ["google"]]], True)'''

motif_list = sm.SubgraphMatching(graph, [["facebook", ["facebook","facebook","facebook", "facebook"]]], True, "star", 5)

start = time.clock()
motif_graph = gru.convert_motifs_into_motif_graph(motif_list)
print "----------------------------------------------------------------------"
print "network construction time: {}".format(time.clock()-start)

networkx_graph_object, table, table_inv = gru.convert_motif_graph_to_network_graph_object(motif_graph)

mid = time.clock()
clusters = gru.generate_graph_clusters(0, networkx_graph_object, table_inv)
'''
for key in clusters[1]:
    print key
    print clusters[0][clusters[1][key]]
    break
'''
# print clusters
print "clustering time: {} , # clusters: {}".format(time.clock()-mid, len(clusters[0]))


cluster_no = 0
for cluster in clusters[0]:
    cluster_no += 1
    motif_nodes = set()
    all_motif_nodes_and_connecting_nodes = set()
    for motif in cluster:
        for node in motif:
            motif_nodes.add(node)
            all_motif_nodes_and_connecting_nodes.add(node)
            node_data = adj_list[node]
            node_adj_list = [a["id"] for a in node_data["adjacencies"]]
            for n in node_adj_list:
                all_motif_nodes_and_connecting_nodes.add(n)

    output_graph = {}
    for node in all_motif_nodes_and_connecting_nodes:
        node_data = adj_list[node]
        if node in motif_nodes:
            node_adj_list = [a["id"] for a in node_data["adjacencies"]]
        else:
            node_adj_list = []
        node_attributes_all = [node_data["location"]] + node_data["education"] + node_data["employers"]
        #node_attributes_all = node_data["education"] + node_data["employers"]
        # add relevant attirbutes from our search at top
        node_attributes = []
        for node_attribute in node_attributes_all:
            #if node_attribute in ["university of illinois at urbana-champaign", "shanghai jiao tong university", "google"]:
            #if node_attribute in ["facebook"]:
            if True:
                node_attributes.append(node_attribute)
        node_output_data = {}
        node_output_data["adjacencies"] = node_adj_list
        node_output_data["attributes"] = node_attributes
        output_graph[node] = node_output_data


    #csv_vertices_file = "triangle_motif_vertices.csv"
    #csv_edges_file = "triangle_motif_edges.csv"

    csv_vertices_file = "star_motif_vertices_cluster{0}.csv".format(cluster_no)
    csv_edges_file = "star_motif_edges_cluster{0}.csv".format(cluster_no)

    import csv
    with open(csv_vertices_file, 'wb') as outcsv:
            writer = csv.writer(outcsv)
            # Write header.
            writer.writerow(["id", "labels"])
            for node in output_graph:
                labels_str = ', '.join(str(e) for e in output_graph[node]["attributes"])
                writer.writerow([node, labels_str])

    import csv
    with open(csv_edges_file, 'wb') as outcsv:
            writer = csv.writer(outcsv)
            # Write header.
            writer.writerow(["from", "to"])
            for node in output_graph:
                neighbours = output_graph[node]["adjacencies"]
                for neighbour in neighbours:
                    writer.writerow([node,neighbour])
