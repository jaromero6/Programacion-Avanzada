from random import triangular, normalvariate, uniform
from parameters import PROB_DEALER_CORROMPIDO, PROB_DEALER_EXPULSAR
from collections import deque

"""
Personal lo unico que hace es entregar un valor para un turno y un valor para un
descanso, mientra que su tick consiste en sumar un segundo aa segundos usados 
que indican cuanto tiempo gastado llevan ya sea en descanso o en trabajo. La
accion de ponerlos a trabajar o a descansar esta a cargo de la clase 
Administracion, que además se encarga de asignar el personal correcto a cada 
instalacion
"""


class Personal:
    id_pers = 0

    def __init__(self, nombre, edad, tipo, limites_ditrb):
        self.id_personal = Personal.id_pers
        Personal.id_pers += 1
        self.nombre = nombre
        self.edad = edad
        self.tipo = tipo
        self.limites_distrib = limites_ditrb
        self.segundos_usados = 0
        self.duracion_turno_actual = 0
        self.tiempo_del_siguiente_turno = 0

    @property
    def tiempo_descanso(self):
        tiempo_1 = 3600 * abs(int(normalvariate(14, 5)))
        respeta_maximo = min([72000, tiempo_1])
        respeta_minimo = max([28800, respeta_maximo])
        return respeta_minimo

    @property
    def siguiente_turno(self):
        if self.tiempo_descanso % 3600 == 0:
            return self.tiempo_descanso
        else:
            # Si la hot no calza justo se le da tiempo hasta la siguiente hora
            tiempo_extra = 3600 - (self.tiempo_descanso % 3600)
            return self.tiempo_descanso + tiempo_extra

    @property
    def tomar_turno(self):
        duracion_del_turno = 60 * int(triangular(
            *self.limites_distrib))
        return duracion_del_turno

    def tick_personal(self):
        self.segundos_usados += 1


class Bartender(Personal):
    def __init__(self, nombre, edad):
        super().__init__(nombre, edad, "bartender", (360, 540, 490))


class Dealer(Personal):
    def __init__(self, nombre, edad):
        super().__init__(nombre, edad, "dealer", (360, 540, 540))
        probabilidad = uniform(0, 1)
        self.comprado_por_la_mafia = probabilidad <= PROB_DEALER_CORROMPIDO

    def descubrir_tramposo(self, lista_sospechosos):
        for sospechoso in lista_sospechosos:
            if sospechoso.trampa:
                probabilidad = uniform(0, 1)
                lo_descubre = probabilidad <= PROB_DEALER_EXPULSAR
                if lo_descubre:
                    sospechoso.destino = None
                    sospechoso.llega_a_objetivo = False
                    sospechoso.decision_tomada = "retirarse"
                    sospechoso.tiempo = 0
                    sospechoso.razones_salida["trampa"] += 1


class MrT(Personal):
    def __init__(self, nombre, edad):
        super().__init__(nombre, edad, "mr_t", (360, 540, 420))


class Administracion:
    def __init__(self, tarots, restobars, ruletas, tragamonedas, mrts,
                 bartenders, dealers):
        self.tarots = tarots
        self.restobars = restobars
        self.ruletas = ruletas
        self.tragamonedas = tragamonedas
        self.bartenders_descan = bartenders
        self.dealers_descan = dealers
        self.mrts_descan = mrts

    def poner_a_trabajar_a_personal(self, instalacion, terminan_descanso,
                                    personal_a_cargo):
        if len(terminan_descanso) >0:
            ingresa_al_turno = personal_a_cargo.pop(
                personal_a_cargo.index(terminan_descanso.popleft()))
            ingresa_al_turno.trabajando = True
            ingresa_al_turno.segundos_usados = 0
            ingresa_al_turno.duracion_turno_actual = ingresa_al_turno \
                .tomar_turno
            ingresa_al_turno.tiempo_del_siguiente_turno = 0
            instalacion.personal_instalacion.append(ingresa_al_turno)

    def poner_a_descansar_a_personal(self, instalacion, personal_descansando):
        terminan_turno = filter(lambda x: x.segundos_usados >=
                                          x.duracion_turno_actual,
                                instalacion.personal_instalacion)
        for i in terminan_turno:
            trabajador = instalacion.personal_instalacion.pop(
                instalacion.personal_instalacion.index(i))
            trabajador.segundos_usados = 0
            trabajador.duracion_turno_actual = 0
            trabajador.tiempo_del_siguiente_turno = trabajador.siguiente_turno
            personal_descansando.append(trabajador)

    def abastecer_instalacion(self, instalaciones, personal_a_cargo):
        terminan_descanso = deque(filter(lambda x: x.segundos_usados >=
                                                   x.tiempo_del_siguiente_turno,
                                         personal_a_cargo))
        # Se priorizan las que no funcionan
        prioridad = filter(lambda x: not x.funcionando, instalaciones)
        funcionan = filter(lambda x: x.funcionando, instalaciones)
        for i in prioridad:
            self.poner_a_trabajar_a_personal(i, terminan_descanso,
                                             personal_a_cargo)
            i.ejecutar_accion()
        for i in funcionan:
            # Cada trabajador ejecuta su tick:
            for j in i.personal_instalacion:
                j.tick_personal()
            if i.maximo_personal is None:
                self.poner_a_trabajar_a_personal(i, terminan_descanso,
                                                     personal_a_cargo)
            else:
                if len(i.personal_instalacion) < i.maximo_personal:
                    self.poner_a_trabajar_a_personal(i, terminan_descanso,
                                                         personal_a_cargo)
            self.poner_a_descansar_a_personal(i, personal_a_cargo)
            i.ejecutar_accion()

    def tick_de_instalaciones(self):
        self.abastecer_instalacion(self.tarots, self.mrts_descan)
        self.abastecer_instalacion(self.restobars, self.bartenders_descan)
        self.abastecer_instalacion(self.ruletas, self.dealers_descan)
        self.abastecer_instalacion(self.tragamonedas, self.dealers_descan)
        for i in self.mrts_descan:
            i.tick_personal()
        for i in self.bartenders_descan:
            i.tick_personal()
        for i in self.dealers_descan:
            i.tick_personal()
