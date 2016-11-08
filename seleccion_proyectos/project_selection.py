from NetworkFlow import NetworkFlow

def build_graph(file):
    """
        Devuelve el grafo que modela el problema de manera tal que su corte
        minimo nos devuelva la solucion.
        :param file: nombre del archivo con las especificaciones del problema
    """
    specs = read_file(file)
    areas = specs["n"]
    projects = specs["m"]
    costs = specs["c"]
    gains = specs["g"]
    requisites = specs["r"]
    print areas, projects, costs, gains, requisites # Para ir viendo que este todo bien, sacar si me lo olvide puesto

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
            network.add_edge(p + 1, projects + a, limit) # cambiar por inf si anda

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

build_graph("example")
