import sys
from knapsack import max_subset
separador_instancias = '-----'
def procesar_archivo(arch):

    '''Devuelve una lista de listas, cada lista representa a cada instancia
       del problema de la mochila'''
    archivo = open(arch)
    ignorar = ["\n","-----\n"]
    instancias = []
    info_items = 5
    items_sol_optima = 4
    obtener_info = 0
    for linea in archivo:
        if linea in ignorar:
            continue
        elif linea[0] == "k": #nueva instancia del problema
            instancias.append([])
            obtener_info = 0
               
        else: #linea separada por comas o informacion de la instancia
            if obtener_info < 4: #son 4 los datos que debo leer antes de la informacion de items
                # 0:cantidad items
                # 1:capacidad
                # 2:valor optimo
                # 3:tiempo
                if obtener_info == 3: #el tiempo esta en otro formato
                    instancias[len(instancias) - 1].append(float(linea[5:]))
                else:
                    instancias[len(instancias) - 1].append(int(linea[2:]))

                obtener_info += 1
                if obtener_info == 4: #ahora debo empezar a procesar los items y los que estan en la solucion optima
                    for i in range(2):
                    # 4:lista con elementos de la solucion optima
                    # 5:items del tipo (peso, valor)        
                        instancias[len(instancias) - 1].append([]) 
                continue
            item = linea.split(",")
            
            Id = 0
            valor = 1
            peso = 2
            es_solucion = 3
            instancias[len(instancias) - 1][info_items].append((int(item[peso]),int(item[valor])))
            if int(item[es_solucion]):

                instancias[len(instancias) - 1][items_sol_optima].append(int(item[Id]) - 1)

    archivo.close()
    return instancias
def main():

    if len(sys.argv) < 2 or len(sys.argv) > 2:
        print "Uso: knapsack_tests.py <file_test.csv>"
        return
    archivo = str(sys.argv[1])
    instancias = procesar_archivo(archivo)
    
    for instancia in instancias:
        cantidad_items = instancia[0]
        capacidad_mochila = instancia[1]
        valor_a_obtener = instancia[2]
        tf = instancia[3]
        items_optimos = instancia[4]
        items = instancia[5]
        sol, items_sol, tf_sol = max_subset(items, capacidad_mochila)
        print sol
        print str(valor_a_obtener)+" valor a obtener"
        print items_sol
        print str(items_optimos)+" items a obtener (sumar 1 a cada id)"
        print str(tf_sol)+" tiempo en correr max_subset"
        print str(tf)+" tiempo que se supone obtener"
      
main()
