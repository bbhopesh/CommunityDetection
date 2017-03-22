// Move files edges.csv and vertices.csv to /usr/share/neo4j/import before running following statements..

// Create nodes.
LOAD CSV WITH HEADERS FROM "file:///vertices.csv" AS node
CREATE (n:Node { id: toInteger(node.id), name: node.name })


// Create edges.
LOAD CSV WITH HEADERS FROM "file:///edges.csv" AS edge
MERGE (from:Node { id: toInteger(edge.from_vertex)})
MERGE (to:Node { id: toInteger(edge.to_vertex)})
CREATE (from)-[:E]->(to)
