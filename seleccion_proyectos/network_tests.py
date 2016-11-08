from NetworkFlow import NetworkFlow
def test():
    NetworkA = NetworkFlow(6)
    edges = [(0,1,16),(0,2,13),(1,2,10),(2,1,4),(1,3,12),(2,4,14),(3,2,9),(4,3,7),(3,5,20),(4,5,4)]
    #red de flujos de: http://www.geeksforgeeks.org/ford-fulkerson-algorithm-for-maximum-flow-problem/
    src = 0
    dst = 1
    w = 2
    for edge in edges:
        NetworkA.add_edge(edge[src],edge[dst],edge[w])
    flow = NetworkA.flow()
    print "Flujo de la primera red calculado correctamente.. "+str(flow == 23)

    NetworkB = NetworkFlow(6)
    #ejemplo de: http://www.win.tue.nl/~nikhil/courses/2015/2WO08/07NetworkFlowI.pdf (pag 20)
    edges_b =[(0,1,10),(0,2,10),(1,2,2),(1,3,4),(1,4,8),(2,4,9),(4,3,6),(3,5,10),(4,5,10)]
    for edge in edges_b:
        NetworkB.add_edge(edge[src],edge[dst],edge[w])
    flow = NetworkB.flow()
    print "Flujo de la segunda red calculado correctamente.. "+str(flow == 19)
test()
