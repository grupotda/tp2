#!/usr/bin/python
#  -*- coding: utf-8 -*-
from flow_network import FlowNetwork


def test():
    NetworkA = FlowNetwork(6)
    edges = [(0,1,16),(0,2,13),(1,2,10),(2,1,4),(1,3,12),(2,4,14),(3,2,9),(4,3,7),(3,5,20),(4,5,4)]
    # red de flujos de: http://www.geeksforgeeks.org/ford-fulkerson-algorithm-for-maximum-flow-problem/
    src = 0
    dst = 1
    w = 2
    for edge in edges:
        NetworkA.add_edge(edge[src],edge[dst],edge[w])
    flow = NetworkA.max_flow()
    print "Flujo de la primera red calculado correctamente.. "+str(flow == 23)

    NetworkB = FlowNetwork(6)
    # ejemplo de: http://www.win.tue.nl/~nikhil/courses/2015/2WO08/07NetworkFlowI.pdf (pag 20)
    edges_b =[(0,1,10),(0,2,10),(1,2,2),(1,3,4),(1,4,8),(2,4,9),(4,3,6),(3,5,10),(4,5,10)]
    for edge in edges_b:
        NetworkB.add_edge(edge[src],edge[dst],edge[w])
    flow = NetworkB.max_flow()
    print "Flujo de la segunda red calculado correctamente.. "+str(flow == 19)
    
    NetworkC = FlowNetwork(6)
    # ejercicio 2 de Kleinberg, capitulo 7, imagen 7.26
    edges_c = [(0,1,8),(1,4,10),(4,5,8),(0,2,10),(2,5,5),(0,3,5),(3,5,10),(1,2,3),(1,3,3),(2,4,3),(3,4,3)]
    for edge in edges_c:
        NetworkC.add_edge(edge[src],edge[dst],edge[w])
    flow = NetworkC.max_flow()
    print "El flujo deberia ser 21, es", flow, ":", flow == 21

if __name__ == "__main__":
    test()
