from math import asin, sin, cos, sqrt, radians
from collections import namedtuple, defaultdict
import datetime
from functools import reduce

personas = namedtuple("personas", "id name clas age")
aeropuertos = namedtuple("aeropuertos", "icao tipo lat long iso_country")
vuelos = namedtuple("vuelos", "id airport_from airport_to date")
viajes = namedtuple("viajes", "flight_id passenger_id")
PATH = "data/large/"


def obtener_indices(db_type, primera_linea):
    indices_passengers = ["id", "name", "class", "age"]
    indices_airports = ["icao", "type", "lat", "long", "iso_country"]
    indices_flights = ["id", "airport_from", "airport_to", "date"]
    indices_travel = ["flight_id", "passenger_id"]
    if db_type == "passengers":
        return [primera_linea.index(x) for x in indices_passengers]
    elif db_type == "airports":
        return [primera_linea.index(x) for x in indices_airports]
    elif db_type == "flights":
        return [primera_linea.index(x) for x in indices_flights]
    return [primera_linea.index(x) for x in indices_travel]


def acomodar_base_de_datos(db_type, primera_linea, linea):
    indices = obtener_indices(db_type, primera_linea)
    if db_type == "passengers":
        return personas(*[linea[x] for x in indices])
    elif db_type == "airports":
        return aeropuertos(*[linea[x] for x in indices])
    elif db_type == "flights":
        return vuelos(*[linea[x] for x in indices])
    return viajes(*[linea[x] for x in indices])


def cambio_db_type(db_type):
    posibles = {"passengers": "passengers.csv",
                "travels": "flights-passengers.csv", "flights": "flights.csv",
                "airports": "airports.csv"}
    if db_type in posibles:
        return PATH + posibles[db_type]


def retonar_generador(iterable):
    for i in iterable:
        yield i


def cambiar_operador(x, y, symbol):
    if symbol == ">":
        return x > y
    elif symbol == "<":
        return x < y
    elif symbol == "==":
        return x == y
    return x != y


def calcular_distancia(x, y):
    return 2 * 3440 * asin(
        sqrt((sin((radians(x[0]) - radians(y[0])) / 2) ** 2) +
             (cos(radians(x[0])) * cos(radians(y[0])) *
              ((sin((radians(x[1]) - radians(y[1])) / 2)) **
               2))))


def filtrar_fechas(value, symbol, flights):
    return filter(lambda x: cambiar_operador(
        datetime.datetime.strptime(x.date, "%Y-%m-%d %H:%M:%S"),
        datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S"), symbol
    ), flights)


def comparar_fechas(start, fecha, end):
    return datetime.datetime.strptime(start, "%Y-%m-%d %H:%M:%S") <= \
           datetime.datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S") <= \
           datetime.datetime.strptime(end, "%Y-%m-%d %H:%M:%S")


def filtrar_por_destino_fecha(start, end, icao, flights):
    return set(
        map(lambda x: x.id, filter(lambda x: comparar_fechas(start, x.date,
                                                             end) and
                                                             x.airport_to ==
                                                            icao,
                                   flights)))


def filtro_por_distancia(aereo_p, icao, distance, lower):
    if not lower:
        return filter(lambda x: calcular_distancia((float(x.lat),
                                                    float(x.long)),
                                                   (float(aereo_p[icao].lat),
                                                    float(aereo_p[icao].long)))
                                > distance,
                      aereo_p.values())
    return filter(lambda x: calcular_distancia((float(x.lat),
                                             float(x.long)),
                                            (float(aereo_p[icao].lat),
                                             float(aereo_p[
                                                       icao].long))) < distance,
           aereo_p.values())


def mas_popular(lista):
    if len(lista) > 0:
        return reduce(lambda x, y: x if lista.count(x) > lista.count(y) else y,
                      lista)
    return None


def sumar(diccionario, llave, valor):
    diccionario[llave] += valor


def obtener_filtros(flights, airports, travels, avg):
    """
    :param flights:
    :param airports:
    :param travels:
    :param avg:
    :return: diccionarios con llaves que esten en los 3 generdores
    """
    if not avg:
        id_airports = {i.icao: 0 for i in airports}
    else:
        id_airports = {i.icao: [] for i in airports}
    filtro_vuelos = {x.id: x.airport_to for x in
                     filter(lambda x: x.airport_to in
                                      id_airports, flights)}
    personas_por_vuelo = defaultdict(list)
    [personas_por_vuelo[x.flight_id].append(x.passenger_id) if x.flight_id in
                                                               filtro_vuelos
     else None for x in travels]
    return id_airports, filtro_vuelos, personas_por_vuelo


def agregar_pasajeros(flights, aeropuertos_visitados, viajes_p, icao1, icao2):
    [[(aeropuertos_visitados[x.airport_from].add(j), aeropuertos_visitados[
        x.airport_to].add(j)) if (x.id in viajes_p and x.airport_to in
        (icao1, icao2) and x.airport_from in (icao1, icao2)) else
        aeropuertos_visitados[x.airport_from].add(j) if
        (x.id in viajes_p and x.airport_from in (icao1, icao2)) else
        aeropuertos_visitados[x.airport_to].add(j) if
        (x.id in viajes_p and x.airport_to in (icao1, icao2)) else None
        for j in viajes_p[x.id]] for x in flights]


def retornar_lista(lista, n):
    if len(lista) >= n:
        return lista[:n]
    return lista


def ejecutar_operacion(pasajeros, aeropuertos_vis, icao1, icao2, operation):
    if operation == "AND":
        return set(map(lambda x: (x, pasajeros[x]),
                       aeropuertos_vis[icao1] & aeropuertos_vis[icao2]))
    elif operation == "OR":
        return set(map(lambda x: (x, pasajeros[x]),
                       aeropuertos_vis[icao1] | aeropuertos_vis[icao2]))
    elif operation == "XOR":
        return set(map(lambda x: (x, pasajeros[x]),
                       aeropuertos_vis[
                           icao1].symmetric_difference(aeropuertos_vis[icao2])))
    return set(map(lambda x: (x, pasajeros[x]),
                   aeropuertos_vis[icao1] - aeropuertos_vis[icao2]))


def devolver_lista(diccionario, pasajeros, viajes_p, n):
    final = []
    orden = sorted(list(diccionario.keys()), key=lambda x: diccionario[x],
                   reverse=True)
    [[final.append((j, pasajeros[j])) if len(final) < n else None for j in
      viajes_p[i]] for i in orden]
    return final
