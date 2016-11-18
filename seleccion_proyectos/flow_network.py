#!/usr/bin/python
#  -*- coding: utf-8 -*-
from digraph import Digraph, Edge
from bfs import Bfs
from math import log, pow
from itertools import chain


class FlowNetwork(Digraph):
    """ Representa a una red de flujo.
        Se puede utilizar como un digrafo normal.
        Condiciones de la red:
            - El primer vertice (0) sera la fuente (s)
            - El ultimo vertice (V-1) sera el sumidero (t)
    """

    def __init__(self, V):
        """ Construye una red sin aristas de V vertices. """
        Digraph.__init__(self, V)
        self.back_vertices = [[] for _ in xrange(V)]
        self.min_capacity = 1  # Scaling Parameter (delta)
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
        edge = FlowEdge(src, dst, capacity)
        back_edge = FlowEdge(dst, src, capacity, edge)
        self.vertices[src].append(edge)
        self.back_vertices[dst].append(back_edge)

    def _restricted_adj_e(self, v):
        """ Itera sobre los aristas salientes de v restringidas a una capacidad. """
        return chain((e for e in self.vertices[v] if e.capacity() >= self.min_capacity),
                     (e for e in self.back_vertices[v] if e.capacity() >= self.min_capacity))

    def _augment(self, path):
        """ Aumenta el flujo en lo maximo posible en el camino.
            Devuelve lo aumentado.
            :param path: iterable de FlowEdge
        """
        max_augment = self._bottleneck(path)
        for edge in path:
            edge.increase_flow(max_augment)
        return max_augment

    def _bottleneck(self, path):
        """ Devuelve la menor capacidad del camino.
            :param path: iterable de FlowEdge
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
        """ Calcula el corte minimo s-t.
            Devuelve 2 sets de vertices correspondientes a cada parte.
        """
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
        """ Calcula y devuelve el flujo maximo de la red. """
        self._calc_max_flow()
        return self.flow


class FlowEdge(Edge):
    """ Arista que trabaja con flujo.
        El peso de la arista es su capacidad total.
        Condicion: Crear siempre de a pares para generar grafo residual.
    """

    def __init__(self, src, dst, cap, asoc_edge=None):
        """ Se construye una arista con flujo inicial 0.
            Si se especifica la arista, se asocia con la recien construida.
            La recien construida se considera la "residual".
            Cond: src y dst deben ser los invertidos de la arista asociada.
        """
        Edge.__init__(self, src, dst, cap)
        if asoc_edge:
            self.flow = cap
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
