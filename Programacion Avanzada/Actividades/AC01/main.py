from collections import namedtuple, defaultdict, deque

"""
Aquí están las estructuras de datos para guardar la información respectiva.

NO MODIFICAR.
"""

# Como se vio en la ayudantía, hay varias formas de declarar una namedtuple :)
Entrenador = namedtuple('Entrenador', 'nombre apellido')
Pokemon = namedtuple('Pokemon', ['nombre', 'tipo', 'max_solicitudes'])
Solicitud = namedtuple('Solicitud', ['id_entrenador', 'id_pokemon'])

################################################################################
"""
En esta sección debe completar las funciones para cargar los archivos al sistema.

Puedes crear funcionas auxiliar si tú quieres, ¡pero estas funciones DEBEN
retornar lo pedido en el enunciado!
"""

def cargar_entrenadores(ruta_archivo):
    resultado = {}
    with open(ruta_archivo, encoding="latin-1") as archivo:
        for linea in archivo:
            a =  linea.strip().split(";")
            tupla_entrenadores = Entrenador(a[1],a[2])
            resultado[a[0]] = tupla_entrenadores
    return resultado



def cargar_pokemones(ruta_archivo):
    resultado = {}
    with open(ruta_archivo, encoding="latin-1") as archivo:
        for linea in archivo:
            a = linea.strip().split(";")
            tupla_pokemones = Pokemon(a[1],a[2],a[3])
            resultado[a[0]] = tupla_pokemones
    return resultado



def cargar_solicitudes(ruta_archivo):
    resultado = {}
    with open(ruta_archivo, encoding="latin-1") as archivo:
        for linea in archivo:
            a = linea.strip().split(";")
            tupla_soliciitudes = Solicitud(a[0],a[1])
            if a[1] in resultado.keys():
                resultado[a[1]].append(tupla_soliciitudes)
            else:
                b = deque()
                b.append(tupla_soliciitudes)
                resultado[a[1]] = b
    return resultado


################################################################################

"""
Lógica del Sistema.
Debes completar esta función como se dice en el enunciado.
"""

def sistema(modo, entrenadores, pokemones, solicitudes):
    resul_entrenadores = defaultdict(set)
    if modo =="1":
        for i in pokemones.keys():
            maximo = int(pokemones[i].max_solicitudes)
            c = 1
            for j in solicitudes[i]:
                eo = j.id_entrenador
                if c == maximo:
                    break
                c+=1
            if eo in resul_entrenadores.keys():
                resul_entrenadores[eo].add(pokemones[i])
            else:
                a = set()
                a.add(pokemones[i])
                resul_entrenadores[eo] = a
    else:
        for i in pokemones.keys():
            maximo = int(pokemones[i].max_solicitudes)
            c = 1
            n = len(solicitudes[i]) -1
            while n>=0:
                eo = solicitudes[i][n].id_entrenador
                if c == maximo:
                    break
                c+=1
                n -= 1
            if eo in resul_entrenadores.keys():
                resul_entrenadores[eo].add(pokemones[i])
            else:
                a = set()
                a.add(pokemones[i])
                resul_entrenadores[eo] = a
    return resul_entrenadores


################################################################################
"""
Funciones de consultas, deben rellenarlos como dice en el enunciado :D.
"""

def pokemones_por_entrenador(id_entrenador, resultado_simulacion):
    lista = []
    for i in resultado_simulacion[id_entrenador]:
        lista.append(i)
    return lista

def mismos_pokemones(id_entrenador1, id_entrenador2, resultado_simulacion):

    lista = []
    for i in resultado_simulacion[id_entrenador1] & resultado_simulacion[id_entrenador2]:
        lista.append(i)
    return lista

def diferentes_pokemones(id_entrenador1, id_entrenador2, resultado_simulacion):
    a = resultado_simulacion[id_entrenador1]
    b = resultado_simulacion[id_entrenador2]
    lista = []
    for i in a - b:
        lista.append(i)
    print(lista)
    return lista


if __name__ == '__main__':

    ############################################################################
    """
    Poblando el sistema.
    Ya se hacen los llamados a las funciones, puedes imprimirlos para ver si se
    cargaron bien.
    """

    entrenadores = cargar_entrenadores('entrenadores.txt')
    pokemones = cargar_pokemones('pokemones.txt')
    solicitudes = cargar_solicitudes('solicitudes.txt')

    #print(entrenadores)
    #print(pokemones)
    #print(solicitudes)

    ################################   MENU   ##################################
    """
    Menú.
    ¡No debes cambiar nada! Simplemente nota que es un menú que pide input del
    usuario, y en el caso en que este responda con "1" ó "2", entonces se hace
    el llamado a la función. En otro caso, el programa termina.
    """

    eleccion = input('Ingrese el modo de lectura de solicitudes:\n'
                 '1: Orden de llegada\n'
                 '2: Orden Inverso de llegada\n'
                 '>\t')

    if eleccion in {"1", "2"}:
        resultados_simulacion = sistema(eleccion, entrenadores,
                                        pokemones, solicitudes)
    else:
        exit()

    ##############################   Pruebas   #################################
