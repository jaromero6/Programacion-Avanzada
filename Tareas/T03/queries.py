from math import inf


def total_energy_by_system(centrals):
    total = 0
    for i in centrals:
        if i.value._demanded_power > i.value.current_power:
            total += i.value.current_power
        else:
            total += i.value._demanded_power
    return total


def total_energy_consumed_by_commune(distribution_substation, commune_name,
                                     consumers, centrals):
    commune_consumption = 0
    for i in distribution_substation:
        if i.value.commune == commune_name:
            commune_consumption += i.value.used_power
    for i in consumers:
        if i.value.commune == commune_name:
            if i.value.received_power >= i.value.power_consumed:
                commune_consumption += i.value.power_consumed
            else:
                commune_consumption += i.value.received_power
    print(f"Consumo de la comuna {commune_name} : "
          f"{commune_consumption * 1000} kW")
    print(f"Porcentaje respecto al consumo total "
          f"{100 * commune_consumption / total_energy_by_system(centrals)} %")
    return commune_consumption


def client_with_the_highest_consumption(consumers, electrical_system,
                                        *extra_args):
    highest_consume = 0
    greatest_client = None
    for i in consumers:
        if i.value.electrical_system == electrical_system:
            if i.value.received_power >= highest_consume:
                highest_consume = i.value.received_power
                greatest_client = i.value
    if greatest_client is None:
        print(f"La consulta no arrojó resultados")
        return None
    print(f"Id cliente con mayor consumo: {greatest_client.id_structure}")
    print(f"Provincia: {greatest_client.province}")
    print(f"Comuna: {greatest_client.commune}")
    print(f"Consumo: {highest_consume} mW")
    return highest_consume


def client_with_the_less_consumption(consumers, electrical_system, *extra_args):
    less_consume = inf
    less_consumer = None
    for i in consumers:
        if i.value.electrical_system == electrical_system:
            if i.value.received_power <= less_consume:
                less_consume = i.value.received_power
                less_consumer = i.value
    if less_consumer is None:
        print(f"La consulta no arrojó resultados")
        return None
    print(f"Id cliente con mayor consumo: {less_consumer.id_structure}")
    print(f"Provincia: {less_consumer.province}")
    print(f"Comuna: {less_consumer.commune}")
    print(f"Consumo: {less_consume} mW")
    return less_consume


def drained_power_in_transmision(consummers, id_consumer, *extra_args):
    for i in consummers:
        if i.value.id_structure == id_consumer:
            print(f"Energia perdida: {i.value.drained_energy} mW")
            return i.value.drained_energy
    print("La consulta no arrojó resultados")


def consumption(distributions_list, id_distribution, *extra_args):
    for i in distributions_list:
        if i.value.id_structure == id_distribution:
            print(f"Consumo: {i.value.received_power} mW")
            return i.value.received_power
    print("La consulta no arrojó resultados")
