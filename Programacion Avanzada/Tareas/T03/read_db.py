import csv
from data_structures import List, IdList
from entities import (ElectricalGeneratingCentral,
                      LiftingStation, TransmisionSubstation,
                      DistributionSubstation, Consumer)

PATH = "bd/small/"


def get_index_of_header_element(element, header):
    index_of = 0
    for i in header:
        if i.value == element:
            return index_of
        index_of += 1


def get_pair_elements(default_order, order_line, line):
    ordered_list = List()
    for i in default_order:
        ordered_list.append(line[get_index_of_header_element(i.value,
                                                             order_line)].value)
    return ordered_list


def unpack_reader(*args):
    return List(*args)


def read_database(filename, default_order):
    file_list = List()
    with open(PATH + filename, encoding="utf-8") as file:
        header = List(*file.readline().strip().split(","))
        for i in unpack_reader(*csv.reader(file)):
            file_list.append(get_pair_elements(default_order, header,
                                               List(*i.value)))
    return file_list


def create_generating_centrals():
    centrals_list = IdList()
    for j in read_database("centrales.csv", List("id", "nombre",
                                                 "sistema_electrico",
                                                 "provincia", "comuna", "tipo",
                                                 "potencia")):
        i = j.value
        central = ElectricalGeneratingCentral(int(i[0].value), i[1].value,
                                              i[2].value, i[3].value,
                                              i[4].value, i[5].value,
                                              float(i[6].value))
        centrals_list.append(int(i[0].value), central)
    return centrals_list


def create_stations(filename, type_substation):
    station_list = IdList()
    for j in read_database(filename, List("id", "nombre", "sistema_electrico",
                                          "provincia", "comuna",
                                          "consumo_mw")):
        i = j.value
        station = type_substation(int(i[0].value), i[1].value, i[2].value,
                                  i[3].value, i[4].value, float(i[5].value))
        station_list.append(int(i[0].value), station)
    return station_list


def create_consumers():
    consumer_list = IdList()
    for j in read_database("casas.csv", List("id", "sistema_electrico",
                                             "provincia", "comuna",
                                             "consumo_kw")):
        i = j.value
        consumer = Consumer(int(i[0].value), i[1].value, i[2].value,
                            i[3].value, float(i[4].value) / 1000)
        consumer_list.append(int(i[0].value), consumer)
    return consumer_list


def make_connections(emisor_list, receptor_list, filename, default_order):
    for j in read_database(filename, default_order):
        i = j.value
        id_emisor, id_receptor, distance = (i[0].value, i[1].value, i[2].value)
        emisor_list[int(id_emisor)].value.quick_connection(receptor_list[
                                                               int(
                                                        id_receptor)].value,
                                                           float(distance))


def load_total_graph():
    centrals = create_generating_centrals()
    liftings = create_stations("elevadoras.csv", LiftingStation)
    transmisions = create_stations("transmision.csv", TransmisionSubstation)
    distributions = create_stations("distribucion.csv", DistributionSubstation)
    consumers = create_consumers()
    make_connections(centrals, liftings, "centrales_elevadoras.csv",
                     List("id_central", "id_elevadora", "distancia"))
    make_connections(liftings, transmisions, "transmision_elevadoras.csv",
                     List("id_elevadora",
                          "id_transmision",
                          "distancia"))
    make_connections(transmisions, distributions,
                     "distribucion_transmision.csv",
                     List("id_transmision",
                          "id_distribucion",
                          "distancia"))
    make_connections(distributions, consumers, "casas_distribucion.csv",
                     List("id_distribucion",
                          "id_casa", "distancia"))
    make_connections(consumers, consumers, "casas_casas.csv",
                     List("id_desde", "id_hasta", "distancia"))
    calculate_ideal_demanded_power(centrals)
    distribute_the_power(consumers)
    return List(centrals, liftings, transmisions, distributions, consumers)


def calculate_ideal_demanded_power(centrals):
    total_demanded = 0
    sing_demanded = 0
    sic_demanded = 0
    aysen_demanded = 0
    magallanes_demanded = 0
    total_generated = 0
    sing_generated = 0
    sic_generated = 0
    aysen_generated = 0
    magallanes_generated = 0
    for i in centrals:
        if i.value.electrical_system == "SING":
            sing_demanded += i.value.demanded_power
            sing_generated += min(i.value.received_power,
                                  i.value._demanded_power)
        elif i.value.electrical_system == "SIC":
            sic_demanded += i.value.demanded_power
            sic_generated += min(i.value.received_power,
                                 i.value._demanded_power)
        elif i.value.electrical_system == "AYSEN":
            aysen_demanded += i.value.demanded_power
            aysen_generated += min(i.value.received_power,
                                   i.value._demanded_power)
        else:
            magallanes_demanded += i.value.demanded_power
            magallanes_generated += min(i.value.received_power,
                                        i.value._demanded_power)
        total_generated += i.value.received_power
        total_demanded += i.value._demanded_power
    print("-------------------------------------------------------------------")
    print("Demanda neta de la red")
    print(f"SIC: {sic_demanded}")
    print(f"SING: {sing_demanded}")
    print(f"AYSEN: {aysen_demanded}")
    print(f"MAGALLANES: {magallanes_demanded}")
    print(f"Total demandado por toda la red: {total_demanded}")
    print("-------------------------------------------------------------------")
    print("Total de energia generada por la red")
    print(f"SIC: {min(sic_generated, sic_demanded)}")
    print(f"SING: {min(sing_generated, sing_demanded)}")
    print(f"AYSEN: {min(aysen_generated, aysen_generated)}")
    print(f"MAGALLANES: {min(magallanes_generated, magallanes_generated)}")
    print(f"Total generado por toda la red: "
          f"{min(total_generated, total_demanded)}")


def distribute_the_power(consumers):
    print("Distribuyendo la potencia en la red ........")
    for i in consumers:
        i.value.distribute_power()
    print("Listo.")
