#!/usr/bin/python
#  -*- coding: utf-8 -*-
import abc
from collections import deque


class Path(object):
    """
    Clase abstracta para definir comportamiento identico
    para los metodos de consulta de un camino.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, graph, src, dst):
        """
        :param graph: Grafo
        :param src: vertice origen
        :param dst: vertice destino
        """
        self.graph = graph
        self.src = src
        self.dst = dst

        # tagged == visited, para que no haya name-clash con el metodo
        # INVARIANTE: tagged[self.src] == True
        self.tagged = [False] * graph.V()
        # edge_to = {dstVertex: Edge(srcVertex, dstVertex, weight)}
        # INVARIANTE: edge_to.has_key(self.src) == False
        self.edge_to = {}
        # distances = {vertex: sum(edge.weight for edge in path)}
        # INVARIANTE: distances[self.src] == 0
        self.distances = {}

        self._algorithm()

    @abc.abstractmethod
    def _algorithm(self):
        """
        Procedimiento que calcula el camino especificado en el constructor
        """
        return

    def visited(self, vertex):
        """
        Indica si se visito un vertice en el recorrido
        :param vertex: vertice
        :return: True / False
        """
        return self.tagged[vertex]

    def distance(self, vertex):
        """
        Devuelve la distancia a un vertice desde el origen.
        Si no fue visitado, devuelve infinito.
        :param vertex: vertice
        :return: la distancia
        """
        if not self.visited(vertex):
            return float("inf")
        else:
            return self.distances[vertex]

    def path(self, vertex):
        """
        Devuele una lista de aristas que comprenden el camino de
        origen hasta el vertice pasado por parametro.
        :param vertex: vertice destino
        :return: [Edge_0, ..., Edge_N], donde:
        Edge_0.src = vertice origen
        Edge_N.dst = vertice parametro.
        None si no habia camino, [] si vertex era el origen.
        """
        if not self.visited(vertex):
            return None

        path = deque()
        # Recorremos el camino de destino a origen
        # Si me pidieron origen, no entra aca y devuelve []
        while self.edge_to.has_key(vertex):
            edge = self.edge_to[vertex]
            path.appendleft(edge)
            vertex = edge.src
        return list(path)

    def vertex_path(self, vertex):
        """
        Devuele una lista de vertices que comprenden el camino de
        origen hasta el vertice pasado por parametro.
        :param vertex: vertice destino
        :return: [Vertex_0, ..., Vertex_N], donde:
        Vertex_0 = vertice origen
        Vertex_N = vertice parametro.
        None si no habia camino, [] si vertex era el origen.
        """
        if not self.visited(vertex):
            return None
        if vertex == self.src:
            return []

        path = deque()
        # Recorremos el camino de destino a origen
        while self.edge_to.has_key(vertex):
            edge = self.edge_to[vertex]
            path.appendleft(edge.dst)
            vertex = edge.src
        path.appendleft(vertex) # el origen
        return list(path)
