#!/usr/bin/python
#  -*- coding: utf-8 -*-

from digraph import Digraph, Edge
from bfs import Bfs
from math import log, pow
from itertools import chain

class NetworkFlow(Digraph):
    '''Reprensenta a una red de flujos'''

    def __init__(self, V):
        """Pre: La fuente sera el primer vertice
                El sumidero sera el ultimo vertice
        """
        Digraph.__init__(self, V)
        self.back_vertices = [[] for _ in xrange(V)]
        self.min_capacity = 1  # Scaling Parameter
        self.source = 0
        self.sink = V - 1
        self.flow = 0

    def add_edge(self, src, dst, capacity=1):
        """
        Añade una arista al grafo.
        :param src: el vertice origen, debe pertenecer al grafo.
        :param dst: el vertice destino, debe pertenecer al grafo.
        :param capacity: la capacidad de la arista.
        """
        if dst >= self.V(): raise IndexError("Vertice desconocido")
        edge = ResidualEdge(src, dst, capacity)
        back_edge = ResidualEdge(dst, src, capacity, edge)
        self.vertices[src].append(edge)
        self.back_vertices[dst].append(back_edge)

    def _restricted_adj_e(self, v):
        """ Itera sobre los aristas salientes de v restringidas a una capacidad. """
        return chain((e for e in self.vertices[v] if e.capacity() >= self.min_capacity),
                     (e for e in self.back_vertices[v] if e.capacity() >= self.min_capacity))

    def _augment(self, path):
        """ Aumenta el flujo en lo maximo posible en el camino.
            Devuelve lo aumentado.
            :param path: iterable de ResidualEdge
        """
        max_augment = self._bottleneck(path)
        for edge in path:
            edge.increase_flow(max_augment)
        return max_augment

    def _bottleneck(self, path):
        """ Devuelve la menor capacidad del camino.
            :param path: iterable de ResidualEdge
        """
        return min(edge.capacity() for edge in path)

    def _calc_max_flow(self):
        """ Basado en el Scaling Max-Flow de Kleinberg y Tardos. """
        # Defino min_capacity inicial:
        max_cap_from_source = max(edge.capacity() for edge in self.adj_e(self.source))
        if max_cap_from_source == 0: return  # nada para mejorar
        self.min_capacity = pow(2, int(log(max_cap_from_source, 2)))

        # Asigno el metodo restringido por capacidad al metodo que usa bfs
        old_adj_e_method = self.adj_e
        self.adj_e = self._restricted_adj_e

        while self.min_capacity >= 1:

            path = Bfs(self, self.source, self.sink).path(self.sink)
            while path:
                self.flow += self._augment(path)
                path = Bfs(self, self.source, self.sink).path(self.sink)

            self.min_capacity /= 2

        # Re-asigno al metodo clasico
        self.adj_e = old_adj_e_method

    def classify_vertices(self):
        self._calc_max_flow()

        # Asigno el metodo restringido por capacidad al metodo que usa bfs
        self.min_capacity = 1
        old_adj_e_method = self.adj_e
        self.adj_e = self._restricted_adj_e

        a = set()
        b = set()

        bfs = Bfs(self, self.source, self.sink)
        for v in xrange(self.V()):
            if bfs.visited(v):
                a.add(v)
            else:
                b.add(v)

        # Re-asigno al metodo clasico
        self.adj_e = old_adj_e_method

        return a, b

    def max_flow(self):
        self._calc_max_flow()
        return self.flow


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

    def increase_flow(self, value):
        """ Incrementa el flujo que pasa por la arista. """
        self.flow += value
        self.back_edge.flow -= value

    def capacity(self):
        """ Devuelve la capacidad restante (residual). """
        return self.weight - self.flow
