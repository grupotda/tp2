from NetworkFlow import NetworkFlow
import sys

def select_projects(network, projects):
    """
        Selecciona los proyectos y expertos que son solucion del problema y los
        imprime por consola.
        :param NetworkFlow: grafo que modela el problema
        :param list: lista de nodos que son ademas proyectos
    """
    a = network.classify_vertices()[0]
    projects = set(range(1, projects + 1))
    a.remove(0)
    print "Deben seleccionarse los proyectos:", ', '.join(str(p) for p in a.intersection(projects))
    print "Para lo cual deben contratarse expertos en las areas:", ', '.join(str(e-len(projects)) for e in a - a.intersection(projects))

def build_network(specs):
    """
        Devuelve el grafo que modela el problema de manera tal que su corte
        minimo nos devuelva la solucion.
        :param dict: especificaciones del problema
    """
    areas = specs["n"]
    projects = specs["m"]
    costs = specs["c"]
    gains = specs["g"]
    requisites = specs["r"]

    network = NetworkFlow(areas + projects + 2) # n + m + source + sink
    # Convencion:
    #   - vertice 0: fuente
    #   - vertices 1 a m: proyectos
    #   - vertices m + 1 a m + n: areas
    #   - vertice -1 (m + n + 1): sumidero

    limit = sum(costs)

    for p in range(projects):
        network.add_edge(0, p + 1, gains[p])
        for a in requisites[p]:
            network.add_edge(p + 1, projects + a, limit)

    for a in range(areas):
        network.add_edge(projects + a + 1, projects + areas + 1, costs[a])

    return network


def read_file(file):
    """
        Devuelve un diccionario con las especificaciones del problema a resolver.
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
    for i in range(m):
        line = f.readline().split(' ')
        for i in range(len(line)):
            line[i] = int(line[i])
        gains.append(line.pop(0))
        requisites.append(line)
    specs["g"] = gains
    specs["r"] = requisites

    f.close()

    return specs

if len(sys.argv) < 2 or len(sys.argv) > 2:
    print "Uso: project_selection.py <file>"
else:
    f = str(sys.argv[1])
    specs = read_file(f)
    network = build_network(specs)
    select_projects(network, specs["m"])
