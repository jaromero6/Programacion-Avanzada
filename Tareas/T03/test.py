import unittest
from entities import (ElectricalGeneratingCentral, LiftingStation,
                      TransmisionSubstation, DistributionSubstation, Consumer)
from queries import (total_energy_consumed_by_commune,
                     client_with_the_highest_consumption,
                     client_with_the_less_consumption,
                     drained_power_in_transmision, consumption)
from exceptions import ElectricalOverload, ForbbidenAction, InvalidQuery
from data_structures import IdList, List
from user_interact import check_input


class DemandChecker(unittest.TestCase):  # Chequea la demanda

    def setUp(self):
        self.centrals_1, self.liftings_1, self.transmisions_1, \
        self.distributions_1, self.consumers_1 = create_lineal_graph()
        self.centrals_2, self.liftings_2, self.transmisions_2, \
        self.distributions_2, self.consumers_2 = create_double_graph()

    def tearDown(self):
        self.centrals_1, self.liftings_1, self.transmisions_1, \
        self.distributions_1, self.consumers_1 = create_lineal_graph()
        self.centrals_2, self.liftings_2, self.transmisions_2, \
        self.distributions_2, self.consumers_2 = create_double_graph()

    def test_queries(self):  # Verifica consultas
        # Consumo de una comuna -----------------------------------------
        self.assertEqual(total_energy_consumed_by_commune(
            self.distributions_1, "c", self.consumers_1, self.centrals_1),
            4.999999999999998)
        self.assertEqual(total_energy_consumed_by_commune(
            self.distributions_2, "c", self.consumers_2, self.centrals_2), 21)
        #  Cliente con mayor consumo ----------------------------------------
        self.assertEqual(client_with_the_highest_consumption(
            self.consumers_1, "a"), 4.999999999999998)
        self.assertEqual(client_with_the_highest_consumption(
            self.consumers_2, "a"), 14.002226332857944)
        # Cliente con menor consumo -----------------------------------------
        self.assertEqual(client_with_the_less_consumption(
            self.consumers_1, "a"), 4.999999999999998)
        self.assertEqual(client_with_the_less_consumption(
            self.consumers_2, "a"), 1.0)
        # Potencia perdida ---------------------------------------------------
        self.assertEqual(drained_power_in_transmision(
            self.consumers_1, 0), 0.0034168979250670394)
        self.assertEqual(drained_power_in_transmision(
            self.consumers_2, 3), 0.009046012020861385)
        # Consumo de distribuidora
        self.assertEqual(consumption(self.distributions_1, 0),
                         10.001011969480881)
        self.assertEqual(consumption(
            self.distributions_2, 1), 19.0050602980006)

    def test_errors(self):  # Verifica los levantamientos de errores
        # ElectricalOverload ------------------------------------------------
        overloading_node = Consumer(0, "a", "b", "c", 29)
        with self.assertRaises(ElectricalOverload):
            self.consumers_1[0].value.add_connection(overloading_node, 18)
            for i in self.centrals_1:
                i.value._demanded_power = 0
            for i in self.centrals_1:
                i.value.demanded_power
        overloading_node = Consumer(0, "a", "b2", "c", 29)
        with self.assertRaises(ElectricalOverload):
            self.consumers_2[3].value.add_connection(overloading_node, 18)
            for i in self.centrals_2:
                i.value._demanded_power = 0
            for i in self.centrals_2:
                i.value.demanded_power
        # Forbbiden Action Agregar Conexion ------------------------
        different_node = DistributionSubstation(4, "a", "b", "cx", "d", 10)
        lifting_node = LiftingStation(4, "a", "b", "c", "d", 12)
        with self.assertRaises(ForbbidenAction):  # Union no valida
            self.centrals_1[0].value.add_connection(different_node, 5)
        with self.assertRaises(ForbbidenAction):  # Distinta comuna
            different_node.add_connection(self.consumers_1[0].value, 12)
        with self.assertRaises(ForbbidenAction):  # Se añade un padre extra
            # no valido
            lifting_node.add_connection(self.transmisions_1[0].value, 12)
        # Forbbiden Action Remover conexion
        with self.assertRaises(ForbbidenAction):  # Remover un camino no
            # existente
            self.centrals_2[0].value.remove_connection(self.consumers_2[
                                                           0].value)
        with self.assertRaises(InvalidQuery):  # Comprueba ints
            check_input(5, List(1, 2, 3))
        with self.assertRaises(InvalidQuery):
            check_input("2", List("22", "1", "3"))  # Comprueba strl


def create_lineal_graph():  # Crea un grafo simple
    centrals = IdList(ElectricalGeneratingCentral(0, "a", "b", "c",
                                                  "d",
                                                  "e",
                                                  1000))
    liftings = IdList(LiftingStation(0, "a", "b", "c", "d", 5))
    transimisions = IdList(TransmisionSubstation(0, "a", "b", "c",
                                                 "d", 5))
    distributions = IdList(DistributionSubstation(0, "a", "b", "c",
                                                  "d", 5))
    consumers = IdList(Consumer(0, "a", "b", "c", 5))
    centrals[0].value.quick_connection(liftings[0].value, 1)
    liftings[0].value.quick_connection(transimisions[0].value, 1)
    transimisions[0].value.quick_connection(distributions[0].value, 1)
    distributions[0].value.quick_connection(consumers[0].value, 1)
    total = 0
    for i in centrals:
        total += i.value.demanded_power
    for i in consumers:
        i.value.distribute_power()
    return centrals, liftings, transimisions, distributions, consumers


def create_double_graph():  # Crea con dos sistemas electricos
    centrals = IdList(ElectricalGeneratingCentral(0, "a", "b1", "c", "d", "e",
                                                  1000),
                      ElectricalGeneratingCentral(1, "a", "b2", "c", "d", "e",
                                                  1000))
    liftings = IdList(LiftingStation(0, "a", "b1", "c", "d", 5),
                      LiftingStation(1, "a", "b2", "c", "d", 5))
    transimisions = IdList(TransmisionSubstation(0, "a", "b1", "c", "d", 5),
                           TransmisionSubstation(1, "a", "b2", "c", "d", 5))
    distributions = IdList(DistributionSubstation(0, "a", "b1", "c", "d", 5),
                           DistributionSubstation(1, "a", "b2", "c", "d", 5))
    consumers = IdList(Consumer(0, "a", "b1", "c", 7), Consumer(1, "a", "b2",
                                                                "c", 3),
                       Consumer(2, "a", "b2", "c", 1), Consumer(3, "a", "b2",
                                                                "c", 10))
    centrals[0].value.quick_connection(liftings[0].value, 1)
    liftings[0].value.quick_connection(transimisions[0].value, 1)
    transimisions[0].value.quick_connection(distributions[0].value, 1)
    distributions[0].value.quick_connection(consumers[0].value, 1)
    centrals[1].value.quick_connection(liftings[1].value, 1)
    liftings[1].value.quick_connection(transimisions[1].value, 1)
    transimisions[1].value.quick_connection(distributions[1].value, 1)
    distributions[1].value.quick_connection(consumers[1].value, 1)
    consumers[1].value.quick_connection(consumers[2].value, 1)
    consumers[1].value.quick_connection(consumers[3].value, 1)
    total = 0
    for i in centrals:
        total += i.value.demanded_power
    for i in consumers:
        i.value.distribute_power()
    return centrals, liftings, transimisions, distributions, consumers
