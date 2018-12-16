from settings import FOURSQUARE_USERNAME, FOURSQUARE_PASSWORD, \
    IPSTACK_SECRET_KEY
import requests
from math import asin, sin, cos, radians, sqrt


def get_places(query="", category=""):
    """
    Realiza la consulta a foursquare para obtener los lugares acorde a los
    parametros que recibe la api
    """
    url = 'https://api.foursquare.com/v2/venues/search'
    params = dict(
        client_id=FOURSQUARE_USERNAME,
        client_secret=FOURSQUARE_PASSWORD,
        intent='browse',
        v='20180323',
        ll="-33.4372,-70.6506",
        radius=30000,
        limit=300
    )
    if query != "":
        params["query"] = query
    if category != "":
        params["categoryId"] = category
    resp = requests.get(url=url, params=params)
    return resp.json()


def get_category_names(category, category_names):
    category_names[category["name"]] = category["id"]
    category_names[category["shortName"]] = category["id"]
    category_names[category["pluralName"]] = category["id"]
    for i in category["categories"]:
        get_category_names(i, category_names)  # Se buscan todas


def get_categories():
    resp = requests.get(url=f"https://api.foursquare.com/v2/venues/categories",
                        params=dict(
                            client_id=FOURSQUARE_USERNAME,
                            client_secret=FOURSQUARE_PASSWORD,
                            v='20180323')).json()["response"]["categories"]
    category_names = {}
    for i in resp:
        get_category_names(i, category_names)
    return category_names


def get_nearest_stop_bus(lat, long, distance=False):
    """
    Busca los paraderos activos y retorna el mas cercano
    """
    resp = requests.get(
        f"https://api.scltrans.it/v1/stops?limit=15&center_lon"
        f"={long}&center_lat={lat}&is_active="
        f"{1}").json()
    if resp["results"]:
        if not distance:
            return resp["results"]  # Retorna todos
        else:
            return list(filter(lambda x: calculate_distance(lat, long,
                                                            float(
                                                                x["stop_lat"]),
                                                            float(
                                                                x["stop_lon"]))
                                         <= 10,
                               resp["results"]))  # Retorna los que estén a
            # no más de 10 km


def get_routes_of_bus_parade(stop_bus):
    """
    Retorna un set con los id de de los viajes que pasan por ese paradero
    """
    resp = requests.get(f"https://api.scltrans.it/v3/stops/"
                        f"{stop_bus}/stop_routes").json()
    return set(map(lambda x: x["route"]["route_id"], resp["results"]))


def get_current_position():
    resp = requests.get(f"http://api.ipstack.com/check?access_key="
                        f"{IPSTACK_SECRET_KEY}").json()
    return resp["latitude"], resp["longitude"]


def ask_for_a_travel(lat, long):
    nearest_stops = get_nearest_stop_bus(lat, long)  # Lista de paraderos
    # cercanos al destino
    own_lat, own_long = get_current_position()  # Se obtiene la posicion actual
    own_near_bus_stops = get_nearest_stop_bus(own_lat, own_long, True)
    trip_informaion = get_useful_stop_bus(own_near_bus_stops, nearest_stops)
    if trip_informaion is not None:
        return trip_informaion[0], trip_informaion[1], trip_informaion[2], \
               calculate_distance(own_lat, own_long, lat, long)
    return None


def get_useful_stop_bus(stops, destiny_stops):
    """Recibe una lista de paraderos, retorna el primero que contenga viajes
    que lleguen al destino final. En terminos simples lo que se hace es ver
    si por uno de los paraderos más cercanos al usuario llega al más cercano
    del destino, si ninguno llega entonces se hace lo mismo pero con el
    segundo paradero más cecano al destino y así sucesivamente hasta
    encontrar uno o bien no encontrar y retornar None lo que indica que no
    hay viajes directos desde donde se está al destino
     """
    for i in destiny_stops:
        dest_stops = get_routes_of_bus_parade(i["stop_id"])
        for j in stops:
            stop_trips = get_routes_of_bus_parade(j["stop_id"])
            utils = stop_trips & dest_stops
            if len(utils):
                result = search_for_a_route(utils, j["stop_id"], i["stop_id"])
                if result is not None:
                    start_name = j["stop_name"]
                    end_name = i["stop_name"]
                    return result, start_name, end_name
    return None


def search_for_a_route(useful_routes, start_id, end_id):
    """
    Busca un viaje que pase primero por  el paradero de inicio y luego por el
    del final, busca en ambas rutas ida y vuelta
    """
    for i in useful_routes:
        resp = requests.get(f"https://api.scltrans.it/v2/routes/"
                            f"{i}/directions/0").json()
        info = []
        if resp["results"]["is_active"]:
            for j in resp["results"]["stop_times"]:
                if j["stop_id"] == start_id or j["stop_id"] == end_id:
                    info.append(j)
                if len(info) == 2:
                    if [info[0]["stop_id"], info[1]["stop_id"]] == [start_id,
                                                                    end_id]:  #
                        # Se comprueba que se cumpla el orden requerido
                        return info
                    else:
                        break
        resp = requests.get(f"https://api.scltrans.it/v2/routes/"
                            f"{i}/directions/1").json()
        if resp["results"]["is_active"]:
            for j in resp["results"]["stop_times"]:
                if j["stop_id"] == start_id or j["stop_id"] == end_id:
                    info.append(j)
                if len(info) == 2:
                    if [info[0]["stop_id"], info[1]["stop_id"]] == [start_id,
                                                                    end_id]:  #
                        # Se comprueba que se cumpla el orden requerido
                        return info
                    else:
                        break


def get_time(id_stop):
    resp = {"title": "smsbus webservice timeout"}
    while resp == {"title": "smsbus webservice timeout"}:
        resp = requests.get(
            f"https://api.scltrans.it/v2/stops/{id_stop}/next_arrivals").json()
    return resp["results"][0]["arrival_estimation"]


def calculate_distance(lat_start, long_start, lat_end, long_end):
    return 6371 * asin(
        sqrt((sin((radians(lat_end) - radians(lat_start)) / 2) ** 2) +
             (cos(radians(lat_start)) * cos(radians(lat_end)) *
              ((sin((radians(long_end) - radians(long_start)) / 2)) **
               2))))
