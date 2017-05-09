DIRECTORY LAYOUT (inside of community detection):

	 core/ A directory containing core GSPD functions
	
	 	 data_gen/ A directory containing scripts used to generate synthetic data
	 	
	 	 ego_dataset/ A directory containing the text files from the EgoNet-UIUC dataset
	 	 
	 	 utils/ A directory containing the scripts which contain the function definitions that are core to this project's purpose
	 	
	 	 SubgraphMatching.py A script containing the class definition for a graph structure used in the STwig paper
	 	

	 linkedin_dataset_example.py A script that we use to perform experimentation. Presenlty configured with a triangle motif, with comments as to how to perform subsequent experiments with other motifs
	 
	 load_neo4j.cypher A file denoting instruction as to how to load an output csv of our system into neo4j's cypher for visualization
	
	 single_label_triangle_example.py A file that we used for testing 
	
	 star_motif_edges_cluster$N.csv A csv file containing edges for different clusters found using the star motif
	
	 star_motif_verticies_cluster$N.csv A csv file containing verticies for different clusters found using the star motif
	
	 star_motif_original_nodes.json A json file containing a serialization of all nodes in the stars motif network cluster
	
	 triangle_motif_edges.csv A csv containing all edges found utilizing a triangle motif 
	
	 triangle_motif_edges_cluster$N.csv A csv containing all edges in the Nth cluster found using the triangle motif
	
	 triangle_motif_example.py  A testing script used to test code correctness.
	
	 triangle_motif_original_nodes.json A json file containing a serialization of all nodes in the triangle motif network cluster
	
	 triangle_motif_nodes_cluster$N.csv A csv containing all nodes in the Nth cluster found using the triangle motif



TO REPLICATE EXPERIMENTATION
To replicate experimenation, simply run the python script *linkedin_dataset_example.py* utilizing python.

