import copy
from operator import truediv

import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._geni = []
        self._idMap = {}


    def getLocalization(self):
        return DAO.getDAOLocalization()


    def buildGraph(self, loc):
        self._graph.clear()
        self._geni = DAO.get_all_genes()
        for g in self._geni:
            self._idMap[g.GeneID] = g

        self._graph.add_nodes_from(DAO.getDAONodes(loc, self._idMap))
        self.addEdges()

    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()


    def addEdges(self):
        interazioni = DAO.get_all_interactions()
        for i in interazioni:
            if self._idMap[i.GeneID1] in self._graph.nodes() and self._idMap[i.GeneID2] in self._graph.nodes():
                cromo1 = self._idMap[i.GeneID1].Chromosome
                cromo2 = self._idMap[i.GeneID2].Chromosome
                if cromo1 != cromo2:
                    self._graph.add_edge(self._idMap[i.GeneID1], self._idMap[i.GeneID2], weight= cromo1 + cromo2)
                else:
                    self._graph.add_edge(self._idMap[i.GeneID1], self._idMap[i.GeneID2], weight=cromo1)

    def getSortedEdges(self):
        lista = []
        for u,v in self._graph.edges():
            peso = self._graph[u][v]['weight']
            lista.append((u,v,peso))

        lista.sort(key =lambda x : x[2], reverse = True)
        return lista

    def getComponenteConnessa(self):
        cc = list(nx.connected_components(self._graph))
        listaCC = []
        for c in cc:
            if len(c) >1:
                listaCC.append(c)

        listaCC.sort(key = len, reverse = True)
        return listaCC





