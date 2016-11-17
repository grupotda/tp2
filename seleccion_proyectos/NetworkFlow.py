#!/usr/bin/python
#  -*- coding: utf-8 -*-

from digraph import Digraph,Edge
from bfs import Bfs

class NetworkFlow(Digraph):
    '''Reprensenta a una red de flujos'''

    def __init__(self, v):
        """Pre: La fuente sera el primer vertice
                El sumidero sera el ultimo vertice
        """
        Digraph.__init__(self,v)
        self.source = 0
        self.sink = v - 1
        self.f = 0
        self.a = set()
        self.b = set()

    def add_edge(self, src, dst, weight=1):
        """
        Añade una arista al grafo.
        :param src: el vertice origen, debe pertenecer al grafo.
        :param dst: el vertice destino, debe pertenecer al grafo.
        :param weight: el peso asociado a la arista.
        """
        if dst >= self.V(): raise IndexError("Vertice desconocido")
        edge = ResidualEdge(src, dst, weight)
        back_edge = ResidualEdge(dst, src, weight, edge)
        self.vertices[src].append(edge)
        self.vertices[dst].append(back_edge)

    def _augment(self, path_to_sink, travel):
        min_flow = self._bottleneck(path_to_sink, travel)
        for arista in travel:
            arista.actualizar_flujo(min_flow)
        return min_flow

    def _bottleneck(self, path, travel):
        """
            Devuelve la arista de peso minimo del camino path
            :param path: objeto Path
            :param travel: aristas del camino
        """
        return min(arista.capacity() for arista in travel)

    def calc_max_flow(self):
        path_to_sink = Bfs(self, self.source, self.sink)
        travel = path_to_sink.path(self.sink)

        while travel:
            min_flow = self._augment(path_to_sink, travel)
            self.f += min_flow
            path_to_sink = Bfs(self, self.source, self.sink)
            travel = path_to_sink.path(self.sink)

    def classify_vertices(self):
        self.flow()

        self.a.add(self.source)
        bfs = Bfs(self, self.source, self.sink)
        for v in xrange(self.V()):
            if bfs.visited(v):
                self.a.add(v)
            else:
                self.b.add(v)
        return self.a, self.b

    def flow(self):
        self.calc_max_flow()
        return self.f


class ResidualEdge(Edge):

    def __init__(self, src, dst, c, asoc_edge=None):
        Edge.__init__(self, src, dst, c)
        if asoc_edge:
            self.flow = c
            self.back_edge = asoc_edge
            asoc_edge.back_edge = self
        else:
            self.flow = 0
            self.back_edge = None

    def actualizar_flujo(self, value):
        '''Actualiza el flujo que pasa por la arista'''
        self.flow += value
        self.back_edge.flow -= value

    def capacity(self):
        return self.weight - self.flow
