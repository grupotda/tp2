import time
def items_obtenidos(items, peso_max, sol_opt):

    w = 0
    obtenidos = list() #contiene los indices de los items obtenidos
    j = peso_max
    for i in xrange(len(items), 0, -1):
        if sol_opt[i][j] != sol_opt[i - 1][j]:
            obtenidos.append(i - 1)
            j -= items[i - 1][w]
    return obtenidos[::-1]

def max_subset(items, weight_limit):
    """Devuelve: valor_optimo, [items_optimos], tiempo_ejecucion (sin contar reconstruccion que es o(n)"""
    w = 0
    v = 1
    matriz = []
    ti = time.clock()
    for item in range(len(items) + 1):
        matriz.append([0]*(weight_limit + 1))

    for item in range(1, len(items) + 1):
        for weight in range(1, weight_limit + 1):
            if weight >= items[item - 1][w]:
                matriz[item][weight] = max(matriz[item - 1][weight],items[item - 1][v] + matriz[item - 1][weight - items[item - 1][w]])
            else:
                matriz[item][weight] = matriz[item - 1][weight]
    tf = time.clock() - ti
    path = items_obtenidos(items, weight_limit, matriz)
    return matriz[len(items)][weight_limit],path,tf
    
