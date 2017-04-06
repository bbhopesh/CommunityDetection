import itertools as it
import time

# graph data structure
class Graph():
    # store graph as adjacency list (hash table)
    # store mapping between id and label
    def __init__(self, graph):
        self.graph = {g:graph[g][1] for g in graph}
        self.label_id = {}
        self.id_label = {}
        
        for g in graph:
            self.id_label[g] = graph[g][0]
            for i in graph[g][0]:
                if i not in self.label_id:
                    self.label_id[i] = [g]
                else:
                    self.label_id[i].append(g)
    
    # given id, return id of neighbors
    def Load(self, id):
        return self.graph[id]
        
    # given label, return id
    def getID(self, label):
        return self.label_id[label]
        
    # check id has given label
    def hasLabel(self, id, label):
        return label in self.id_label[id]

    # given root label and labels of child nodes, return STwig
    def MatchSTwig(self, r, L):
        Sr = self.getID(r)
        R = set()
        for n in Sr:
            c = self.Load(n)
            Sl = []
            for l in L:
                Sl.append(set([i for i in c if self.hasLabel(i, l)]))
            candidates = [[n]] + [list(i) for i in Sl]
            R.add(tuple(set([i for i in it.product(*candidates)])))
        return [i[0] for i in R if len(i) != 0]
        
    # get binding info, Hx is all labels that match x
    def getBinding(self, H):
        return {h:set(self.label_id[h]) for h in H}

def SubgraphMatching(graph, decomp):
    """graph = Graph({"A1":(["Alice", "Carl"], ["B1","D1","E1"]),\
        "B1":(["Bob"], ["A1","C1","D1"]), "C1":(["Carl"], ["B1","E1","A2"]),\
        "D1":(["David"], ["A1","B1"]), "E1":(["Emily"], ["A1","C1","B2"]),\
        "A2":(["Alice"], ["C1"]), "B2":(["Bob"], ["C2","D2"]),\
        "C2":(["Carl"], ["B2","D2"]), "D2":(["David"], ["B2","C2"])})"""
        
    """print graph.label_id, graph.id_label, graph.Load("A1"),\
        graph.getID("Alice"), graph.graph"""
    
    start = time.time()
    r1 = graph.MatchSTwig(*decomp[0])
    r2 = graph.MatchSTwig(*decomp[1])
    query = tuple(set([i[0] for i in decomp] +\
        [j for j in i[1] for i in decomp]))
    binding = graph.getBinding(query)
    # print r1, r2, binding
    
    mid = time.time()
    res = set()
    dot = [i for i in it.product(r1, r2)]
    for l in dot:
        candidate = set([item for sublist in l for item in sublist])
        cnt = []
        for i in binding:
            cnt.append(len(binding[i] & candidate))
        if all(i <= 1 for i in cnt):
            res.add(tuple(candidate))
    print res
    end = time.time()
    print "Total query time:", end-start
    print "MatchSTwig phase:", mid-start, "\nJoining phase:",end-mid
    
    return res

# SubgraphMatching(None, [["Bob", ["Carl", "David"]], ["Carl", ["David"]]])
    