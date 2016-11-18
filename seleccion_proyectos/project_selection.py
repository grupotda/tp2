#!/usr/bin/python
#  -*- coding: utf-8 -*-
from flow_network import FlowNetwork
import sys


def select_projects(network, specs):
    """ Selecciona los proyectos y expertos que son solucion del problema y los
        imprime por consola.
        :param network: FlowNetwork que modela el problema
        :param specs: especificaciones del problema
    """
    a, b = network.classify_vertices()
    a.remove(0)
    selected_projects = a.intersection(set(range(1, specs["m"] + 1)))
    selected_areas = a - selected_projects
    income_projects = sum(specs["g"][p-1] for p in selected_projects)
    cost_areas = sum(specs["c"][e-specs["m"]-1] for e in selected_areas)
    print "Deben seleccionarse los proyectos:", ', '.join(str(p) for p in selected_projects)
    print "Los cuales hacen ingresar:", income_projects
    print "Para lo cual deben contratarse expertos en las areas:", ', '.join(str(e-specs["m"]) for e in selected_areas)
    print "Los cuales cuestan:", cost_areas
    print "Dandonos un resultado total de:", income_projects - cost_areas


def build_network(specs):
    """ Devuelve el grafo que modela el problema de manera tal que su corte
        minimo nos devuelva la solucion.
        :param specs: especificaciones del problema
    """
    areas = specs["n"]
    projects = specs["m"]
    costs = specs["c"]
    gains = specs["g"]
    requisites = specs["r"]

    network = FlowNetwork(areas + projects + 2) # n + m + source + sink
    # Convencion:
    #   - vertice 0: fuente
    #   - vertices 1 a m: proyectos
    #   - vertices m + 1 a m + n: areas
    #   - vertice -1 (m + n + 1): sumidero

    limit = sum(costs) + 1

    for p in range(projects):
        network.add_edge(0, p + 1, gains[p])
        for a in requisites[p]:
            network.add_edge(p + 1, projects + a, limit)

    for a in range(areas):
        network.add_edge(projects + a + 1, projects + areas + 1, costs[a])

    return network


def read_file(file):
    """ Devuelve un diccionario con las especificaciones del problema a resolver.
        La funcion no hace chequeos. Supone que el archivo es valido.
        :param file: nombre del archivo con las especificaciones del problema
    """
    f = open(file, 'r')
    specs = {}
    n = int(f.readline())
    m = int(f.readline())
    specs["n"] = n
    specs["m"] = m

    costs = []
    for i in range(n):
        costs.append(int(f.readline()))
    specs["c"] = costs

    gains = []
    requisites = []
    for _ in range(m):
        line = [int(x) for x in f.readline().split(' ')]
        gains.append(line.pop(0))
        requisites.append(line)
    specs["g"] = gains
    specs["r"] = requisites

    f.close()

    return specs

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 2:
        print "Uso: project_selection.py <file>"
    else:
        f = str(sys.argv[1])
        specs = read_file(f)
        network = build_network(specs)
        select_projects(network, specs)
