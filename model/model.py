import copy

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._airports=DAO.getAllAirports()
        self._idMapAirports={}
        self._graph=nx.Graph()
        for a in self._airports:
            self._idMapAirports[a.ID]=a
        self._bestCammino=[]
        self._bestScore=0
    
    def buildGraph(self,nMin):
        nodes=DAO.getAllNodes(nMin,self._idMapAirports)

        self._graph.add_nodes_from(nodes)

        self.addEdges()


    def addEdges(self):
        allTratte=DAO.getAllEdgesV1(self._idMapAirports)
        #queste tratte hanno 2 problemi ho archi diretti e inversi,ho archi fra aeroporti che avevo filtrato
        for t in allTratte:
            if t.aeroportoP in self._graph and t.aeroportoA in self._graph:
                if self._graph.has_edge(t.aeroportoP,t.aeroportoA):
                    self._graph[t.aeroportoP][t.aeroportoA]["weight"]+=t.peso
                else:
                    self._graph.add_edge(t.aeroportoP,t.aeroportoA,weight=t.peso)

    def addEdgesV2(self):
        allTratte=DAO.getAllEdgesV2(self._idMapAirports)
        
        for t in allTratte:
            self._graph.add_edge(t.aeroportoP,t.aeroportoA,t.peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)
    
    def getAllNodes(self):
        nodes= list(self._graph.nodes)
        nodes.sort(key=lambda x: x.IATA_CODE)
        return nodes

    def getViciniOrdinati(self,source):
        #restituisce tutti i vicini di source ordinati per pesp dell'arco
        vicini=self._graph.neighbors(source)
        viciniT=[]
        for v in vicini:
            viciniT.append((v,self._graph[source][v]["weight"]))
        viciniT.sort(key=lambda x: x[1])
        return viciniT
    
    def hasPath(self,v0,v1):
        #restituisce true se esiste il cammino, altrimenti restituisce false
        return v1 in nx.node_connected_component(self._graph,v0)
    
    def getPath(self,v0,v1):
        #nodo chiave e riporto al nodo a cui sono arrivato
        #dictOfPredecessor=dict(nx.bfs_predecessors(self._graph, v0))
        #path=[v1]
        #while path[0]!=v0:
            #path.insert(0,dictOfPredecessor[path[0]])
        #si può usare nx.shortest_path oppure nx.dijkstra_path passando grafo,v0,v1
        path=nx.dijkstra_path(self._graph,v0,v1,weight=None)
        return path
    
    def getCamminoOttimo(self,v0,v1,t):
        self._bestCammino=[]
        self._bestScore=0
        parziale=[v0]
        self._ricorsione(parziale,v1,t)
        return self._bestCammino,self._bestScore

    def _ricorsione(self,parziale,v1,t):
        #verifico se parziale sia soluzione valida
        if parziale[-1]==v1: #potenzialmente è una soluzione
            if self._getScore(parziale)>self._bestScore:
                self._bestCammino=copy.deepcopy(parziale)
                self._bestScore=self._getScore(parziale)
        
        #verifico se ha senso continuare ad aggiungere elementi in parziale 
        #oppure esco 
        if len(parziale)==t+1:#parziale ha già raggiunto il numero masssimo di tratte
            return

        #espando parziale e rifaccio ricorsione con backtracking
        for n in self._graph.neighbors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale,v1,t)
                parziale.pop()

        def _getScore(self,parziale):
            sumPesi=0
            for i in range(0,len(parziale)-1):
                sumPesi+=self._graph[parziale[i]][parziale[i+1]]["weight"]

            return sumPesi