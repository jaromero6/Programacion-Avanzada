from data_structures import List, IdList
from exceptions import ElectricalOverload, ForbbidenAction
from read_db import calculate_ideal_demanded_power, distribute_the_power
from entities import ElectricalGeneratingCentral


def copy_entity(entity):
    if type(entity) == ElectricalGeneratingCentral:
        pow_cons = entity.received_power
    else:
        pow_cons = entity.power_consumed
    copy_ent = type(entity)(id_=entity.id_structure, name=entity.name,
                            electrical_system=entity.electrical_system,
                            province=entity.province,
                            commune=entity.commune,
                            type_energy=entity.type_energy,
                            power_consumed=pow_cons)
    return copy_ent


def copy_list_entities(entity_list):
    copy_list = IdList()
    for i in entity_list:
        entity = copy_entity(i.value)
        copy_list.append(entity.id_structure, entity)
    return copy_list


def get_distance(to_element, from_element):
    for i in to_element.parents_data:
        if i.value[0].value == from_element:
            return i.value[1].value


def connect_consumers(original_consumer, list_copy_consumers):
    for i in original_consumer.connected_to:
        list_copy_consumers[
            original_consumer.id_structure].value.quick_connection(
            list_copy_consumers[i.id_structure].value, get_distance(
                i, original_consumer))


def connect_copy(original_element, copy_element, down_list, upper_list):
    for i in original_element.connected_to:  # Se le añaden hijos

        copy_element.quick_connection(down_list[i.id_structure].value,
                                      get_distance(i, original_element))
    for i in original_element.parents_data:  # Lo agregamos como hijo
        upper_list[i.value[0].value.id_structure].value.quick_connection(
            copy_element, get_distance(original_element, i.value[0].value))


def get_copy_of_system(centrals, liftings, transmisions, distributions,
                       consumers):
    # Se hacen las copias
    centrals_copy = copy_list_entities(centrals)
    liftings_copy = copy_list_entities(liftings)
    transmisions_copy = copy_list_entities(transmisions)
    distributions_copy = copy_list_entities(distributions)
    consumers_copy = copy_list_entities(consumers)
    # Se hacen las conexiones
    for i in liftings:
        connect_copy(i.value, liftings_copy[i.value.id_structure].value,
                     transmisions_copy, centrals_copy)
    for i in distributions:
        connect_copy(i.value, distributions_copy[i.value.id_structure].value,
                     consumers_copy, transmisions_copy)
    for i in consumers:
        connect_consumers(i.value, consumers_copy)
    return List(centrals_copy, liftings_copy, transmisions_copy,
                distributions_copy, consumers_copy)


def restart_system(centrals, liftings, transmisions, distributions, consumers):
    for i in centrals:
        i._demanded_power = 0
        i.received = False
    for i in liftings:
        i._demanded_power = 0
        i.received = False
        i.received_power = 0
    for i in transmisions:
        i._demanded_power = 0
        i.received = False
        i.received_power = 0
    for i in distributions:
        i._demanded_power = 0
        i.received = False
        i.received_power = 0
    for i in consumers:
        i._demanded_power = 0
        i.received = False
        i.received_power = 0
    print("Calculando demanda y flujo ...")
    calculate_ideal_demanded_power(centrals)
    distribute_the_power(consumers)


# Agregar y remover conexiones -------------------------------------------------

def add_connection_modify(from_, to, distance, centrals, liftings, transmisions,
                          distributions, consumers):
    from_.add_connection(to, distance)
    restart_system(centrals, liftings, transmisions, distributions,
                   consumers)


def remove_connection_modify(from_, to, centrals, liftings, transmisions,
                             distributions, consumers):
    from_.remove_connection(to)
    restart_system(centrals, liftings, transmisions, distributions,
                   consumers)


def add_connection(from_, to, distance, centrals, liftings, transmisions,
                   distributions, consumers):
    factible_change = False
    try:
        add_connection_modify(from_, to, distance, centrals, liftings,
                              transmisions, distributions, consumers)
    except ElectricalOverload as err:
        print(f"{err}")
    except ForbbidenAction as err:
        print(f"{err}")
    finally:
        return factible_change


def remove_connection(from_, to, centrals, liftings, transmisions,
                      distributions, consumers):
    facttible_change = False
    try:
        remove_connection_modify(from_, to, centrals, liftings, transmisions,
                                 distributions, consumers)
        facttible_change = True
    except ElectricalOverload as err:
        print(f"{err}")
    except ForbbidenAction as err:
        print(f"{err}")
    finally:
        return facttible_change


# Agregar y remover Nodos ------------------------------------------------------

def add_node_modify(new_node, list_of_entities, centrals,
                    liftings, distributions, transmisions, consumers):
    list_of_entities.append(new_node.id_structure, new_node)
    restart_system(centrals, liftings, transmisions, distributions,
                   consumers)


def remove_node_modify(removed_node, centrals, liftings,
                       transmisions, distributions, consumers):
    removed_node.remove_self(liftings, transmisions, distributions, consumers)
    restart_system(centrals, liftings, transmisions, distributions,
                   consumers)


def add_node(new_node, list_of_entities, centrals,
             liftings, distributions, transmisions, consumers):
    facttible_change = False
    try:
        add_node_modify(new_node, list_of_entities, centrals,
                        liftings,
                        transmisions,
                        distributions, consumers)
        facttible_change = True
    except ElectricalOverload as err:
        print(f"{err}")
    except ForbbidenAction as err:
        print(f"{err}")
    finally:
        return facttible_change


def remove_node(removed_node, centrals, liftings,
                transmisions, distributions, consumers):
    facttible_change = False
    try:
        remove_node_modify(removed_node, centrals, liftings,
                           transmisions,
                           distributions, consumers)
        facttible_change = True
    except ElectricalOverload as err:
        print(f"{err}")
    except ForbbidenAction as err:
        print(f"{err}")
    finally:
        return facttible_change
