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
        return [i for s in R for i in s if len(s) != 0]
        
    # get binding info, Hx is all labels that match x
    def getBinding(self, H):
        return {h:set(self.label_id[h]) for h in H}

def triangle_check(pre, graph, size):
    res = []
    for i in pre:
        if all(i[(j+1) % size] in graph.graph[i[j]] for j in range(size)):
            res.append(i)
    return res

def star_check(pre, graph):
    res = []
    for i in pre:
        nodes = set(i)
        if any(all(k in graph.graph[j] for k in nodes-set([j])) for j in nodes):
            res.append(i)
    return res

def SubgraphMatching(graph, decomp, one_level = False, type = "triangle", size = 3):
    
    # print graph.label_id, graph.id_label, graph.graph    
    start = time.time()
    r1 = graph.MatchSTwig(*decomp[0])
    if one_level == True:
        r2 = [()]
    else:
        r2 = graph.MatchSTwig(*decomp[1])

    query = tuple(set([i[0] for i in decomp] +\
        [j for j in i[1] for i in decomp]))
    # binding = graph.getBinding(query)
    # print len(r1), len(r2), query
    
    mid = time.time()
    res = set()
    for l in it.product(r1, r2):
        candidate = set([i for s in l for i in s])
        if len(candidate) == size:
            res.add(tuple(sorted(candidate)))

    if type == "triangle":
        res = triangle_check(res, graph, size)
    if type == "star":
        res = star_check(res, graph)
    end = time.time()
    
    #print res
    print "Total query time:", end-start, "\tCount:", len(res)
    print "MatchSTwig phase:", mid-start, "\tJoining phase:",end-mid
    
    return res

"""g1 = Graph({0:([["C","F"],[3,6]]), 1:[["A","D"],[5,8]],\
    3:[["B","E"],[0,6]], 5:[["C","F"],[1,8]], 6:[["A","C","D","F"],\
    [0,3,7,8]], 7:[["A","D"],[6,8]], 8:[["B","E"],[1,5,6,7]]})
SubgraphMatching(g1, [["A", ["B", "C"]], ["B", ["C"]]])"""
    
