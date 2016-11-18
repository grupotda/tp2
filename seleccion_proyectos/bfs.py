#!/usr/bin/python
#  -*- coding: utf-8 -*-
from path import Path
from collections import deque


class Bfs(Path):
    """
    Breadth-first search
    """

    def _algorithm(self):
        q = deque()

        q.append(self.src)
        self.distances[self.src] = 0
        self.tagged[self.src] = True

        while q and not self.tagged[self.dst]:
            vertex = q.popleft()
            for edge in self.graph.adj_e(vertex):
                if not self.tagged[edge.dst]:
                    q.append(edge.dst)
                    self.edge_to[edge.dst] = edge
                    self.distances[edge.dst] = self.distances[vertex] + edge.weight
                    self.tagged[edge.dst] = True

                    if edge.dst == self.dst:
                        break
