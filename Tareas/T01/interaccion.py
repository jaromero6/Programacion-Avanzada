import consultas as cons
from iic2233_utils import parse
from functools import reduce
import os
from collections import defaultdict
from modificaciones_archivo import comprobar_input, guardar_archivo, \
    modificar_archivo, mostrar_archivo, verificar_existencia_de_archivos


# Funciones que ejecutan las consultas -----------------------------------------


def desempaquetar_listas_de_listas(lista):
    """
    Recibe una lista de lista y retorna una lista con todos los elementos de
    cada lista desempaquetados
    :param lista:
    :return: una lista de todos los elementos desempaquetados
    """
    return [quitar_lista_a_elemento(i) for i in lista]


def quitar_lista_a_elemento(elemento):
    """
    :param elemento:
    :return: el elemento desempaquetado en caso de ser una lista
    """
    if type(elemento) == list:
        return quitar_lista_a_elemento(*elemento)
    return elemento


def obtener_consultas():
    return {
        "load_database": cons.load_database, "filter_flights":
            cons.filter_flights,
        "filter_passengers": cons.filter_passengers,
        "filter_passengers_by_age": cons.filter_passengers_by_age,
        "filter_airports_by_country": cons.filter_airports_by_country,
        "filter_airports_by_distance": cons.filter_airports_by_distance,
        "favourite_airport": cons.favourite_airport,
        "passenger_miles": cons.passenger_miles,
        "popular_airports": cons.popular_airports,
        "airport_passengers": cons.airport_passengers,
        "furthest_distance": cons.furthest_distance
    }


def obtener_llaves(consulta, diccionario):
    """
    Recibe un diccionario con posibles diccionarios anidados y un defauldict
    A este le añade las consultas con el fin de obtener las llaves de los
    diccionarios anidados
    :param consulta:
    :param diccionario:
    :return: Nada
    """
    [diccionario[k].append(v) for k, v in consulta.items()]
    [[obtener_llaves(j, diccionario) if type(j) == dict else None for j in
      i] if type(i) == tuple or type(i) == list else None for i in
            consulta.values()]


def verificar_llaves(consulta):
    """
    Verifica que las llaves esten entre las consultas que se pueden hacer
    :param consulta:
    :return: True si todas las llaves están bien, False en otro caso
    """
    diccionario_llaves = defaultdict(list)
    obtener_llaves(consulta, diccionario_llaves)
    print(diccionario_llaves)
    todo_bien = [x in obtener_consultas() for x in diccionario_llaves]
    if False in todo_bien:
        return False
    return True


def ejecuta_consulta(consulta, argumentos):
    consultas_disp = obtener_consultas()
    return consultas_disp[consulta](
        *desempaquetar_listas_de_listas(argumentos))


def buscar_consultas_anidadas(consulta, argumentos_consulta):
    """
    Recibe una consulta, ejecuta sus argumentos en caso de ser necesario y
    ejecuta esta consulta
    :param consulta:
    :param argumentos_consulta:
    :return: Consulta ejecutada
    """
    return ejecuta_consulta(
        consulta, [x if type(x) != dict else
                   [buscar_consultas_anidadas(j, x[j]) for j
                    in x] for x in argumentos_consulta]
    )


def formato_consulta(consulta):
    if type(consulta) == dict:
        menu_consultas_ejecutadas(consulta)
    else:
        [menu_consultas_ejecutadas(i) for i in consulta]


def ejecutar_consultas(consultas):
    return [(encontrar_tipo(i), {i: consultas[i]}, buscar_consultas_anidadas(
        i, consultas[i])) for i in consultas]


def encontrar_tipo(comando):
    """
    :param comando:
    :return:Tipo de funcion, G si es Generadora,D si retorna un tipo de
    estructura
    de dato
    """
    consultas_gen = ['load_database', 'filter_flights', 'filter_passengers',
                     'filter_passengers_by_age',
                     'filter_airports_by_country',
                     'filter_airports_by_distance']
    if comando in consultas_gen:
        return "G"
    return "D"


def recibir_consulta(consulta):
    print(consulta)
    if parse(consulta):
        if type(parse(consulta)) == dict:
            if verificar_llaves(parse(consulta)):
                return formato_consulta(parse(consulta))
        elif type(parse(consulta)) == list:
            print("HOLA")
            tipo_correcto = [type(i) == dict for i in parse(consulta)]
            if False in tipo_correcto:
                print("La consulta ingresada no cumple con el formato")
            todo_bien = [verificar_llaves(i) for i in parse(consulta)]
            if False not in todo_bien:
                return formato_consulta(parse(consulta))
    print("Se ha producido un error")


# Funciones que piden inputs----------------------------------------------------

def menu_de_inicio():
    print("Elija una opcion pulsando el numero asociado a esta")
    print("1- Ingresar input de forma manual")
    print("2 -Ingresar consultas mediante archivo")
    print("3 -Ver archivo output.txt")
    accion = comprobar_input(input(), ["1", "2", "3"])
    if accion == "1":
        ingresar_por_usuario()
    elif accion == "2":
        ingresar_por_archivo()
    elif accion == "3":
        if verificar_existencia_de_archivos():
            menu_de_archivo()
        else:
            print("Ver Readme para mas informacion sobre estos archivos")


def ingresar_por_usuario():
    print("-------------------------------------------------------------------")
    print("Ingrese una consulta de la forma [{nombre_consulta 1: [args]},"
          "{consulta 2 :[args]}, .... }]")
    print("show -> Muestra consultas disponibles\nPara cancelar pulse -1")
    accion = input()
    if accion == "show":
        [print(i) for i in obtener_consultas()]
    elif accion == "-1":
        print("Cancelando .....")
        return "salir"
    elif parse(accion):
            recibir_consulta(accion)
    else:
        print("Error : Comando ingresado no existe")
    return ingresar_por_usuario()


def ingresar_por_archivo(ruta=""):
    print("-------------------------------------------------------------------")
    if ruta == "":
        print("Ingresar ruta del archivo.txt que desea leer, -1 para cancelar")
        ruta = input()
    if ruta == "-1":
        return "salir"
    elif os.path.exists(ruta) and ".txt" in ruta:
        acc = mostrar_consultas_archivo([i for i in leer_archivo(ruta)])
        if acc != "salir":
            recibir_consulta(acc)
            return ingresar_por_archivo(ruta)
    else:
        print("Error : La ruta del archivo no existe")
    return ingresar_por_archivo()


def leer_archivo(ruta):
    with open(ruta, encoding="utf-8") as archivo:
        c = 1
        for i in archivo:
            yield str(c), i.strip()
            c += 1


def mostrar_consultas_archivo(lista):
    [print(i[0], "-", i[1]) for i in lista]
    print("Ingresar numero asociado a la consulta, separe por coma si es mas "
          "de una. Pulse -1 para cancelar")
    posibles = [str(i) for i in range(1, len(lista) + 1)]
    accion = verificar_lista(lista, input(), posibles)
    if accion != "salir":
            return accion
    return "salir"


def verificar_lista(lista, accion, posibles):
    if accion == "-1":
        print("Accion cancelada")
        return "salir"
    if len(accion) > 0 and parse(accion):
        todos_bien = reduce(lambda x, y: x and y, [str(x) in posibles for x in
                                               accion.split(",")])
        if todos_bien:
            return "[" + ",".join([lista[int(i)-1][1] for i in accion.split(
                ",")]) + "]"
    print("Error al ingresar acciones, volver a intentarlo")
    return verificar_lista(lista, input(), posibles)


def menu_consultas_ejecutadas(consultas):
    print("Realizando consulta, por favor espere .....")
    consulta_ejecutada = ejecutar_consultas(consultas)
    [mostrar_consulta_que_retorna_generador(i[1], i[2]) if i[0] == "G" else
         mostrar_consulta_que_retorna_estructura_de_datos(i[1], i[2])
     for i in consulta_ejecutada]


def menu_de_archivo():
    print("-------------------------------------------------------------------")
    print("Esocger una opcion a relizar con el archivo output.txt")
    print("1- Mostrar consultas\n2- Eliminar consultas")
    print("Pulse -1 para salir")
    accion = comprobar_input(input(), ["1", "2"], "-1", "Cancelar")
    if accion == "salir":
        return "salir"
    elif accion == "1":
        mostrar_archivo()
    elif accion == "2":
        modificar_archivo()
    return menu_de_archivo()


# Mostrar_resultados -----------------------------------------------------------

def mostrar_consulta_que_retorna_generador(nombre_cons, consulta):
    string_consulta = str(nombre_cons) + "\n"
    tipo_consulta = type(consulta)
    lista_generadora = list(consulta)
    print("Resultados --------------------------------------------------------")
    if len(lista_generadora) == 0:
        print("El filtro no obtuvo resultados")
    [print(i) for i in lista_generadora]
    print("¿Desea guardar este output?")
    print("1- Si\n2- No")
    accion = comprobar_input(input(), ["1"], "2",
                             "Ok, el output no sera guardado")
    if accion == "1":
        guardar_archivo(string_consulta, lista_generadora, tipo_consulta)


def mostrar_consulta_que_retorna_estructura_de_datos(nombre_cons, consulta):
    print("Resultados ------------------------------------------------------")
    if type(consulta) == dict:
        [print(i, j) for i, j in consulta.items()]
        resultado = consulta.items()
    else:
        [print(i) for i in consulta]
        resultado = consulta
    if len(resultado) == 0:
        print("La consulta no obtuvo resultados")
    print("¿Desea guardar este output?")
    print("1- Si\n2- No")
    accion = comprobar_input(input(), ["1"], "2",
                             "Ok, el output no sera guardado")
    if accion == "1":
        guardar_archivo(str(nombre_cons) + "\n", resultado, type(consulta))
