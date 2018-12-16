from collections import defaultdict
import funciones_aux as aux

PATH = aux.PATH


def load_database(db_type):
    with open(aux.cambio_db_type(db_type.lower()), encoding="utf-8-sig") as \
            archivo:
        linea = archivo.readline().strip().split(",")
        for i in archivo:
            yield aux.acomodar_base_de_datos(
                db_type.lower(), linea,
                i.strip().split(",")
            )


def filter_flights(flights, airports, attr, symbol, value):
    if attr == "date":
        return aux.retonar_generador(aux.filtrar_fechas(value, symbol, flights))
    elif attr == "distance":
        aeropuerto = {x.icao: (float(x.lat), float(x.long)) for x in airports}
        return aux.retonar_generador(filter(
            lambda x: aux.cambiar_operador(
                aux.calcular_distancia(aeropuerto[x.airport_from],
                                       aeropuerto[x.airport_to]),
                value, symbol), filter(lambda x: x.airport_to in aeropuerto and
                                                 x.airport_from in aeropuerto,
                                       flights))
        )


def filter_passengers(passengers, flights, travels, icao, start, end):
    filtro_fecha_des = aux.filtrar_por_destino_fecha(start, end, icao, flights)
    filtro_viajes = set(map(lambda x: x.passenger_id,
                            filter(lambda x: x.flight_id in filtro_fecha_des,
                                   travels)))
    return aux.retonar_generador(filter(lambda x: x.id in filtro_viajes,
                                        passengers))


def filter_passengers_by_age(passengers, age, lower=True):
    if lower:
        return filter(lambda x: int(x.age) < age, passengers)
    return aux.retonar_generador(filter(lambda x: int(x.age) >= age,
                                        passengers))


def filter_airports_by_country(airports, iso):
    return aux.retonar_generador(filter(lambda x: x.iso_country == iso,
                                        airports))


def filter_airports_by_distance(airports, icao, distance, lower=False):
    aereo_p = {x.icao: x for x in airports}
    if icao not in aereo_p:
        return (i for i in [])
    return aux.retonar_generador(aux.filtro_por_distancia(aereo_p, icao,
                                                          distance, lower))


def favourite_airport(passengers, flights, travels):
    pasajeros = {x.id: (x.name, []) for x in passengers}
    vuelos_p = {x.id: x.airport_to for x in flights}
    [
     pasajeros[i.passenger_id][1].append(vuelos_p[i.flight_id]) for i
     in filter(lambda x: x.flight_id in vuelos_p
               and x.passenger_id in pasajeros, travels)
    ]
    return {(x, pasajeros[x][0]): aux.mas_popular(pasajeros[x][1]) for x in
            pasajeros}


def passenger_miles(passengers, airports, flights, travels):
    pasajeros = {x.id: (x.name, []) for x in passengers}
    aeropuertos = {x.icao: (float(x.lat), float(x.long)) for x in airports}
    vuelos_p = {x.id: aux.calcular_distancia(aeropuertos[x.airport_from],
                aeropuertos[x.airport_to]) for x in filter(lambda x:
                x.airport_from in aeropuertos and x.airport_to in
                                                  aeropuertos, flights)}
    [pasajeros[i.passenger_id][1].append(vuelos_p[i.flight_id]) if
     i.passenger_id in pasajeros and i.flight_id in vuelos_p else None for i in
     travels]
    return {(x,pasajeros[x][0]): sum(pasajeros[x][1]) for x in pasajeros}


def popular_airports(flights, airports, travels, topn, avg=False):
    filtros = aux.obtener_filtros(flights, airports, travels, avg)
    if not avg:
        [aux.sumar(filtros[0], filtros[1][x], len(filtros[2][x])) for x in
         filtros[2]]
        return sorted(list(filtros[0].keys()), key=lambda x: filtros[0][x],
                      reverse=True)[:topn]
    else:
        [filtros[0][filtros[1][x]].append(len(filtros[2][x])) for x in
         filtros[2]]
        return aux.retornar_lista(sorted(list(filter(lambda x: filtros[0][x] !=
                [], filtros[0].keys())), key=lambda x: sum(filtros[0][x]) / (
                len(filtros[0][x])), reverse=True), topn)


def airport_passengers(passengers, flights, travels, icao1, icao2, operation):
    pasajeros = {x.id: x.name for x in passengers}
    viajes_p = defaultdict(list)
    [viajes_p[x.flight_id].append(x.passenger_id) if x.passenger_id in
                                                     pasajeros else None for x
     in travels]
    aeropuertos_visitados = {icao1: set(), icao2: set()}
    aux.agregar_pasajeros(flights, aeropuertos_visitados, viajes_p, icao1,
                          icao2)
    return aux.ejecutar_operacion(pasajeros, aeropuertos_visitados, icao1,
                                  icao2,
                                  operation)


def furthest_distance(passengers, airports, flights, travels, icao, n=3):
    pasajeros = {x.id: x.name for x in passengers}
    viajes_p = defaultdict(list)
    [viajes_p[x.flight_id].append(x.passenger_id) if x.passenger_id in pasajeros
     else None for x in travels]
    aeropuertos = {x.icao: (float(x.lat), float(x.long)) for x in airports}
    if icao not in aeropuertos:
        return []
    distancia_vuelos = {x.id: aux.calcular_distancia(aeropuertos[x.airport_to],
                                                     aeropuertos[icao]) for x in
                        filter(lambda x: x.airport_from == icao and
                               x.airport_to in aeropuertos and x.id
                               in viajes_p, flights)}
    return aux.devolver_lista(distancia_vuelos, pasajeros, viajes_p, n)
