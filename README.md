## Directory Layout (inside of community\_detection):
> core/ A directory containing core GSPD functions
>
> > data\_gen/ A directory containing scripts used to generate synthetic data
> >
> > ego\_dataset/ A directory containing the text files from the EgoNet-UIUC dataset
> > 
> > utils/ A directory containing the scripts which contain the function definitions that are core to this project's purpose
> >
> > SubgraphMatching.py A script containing the class definition for a graph structure used in the STwig paper
> >

> linkedin\_dataset\_example.py A script that we use to perform experimentation. Presenlty configured with a triangle motif, with comments as to how to perform subsequent experiments with other motifs
> 
> load\_neo4j.cypher A file denoting instruction as to how to load an output csv of our system into neo4j's cypher for visualization
>
> single\_label\_triangle\_example.py A file that we used for testing 
>
> star\_motif\_edges\_cluster$N.csv A csv file containing edges for different clusters found using the star motif
>
> star\_motif\_verticies\_cluster$N.csv A csv file containing verticies for different clusters found using the star motif
>
> star\_motif\_original\_nodes.json A json file containing a serialization of all nodes in the stars motif network cluster
>
> triangle\_motif\_edges.csv A csv containing all edges found utilizing a triangle motif 
>
> triangle\_motif\_edges\_cluster$N.csv A csv containing all edges in the Nth cluster found using the triangle motif
>
> triangle\_motif\_example.py  A testing script used to test code correctness.
>
> triangle\_motif\_original\_nodes.json A json file containing a serialization of all nodes in the triangle motif network cluster
>
> triangle\_motif\_nodes\_cluster$N.csv A csv containing all nodes in the Nth cluster found using the triangle motif



# To replicate experimentation
To replicate experimenation, simply run the python script *linkedin\_dataset\_example.py* utilizing python.



# Presentation
Uploaded in the repository as `Presentation.pdf` <br/>
Google slides https://docs.google.com/presentation/d/1lGMQaSso7ss6bR-eZTxzce3ivO9Ogdf29piCdQarTg8/edit?usp=sharing



# Report
Uploaded in the repository as `Report.pdf`
