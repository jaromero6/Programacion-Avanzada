from data_structures import List, Graph
from exceptions import ElectricalOverload, ForbbidenAction
from math import inf


class Entity:
    def __init__(self, id_, name, electrical_system, province, commune,
                 cross_sectional_area, receptor):
        self.id_structure = id_
        self.name = name
        self.electrical_system = electrical_system
        self.province = province
        self.commune = commune
        self.cross_sectional_area = cross_sectional_area
        self.connected_to = Graph(id_, self)
        self.receptor = receptor
        self.max_of_parents = inf
        self.power_consumed = 0.0  # potencia que se necesita para funcionar
        self.parents_data = List()
        self.received_power = 0.0
        self._demanded_power = 0.0  # Guarda el valor de la demanda,
        # así este solo se calcula una vez
        self.received = False
        self.extra_energy = 0

    @property
    def current_power(self):
        if isinstance(self, Consumer) and self.received_power > 30:
            raise ElectricalOverload("Añadir",
                                     f"{self._demanded_power - 30} mW")
        available = self.received_power - self.power_consumed
        if available <= 0:
            return 0
        return available

    @property
    def used_power(self):
        used = self.received_power - self.current_power
        if used < 0:
            return self.received_power
        return used

    @property
    def demanded_power(self):
        """
        Retorna la potencia demandada por el nodo actual mas la potencia
        demandada por los hijos de este considerando la perdida de energia
        """
        total_power = self.power_consumed
        for i in self.connected_to:
            total_power += self.power_required_to_send(i)
            # resistencia
        if len(self.parents_data) > 0:
            self._demanded_power = total_power / len(self.parents_data)
            if self._demanded_power > 30 and isinstance(self, Consumer):
                raise ElectricalOverload("Add_connection",
                                         f"{self._demanded_power - 30} mW")
            return total_power / len(self.parents_data)  # Se divide el gasto
        # entre los padres del nodo
        self._demanded_power = total_power  # Asi se accede más rapido a este
        #  valor
        if self._demanded_power > 30 and isinstance(self, Consumer):
            raise ElectricalOverload("Add_connection",
                                     f"{self._demanded_power - 30} mW")
        return total_power

    @property
    def drained_energy(self):
        total_drained = 0
        direct_connnection = self.find_direct_connection()
        if direct_connnection is None:
            print("Casa aislada")
            return 0
        first = 0
        second = 1
        while first < len(direct_connnection) - 1:
            total_drained += (direct_connnection[
                                  first].value.get_relative_power_to_send(
                direct_connnection[second].value) * direct_connnection[
                                  second].value.get_resistance(
                direct_connnection[first].value))
            # Se suma: Potencia mandada * Resistenca = Potencia perdida en el
            #  cable
            first += 1
            second += 1
        return total_drained

    def find_direct_connection(self):  # Busca la conexion directa a una
        # elevadora
        if isinstance(self, LiftingStation):  # Caso base: Llegamos a la
            # estacion elevadora
            return List(self)
        for i in self.parents_data:  # De lo contrario buscamos en los padres
            result = i.value[0].value.find_direct_connection()
            if result is not None:
                result.append(self)  # Se agrega a si mismo y se retorna
                return result

    def power_required_to_send(self, element):  # Retorna
        # potencia requerida por un element que es hijo del nodo actual
        return element.demanded_power / (1 - element.get_resistance(self))

    def get_relative_power_to_send(self, element):
        # Emtrega la cantidad de energia que debe mandar  a element en relacion
        # a lo que están demandadando en total al nodo actual
        total = 0
        element_demand = element._demanded_power / (1 - element.get_resistance(
            self))
        for i in self.connected_to:
            total += i._demanded_power / (1 - i.get_resistance(
                self))
        return self.current_power * (element_demand / max(1, total))

    def get_resistance(self, from_):  # Entrega solo la potencia pérdida
        # entre el nodo actual y un padre
        RESISTIVITY = 0.0172
        for i in self.parents_data:
            if i.value[0].value == from_:
                return RESISTIVITY * i.value[1].value / i.value[2].value

    def use_extra_energy(self, demanded_power, power_to_send):
        if self.extra_energy == 0:
            return power_to_send  # Si es 0 no ocurre nada
        if demanded_power - power_to_send <= self.extra_energy:
            self.extra_energy -= demanded_power - power_to_send  # Se le resta
            # lo que se ocupa de esta sobra
            return demanded_power  # Se suple la demanda
        aditional = power_to_send + self.extra_energy  # Se usa extra
        self.extra_energy = 0  # Se usará toda
        return aditional

    def send_power(self, element):
        power_to_send = self.get_relative_power_to_send(element)
        # Se verifica que no se mande más de lo necesario
        if power_to_send > element._demanded_power / (1 -
                                                    element.get_resistance(
                                                              self)):
            self.extra_energy += power_to_send - (element._demanded_power / (
                1 - element.get_resistance(self)))
            element.received_power += element._demanded_power  # Se suple su
            # demanda
        else:
            element.received_power += self.use_extra_energy(
                element._demanded_power, power_to_send) * (1 -
                                                        element.get_resistance(
                                                               self))

    def distribute_power(self, to=None):
        # Primero el nodo le pide a todos sus padres que le manden energia
        if not self.received:
            for i in self.parents_data:
                i.value[0].value.distribute_power(self)
                # Luego de que ya le llega energía desde todos sus padres
                # entonces le manda a sus hijos
        self.received = True  # Ya recibio la energia asi que dejamos el
        # registro de que recibio completamente su energia
        if to is not None:
            for i in self.connected_to:
                if i == to:
                    self.send_power(i)
                    return

    def set_parent_data(self, element, distance):
        """
        Envia la informacion del padre a parents_data de element
        """
        data = List(self, distance, self.cross_sectional_area)
        element.parents_data.append(data)

    def delete_parent_data(self, element):
        index_ = 0
        for i in element.parents_data:
            if i.value[0].value == self:
                element.parents_data.remove(index_)
                return
            index_ += 1

    def quick_connection(self, element, distance):  # Funciona igual que
        # add_connection solo que se evita hacer comparaciones
        self.set_parent_data(element, distance)
        self.connected_to.add_node(element.id_structure, element)
        self.connected_to.add_connection(element.id_structure)

    def add_connection(self, element, distance):
        if (isinstance(element, TransmisionSubstation) or isinstance(element,
                                        DistributionSubstation)) and len(
            element.parents_data) > 0:
            raise ForbbidenAction("add_connection", "Subestaciones de "
                                                    "transmision no admiten "
                                                    "más de un padre")
        if ((isinstance(self, Consumer) or isinstance(self,
                                DistributionSubstation)) and isinstance(
            element, Consumer)) and \
                        self.commune != element.commune:
            raise ForbbidenAction("add_connection", f"Imposible unir "
                                f"{type(self)} con {type(element)} debido a "
                                f"que son de distintas comunas")
        if self.electrical_system == element.electrical_system:
            if type(element) == self.receptor:
                if element not in self.connected_to:
                    self.connected_to.add_node(element.id_structure,
                                               element)
                    self.connected_to.add_connection(element.id_structure)
                    self.set_parent_data(element, distance)
                else:  # Si la conexion existe
                    raise ForbbidenAction("add_connection", f"El camino ya "
                                                            f"existe")

                return
            raise ForbbidenAction("add_connection", f"{type(self)} no "
                                                    f"puede unirse a "
                                                    f"{type(element)}")
        raise ForbbidenAction("add_connection",
                              "Nodos de distintos sistemas "
                              "electricos")

    def remove_connection(self, element):
        if element in self.connected_to:
            self.connected_to.remove_connection(element.id_structure)
            self.delete_parent_data(element)
        else:
            raise ForbbidenAction("remove_connection",
                                  f"Camino no existente")

    def remove_self(self, liftings, transmisions, distributions, consumers):
        for i in self.parents_data:  # Se desconecta de los padres
            i.value[0].value.remove_connection(self)
        for i in self.connected_to:  # Se desconecta de los hijos
            self.remove_connection(i)
            if len(i.parents_data) == 0:  # En caso que el hijo se quede sin
                # padre también se extrae
                i.remove_self(liftings, consumers, distributions, consumers)
        # Finalmente el nodo se quita de la lista
        if isinstance(self,LiftingStation):
            liftings.remove(self.id_structure)
        elif isinstance(self,TransmisionSubstation):
            transmisions.remove(self.id_structure)
        elif isinstance(self, DistributionSubstation):
            distributions.remove(self.id_structure)
        elif isinstance(self, Consumer):
            consumers.remove(self.id_structure)

    def __eq__(self, other):
        return self.id_structure == other.id_structure


# power cnosumed para la central es su energia inicial


class ElectricalGeneratingCentral(Entity):
    def __init__(self, id_, name, electrical_system, province, commune,
                 type_energy, power_consumed):
        super().__init__(id_, name, electrical_system, province, commune, 253,
                         LiftingStation)
        self.type_energy = type_energy
        self.received_power = power_consumed  # En este caso es su energia
        # inicial

# Los parametros **kwargs son para poder hacer una copia de la entidad


class LiftingStation(Entity):
    def __init__(self, id_, name, electrical_system, province, commune,
                 power_consumed, **kwargs):
        super().__init__(id_, name, electrical_system, province, commune,
                         202.7, TransmisionSubstation)
        self.power_consumed = power_consumed
        self.type_energy = None


class TransmisionSubstation(Entity):
    def __init__(self, id_, name, electrical_system, province, commune,
                 power_consumed, **kwargs):
        super().__init__(id_, name, electrical_system, province, commune, 152,
                         DistributionSubstation)
        self.power_consumed = power_consumed
        self.max_of_parents = 1
        self.type_energy = None


class DistributionSubstation(Entity):
    def __init__(self, id_, name, electrical_system, province, commune,
                 power_consumed, **kwargs):
        super().__init__(id_, name,
                         electrical_system, province, commune, 85, Consumer)
        self.power_consumed = power_consumed
        self.max_of_parents = 1
        self.type_energy = None


class Consumer(Entity):
    def __init__(self, id_, electrical_system, province, commune,
                 power_consumed, **kwargs):
        super().__init__(id_, None, electrical_system, province, commune,
                         85, Consumer)
        self.power_consumed = power_consumed
        self.type_energy = None
