import datetime
from mail_validation import validate_user_settings
from checker import check_categories, check_number
from webservices import get_places, get_nearest_stop_bus, \
    get_current_position, ask_for_a_travel, get_time


def main_function():
    print("------------------------------DCConnect "
          "--------------------------------------------------------")
    get_user_settings()
    while True:
        get_forsquare_params()


def get_user_settings():
    print("Ingresar correo")
    mail = input("$ ")
    print("Ingresar contraseña")
    password = input("$ ")
    if validate_user_settings(mail, password):
        return True
    print("Datos no validos, volver a ingreasarlos")
    return get_user_settings()


def get_forsquare_params():
    print("Ingresar una descripcion, dejar vacio si no se quiere usar este "
          "filtro")
    query = input("$ ")
    print("Ingresar alguna categoria, separar por comas si hay mas "
          "de uno, dejar vacio si no se quiere usar este filtro")
    categoryid = check_categories(input("$ "))
    if categoryid is None:
        print("Catgoria no valida se dejará como espacio vacio")
        categoryid = ""
    return select_place(get_places(query, categoryid))


def select_place(response):
    c = 0
    result = {}
    location = "-"
    categories = "-"
    print("N°     | Nombre    | Ubicación    |  Categorias")
    for i in response["response"]["venues"]:
        if "location" in i:
            if "address" in i["location"]:
                location = i["location"]["address"]
            if "categories":
                categories = list(map(lambda x: x["name"], i["categories"]))
        print(f"{c}-", i["name"], "   |   ", location, "   |   ", categories)
        result[c] = [i["name"], i["location"]["lat"], i["location"]["lng"]]
        c += 1
    while c != 0:  # Se controla que existan lugares
        print("Ingresar el numero asociado al lugar que se desea visitar")
        number = check_number(input("$ "))
        while number is None:
            print("Numero no valido, voler a intentarlo")
            number = check_number(input("$ "))
        if number <= c:
            return get_information(result[number])
        else:
            print("Numero no valido, vuelver a intentarlo")
    print("No hay lugares para visitar")


def get_information(place):
    print("Obteniendo información (Esto puede tardar un poco)    ............")
    result = ask_for_a_travel(place[1], place[2])
    print(result)
    if result is None:
        print("No hay viajes que lleguen directo al destino seleccionado")
        return
    stops_info, start_name, end_name, distance = result[0], result[1], result[
        2], result[3]
    trip = stops_info[0]["trip_id"]
    print(f"Recorrido que llega al destino: {trip}")
    print(f"Tomar la micro en {start_name}\n y bajarse en {end_name}")
    """
    Se ordenan los paraderos según su lugar en el recorrido par poder 
    calcular el tiempo de viaje 
    """
    stops_info = sorted(stops_info, key=lambda x: x["stop_sequence"])
    end = datetime.datetime.strptime(stops_info[1]["departure_time"],
                                     '%H:%M:%S')
    start = datetime.datetime.strptime(stops_info[0]["departure_time"],
                                       '%H:%M:%S')
    print(f"Duracion aproximada del viaje: {end - start}")
    start_id = stops_info[0]["stop_id"]
    print(f"La siguiente micro pasa en : {get_time(start_id)}")
    print(f"La distancia que recorre el viaje es {distance} km")
    print("Pulse una tecla para continuar")
    input("$ ")
