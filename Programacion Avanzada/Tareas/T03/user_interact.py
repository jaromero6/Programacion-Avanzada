from exceptions import InvalidQuery, ElectricalOverload, ForbbidenAction
from read_db import load_total_graph
from data_structures import List, IdList
from queries import (total_energy_consumed_by_commune,
                     client_with_the_highest_consumption,
                     client_with_the_less_consumption,
                     drained_power_in_transmision, consumption)
import modification_system as mod
from entities import (ElectricalGeneratingCentral,
                      LiftingStation, TransmisionSubstation,
                      DistributionSubstation, Consumer)
from math import inf


def load_function():
    print("Cargando datos y generando grafo ............................")
    return load_total_graph()


def check_input(user_input, possible_actions):
    if user_input in possible_actions:
        return True
    else:
        raise InvalidQuery("La accion ingresada no existe")


def decide_action(message, correct_input_list):
    print(message)
    try:
        action = input()
        check_input(action, correct_input_list)
    except InvalidQuery as err:
        print(f"{err}")
        return decide_action(message, correct_input_list)
    else:
        return action


def main_menu(centrals, liftings, transmisions, distributions, consumers):
    action = decide_action("Pulse 1 para realizar un consulta, 2 para "
                           "modificar la red, 0 para salir", List("0", "1",
                                                                  "2"))
    if action == "0":
        exit()
    elif action == "1":
        decide_querie(centrals, liftings, transmisions, distributions,
                      consumers)
    else:
        decide_system_modification(centrals, liftings, transmisions,
                                   distributions, consumers)


def show_queries():
    print("-----------------------------------------------------------------")
    print("Pulse el numero asociado a cada consulta")
    print("0) Volver atrás.")
    print("1) Energía total consumida por comuna.")
    print("2) Cliente con el mayor consumo por comuna.")
    print("3) Cliente con el menor consumo por comuna.")
    print("4) Energía perdida en transmisión. ")
    print("5) Consumo de una subsestación. ")
    functions_list = IdList()
    functions_list.append(1, total_energy_consumed_by_commune)
    functions_list.append(2, client_with_the_highest_consumption)
    functions_list.append(3, client_with_the_less_consumption)
    functions_list.append(4, drained_power_in_transmision)
    functions_list.append(5, consumption)
    return functions_list


def get_commune_name():
    print("Ingrese nombre de la comuna por la que desea consultar")
    return input()


def get_numeric_id():
    print("Ingrese id:")
    id_ = input()
    if not id_.isnumeric():
        print("El id debe ser un numero")
        return get_numeric_id()
    return int(id_)


def decide_querie(centrals, liftings, transmision, distributions, consumers):
    list_functions = show_queries()
    action = decide_action("Seleccione la consulta deseada", List("0", "1",
                                                                  "2", "3", "4",
                                                                  "5"))
    arguments_funtions = List(distributions, consumers, consumers)
    if int(action) == 0:
        return main_menu(centrals, liftings, transmision, distributions,
                         consumers)
    elif action == "1":
        argument = get_commune_name()
        get_querie_result(list_functions[int(action)].value, argument,
                          consumers,
                          centrals, arguments_funtions[int(action) - 1].value)
    elif int(action) in List(2, 3, 4):
        if int(action) == 4:
            argument = get_numeric_id()
        else:
            argument = select_electrical_system()
        get_querie_result(list_functions[int(action)].value, argument, None,
                          None, consumers)
    else:
        argument = get_numeric_id()
        get_querie_result(list_functions[5].value, argument, None, None,
                          distributions)
    return decide_querie(centrals, liftings, transmision, distributions,
                         consumers)


def get_querie_result(function_, argument, consumers,
                      centrals, list_of_entities=None):
    print("El resultado de la consulta es: ..............")
    function_(list_of_entities, argument, consumers, centrals)
    print("Pulse una tecla para volver atrás")
    input()


def show_modification_options():
    print("0) Volver atrás")
    print("1) Agregar conexion")
    print("2) Remover conexion")
    print("3) Añadir nodo")
    print("4) Remover un nodo")


def get_instance_to_modify(centrals, liftings, transmisions, distributions,
                           consumers):
    list_of_instances = List(centrals, liftings, transmisions, distributions,
                             consumers)
    print("Seleccione la instancia deseada, 0 para cancelar")
    print("0) Cancelar")
    print("1) Centrales")
    print("2) Elevadoras")
    print("3) Transmisiones")
    print("4) Distribuciones")
    print("5) Casas")
    action = decide_action("Seleccione:", List("0", "1", "2", "3", "4", "5"))
    if action == "0":
        return "0"
    return list_of_instances[int(action) - 1].value


def decide_system_modification(centrals, liftings, transmisions,
                               distributions, consumers):
    list_of_modifications = List(add_user_connection, remove_user_connection,
                                 user_add_new_node, user_remove_node)
    show_modification_options()
    action = decide_action("Pulse el numero asociado a la acción a "
                           "realizar", List("0", "1", "2", "3", "4"))
    if action == "0":
        return main_menu(centrals, liftings, transmisions,
                         distributions,
                         consumers)
    list_of_modifications[int(action) - 1].value(centrals, liftings,
                                                 transmisions, distributions,
                                                 consumers)
    return decide_system_modification(centrals, liftings, transmisions,
                                      distributions, consumers)


def get_entity_by_id(list_of_entities):
    print("Ingrese el id de la entidad")
    action = input()
    if not action.isnumeric():
        raise InvalidQuery("Id ingresado no es valido")
    entity_selected = list_of_entities[int(action)]
    if entity_selected is None:
        raise InvalidQuery("Entidad inexistente con el id ingresado")
    return entity_selected.value


def get_entity(list_of_entities):
    try:
        entity_selected = get_entity_by_id(list_of_entities)
        return entity_selected
    except InvalidQuery as err:
        print(f"{err}")
        return get_entity(list_of_entities)


def get_distance_number():
    distance = input()
    try:
        if float(distance) > 0:
            return float(distance)
    except:
        raise InvalidQuery("Distancia ingresada no valida")


def get_distance():
    try:
        distance = get_distance_number()
        return distance
    except InvalidQuery as err:
        print(f"{err}")
        return get_distance()


def ask_for_permanent_change():
    print("Es factible aplicar los cambios")
    print("¿Desea aplicar los cambios de forma permanente? Pulse 1 para si, "
          "2 no")
    result = decide_action("Seleccione", List("1", "2"))
    if result == "1":
        return True
    return False


def add_user_connection(centrals, liftings, transmisions, distributions,
                        consumers):
    print("AÑADIR CONEXIÓN ---------------------------------------------------")
    system_copy = mod.get_copy_of_system(centrals, liftings, transmisions,
                                         distributions, consumers)
    centrals_copy = system_copy[0].value
    liftings_copy = system_copy[1].value
    transmisions_copy = system_copy[2].value
    distributions_copy = system_copy[3].value
    consumers_copy = system_copy[4].value
    print("Seleccione el tipo de instancia donde parte la conexion")
    from_instances = get_instance_to_modify(centrals_copy, liftings_copy,
                                            transmisions_copy,
                                            distributions_copy, consumers_copy)
    if type(from_instances) == str:
        return decide_system_modification(centrals, liftings, transmisions,
                                          distributions, consumers)
    print("Seleccione el tipo de instancia donde termina la conexion")
    to_instances = get_instance_to_modify(centrals_copy, liftings_copy,
                                          transmisions_copy,
                                          distributions_copy, consumers_copy)
    if type(to_instances) == str:
        return decide_system_modification(centrals, liftings, transmisions,
                                          distributions, consumers)
    print("Seleccione el id desde donde parte la conexion")
    from_ = get_entity(from_instances)
    print("Seleccion el id donde termina la conexion")
    to = get_entity(to_instances)
    print("Ingrese distancia de la conexión")
    distance = get_distance()
    result = mod.add_connection(from_, to, distance, centrals_copy,
                                liftings_copy, transmisions_copy,
                                distributions_copy, consumers_copy)
    if result:
        if ask_for_permanent_change():
            return add_user_connection(centrals_copy, liftings_copy,
                                       transmisions_copy, distributions_copy,
                                       consumers_copy)
    return add_user_connection(centrals, liftings, transmisions,
                               distributions, consumers)


def remove_user_connection(centrals, liftings, transmisions, distributions,
                           consumers):
    print("REMOVER CONEXIÓN ------------------------------------------------")
    system_copy = mod.get_copy_of_system(centrals, liftings, transmisions,
                                         distributions, consumers)
    centrals_copy = system_copy[0].value
    liftings_copy = system_copy[1].value
    transmisions_copy = system_copy[2].value
    distributions_copy = system_copy[3].value
    consumers_copy = system_copy[4].value
    print("Seleccione el tipo de instancia donde parte la conexion")
    from_instances = get_instance_to_modify(centrals_copy, liftings_copy,
                                            transmisions_copy,
                                            distributions_copy, consumers_copy)
    print("Seleccione el tipo de instancia donde termina la conexion")
    to_instances = get_instance_to_modify(centrals_copy, liftings_copy,
                                          transmisions_copy,
                                          distributions_copy, consumers_copy)
    print("Seleccione el id desde donde parte la conexion")
    from_ = get_entity(from_instances)
    print("Seleccion el id donde termina la conexion")
    to = get_entity(to_instances)
    result = mod.remove_connection(from_, to, centrals_copy, liftings_copy,
                                   transmisions_copy, distributions_copy,
                                   consumers_copy)
    if result:
        if ask_for_permanent_change():
            return remove_user_connection(centrals_copy, liftings_copy,
                                          transmisions_copy, distributions_copy,
                                          consumers_copy)
    return remove_user_connection(centrals, liftings, transmisions,
                                  distributions, consumers)


def select_type():
    print("Seleccione la instancia, 0 para cancelar")
    print("0) Cancelar")
    print("1) Central Generadora de energia")
    print("2) Central Elevadora")
    print("3) Subestación de Transmisión")
    print("4) Subestación de Distribución")
    print("5) Casas")
    action = decide_action("Seleccione", List("0", "1", "2", "3", "4", "5"))
    if action == "0":
        return action
    return int(action) - 1


def get_id(list_of_entities):
    print("Ingrese id")
    id_ = input()
    if not id_.isnumeric():
        print("El id no debe ser un número")
        return get_id(list_of_entities)
    if int(id_) in list_of_entities:
        print("El id ingresado ya existe")
        return get_id(list_of_entities)
    if int(id_) < 0:
        print("El id debe ser un numero positivo")
        return get_id(list_of_entities)
    return int(id_)


def select_electrical_system():
    print("Seleccione un sistema")
    print("1) SIC")
    print("2) SING")
    print("3) AYSEN")
    print("4) MAGALLANES")
    systems = List("SIC", "SING", "AYSEN", "MAGALLANES")
    action = decide_action("Seleccione", List("1", "2", "3", "4"))
    return systems[int(action) - 1].value


def select_type_energy():
    print("Seleccione el tipo de energia")
    print("1) Solar")
    print("2) Termoeléctrica")
    print("3) Biomasa")
    list_of_types = List("Solar", "Termoelectrica", "Biomasa")
    return list_of_types[int(decide_action("Seleccione:", List("1", "2",
                                                               "3"))) - 1].value


def select_quantity_of_energy(min_=0, max_=inf):
    print("Ingrese la cantidad de energia en  MW")
    power = input()
    try:
        power = int(power)
        if not min_ < power < max_:
            print("Error: La potencia no está dentro del rango esperdo")
            return select_quantity_of_energy(min_, max_)
        return power
    except:
        print("Error: La potencia debe ser un numero ENTERO")
        return select_quantity_of_energy(min_, max_)


def create_new_central(list_of_centrals):
    print("Ingrese atributos de la nueva central")
    id_new_central = get_id(list_of_centrals)
    print("Ingrese nombre")
    name = input()
    electrical_system = select_electrical_system()
    print("Ingrese comuna")
    commune = input()
    print("Ingrese provincia")
    province = input()
    energy_type = select_type_energy()
    power = select_quantity_of_energy(19, 201)
    return ElectricalGeneratingCentral(id_new_central, name,
                                       electrical_system, province, commune,
                                       energy_type, power)


def create_substation(list_of_substation, substation):
    print("Ingrese atributos de la nueva subsestacion")
    id_new_central = get_id(list_of_substation)
    print("Ingrese nombre")
    name = input()
    electrical_system = select_electrical_system()
    print("Ingrese comuna")
    commune = input()
    print("Ingrese provincia")
    province = input()
    power = select_quantity_of_energy()
    return substation(id_new_central, name, electrical_system, province,
                      commune, power)


def create_consumer(list_of_consumers):
    print("Ingrese atributos de la nueva casa")
    id_new_central = get_id(list_of_consumers)
    electrical_system = select_electrical_system()
    print("Ingrese comuna")
    commune = input()
    print("Ingrese provincia")
    province = input()
    power = select_quantity_of_energy(0, 31)
    return Consumer(id_new_central, electrical_system, province,
                    commune, power)


def create_node(node_type, centrals, liftings, transmisions, distributions,
                consumers):
    if node_type == ElectricalGeneratingCentral:
        return create_new_central(centrals)
    elif node_type != Consumer:
        list_type = List(LiftingStation, TransmisionSubstation,
                         DistributionSubstation)
        list_entities = List(liftings, transmisions, distributions)
        c = 0
        for i in list_type:
            if i.value == node_type:
                break
            c += 1
        return create_substation(list_entities[c].value, node_type)
    else:
        return create_consumer(consumers)


def user_add_new_node(centrals, liftings, transmisions, distributions,
                      consumers):
    print("AÑADIR NODO  ------------------------------------------------")
    node_type = select_type()
    if node_type == "0":
        return decide_system_modification(centrals, liftings, transmisions,
                                          distributions, consumers)
    system_copy = mod.get_copy_of_system(centrals, liftings, transmisions,
                                         distributions, consumers)
    centrals_copy = system_copy[0].value
    liftings_copy = system_copy[1].value
    transmisions_copy = system_copy[2].value
    distributions_copy = system_copy[3].value
    consumers_copy = system_copy[4].value
    list_types = List(ElectricalGeneratingCentral, LiftingStation,
                      TransmisionSubstation, DistributionSubstation, Consumer)
    new_node = create_node(list_types[int(node_type)].value, centrals_copy,
                           liftings_copy, transmisions_copy, distributions_copy,
                           consumers_copy)
    instances = List(centrals_copy, liftings_copy, transmisions_copy,
                     distributions_copy, consumers_copy)
    result = mod.add_node(new_node, instances[int(node_type)].value,
                          centrals_copy, liftings_copy, transmisions_copy,
                          distributions_copy, consumers_copy)
    if result:
        if ask_for_permanent_change():
            print("Cambios aplicados ....................")
            return user_add_new_node(centrals_copy, liftings_copy,
                                     transmisions_copy, distributions_copy,
                                     consumers_copy)
    return user_add_new_node(centrals, liftings, transmisions,
                             distributions, consumers)


def user_remove_node(centrals, liftings, transmisions, distributions,
                     consumers):
    print("REMOVER NODO -------------------------------------------------")
    system_copy = mod.get_copy_of_system(centrals, liftings, transmisions,
                                         distributions, consumers)
    centrals_copy = system_copy[0].value
    liftings_copy = system_copy[1].value
    transmisions_copy = system_copy[2].value
    distributions_copy = system_copy[3].value
    consumers_copy = system_copy[4].value
    instances = List(centrals_copy, liftings_copy, transmisions_copy,
                     distributions_copy, consumers_copy)
    node_type = select_type()
    if node_type == "0":
        return decide_system_modification(centrals, liftings, transmisions,
                                          distributions, consumers)
    print("Seleccione la instancia a borrar")
    removed_node = get_entity(instances[int(node_type)].value)
    result = mod.remove_node(removed_node, centrals_copy,
                             liftings_copy, transmisions_copy,
                             distributions_copy, consumers_copy)
    if result:
        if ask_for_permanent_change():
            return remove_user_connection(centrals_copy, liftings_copy,
                                          transmisions_copy, distributions_copy,
                                          consumers_copy)
    return remove_user_connection(centrals, liftings, transmisions,
                                  distributions, consumers)
