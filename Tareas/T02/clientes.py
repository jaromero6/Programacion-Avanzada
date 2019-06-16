from gui.entities import Human
from random import uniform, normalvariate, choice, choices
from parameters import INFLUENCIA_TINI, PROB_LLEGADA, CONSTANTE_APUESTA, \
    P_RECARGA, C_RECARGA
from math import pi


class Humano(Human):
    def __init__(self, pos_x=0, pos_y=0, parent=None):
        alto = (0.7, 1)
        medio = (0.3, 0.7)
        bajo = (0, 0.3)
        din = [0]
        luc = [0]
        ans = [0]
        sue = [0]
        soc = [0]
        sta = [0]
        des= [0]
        ludopata = {alto: [ans, sta], medio: [din, luc, sue, soc, des],
                    bajo: []}
        kibitzer = {alto: [soc], medio: [luc, sue, des], bajo: [din, sta, ans]}
        dieciochero = {alto: [soc, ans], medio: [sta, sue, din], bajo: [luc,
                                                                        des]}
        ganador = {alto: [soc, sta, sue, des], medio: [ans, din, luc], bajo: []}
        millonario = {alto: [din, sta], medio: [soc, sue, ans, luc, des],
                      bajo: []}
        personalidades = {"ludopata": ludopata, "kibitzer": kibitzer,
                          "dieciochero": dieciochero, "ganador": ganador,
                          "millonario": millonario}
        personality = choice(list(personalidades.keys()))
        super().__init__(personality, pos_x, pos_y, parent)
        for distribucion in personalidades[personality]:
            for i in range(len(personalidades[personality][distribucion])):
                personalidades[personality][distribucion][i][0] = uniform(
                    distribucion[0], distribucion[1])
        self.dinero_ = din[0] * 200
        self.sociabilidad_ = soc[0]
        self.lucidez_ = luc[0]
        self.suerte_ = sue[0]
        self.ansiedad_ = ans[0]
        self.stamina_ = sta[0]
        self.deshonestidad_ = des[0]
        self.monto_inicial = self.dinero_
        self.cambios_a_p_retirarse = []
        self.duracion_instalacion_ = 0
        self.tiempo_en_el_bano_ = 0

    @property
    def dinero(self):
        return self.dinero_
    @dinero.setter
    def dinero(self, valor):
        nuev_din = max([0, valor])
        self.dinero_ = nuev_din

    @property
    def sociabilidad(self):
        return self.sociabilidad_

    @sociabilidad.setter
    def sociabilidad(self, valor):
        n_soc = max([0, valor])
        n_soc = min([1, n_soc])
        self.sociabilidad_ = n_soc

    @property
    def lucidez(self):
        return self.lucidez_

    @lucidez.setter
    def lucidez(self, valor):
        n_luc = max([0, valor])
        n_luc = min([1, n_luc])
        self.lucidez_ = n_luc

    @property
    def suerte(self):
        return self.suerte_

    @suerte.setter
    def suerte(self, valor):
        n_suer = max([0, valor])
        n_suer = min([1, n_suer])
        self.suerte_ = n_suer

    @property
    def ansiedad(self):
        if 2 * self.monto_inicial <= self.dinero or 0.2 * self.monto_inicial \
                >= self.dinero:
            no_excede = min([1, 2 * self.ansiedad_])
            return no_excede
        return self.ansiedad_

    @ansiedad.setter
    def ansiedad(self, valor):
        n_ans = max([0, valor])
        n_ans = min([1, n_ans])
        self.ansiedad_ = n_ans

    @property
    def stamina(self):
        if self.dinero == 0:
            return 0
        return self.stamina_

    @stamina.setter
    def stamina(self, valor):
        n_sta = max([0, valor])
        n_sta = min([1, n_sta])
        self.stamina_ = n_sta

    @property
    def deshonestidad(self):
        return self.deshonestidad_

    @deshonestidad.setter
    def deshonestidad(self, valor):
        n_des = max([0, valor])
        n_des = min([1, n_des])
        self.deshonestidad_ = n_des

    @property
    def p_retirarse(self):
        return  max([0, 1 - self.stamina])

    @p_retirarse.setter
    def p_retirarse(self, valor):
        self.stamina = 1 - valor

    @property
    def p_jugar(self):
        return min([self.ansiedad, 1 - self.p_retirarse])

    @property
    def p_participar_en_actividad(self):
        return min([self.sociabilidad, max([0, 1 - self.p_jugar -
                                            self.p_retirarse])])

    @property
    def p_ir_instalacion(self):
        return 1 - min([1, self.p_retirarse + self.p_participar_en_actividad
                        + self.p_jugar])

    @property
    def duracion_actividades(self):
        dur_actividades = int(60 * max([self.lucidez + self.sociabilidad -
                                        self.ansiedad, 0.1]) * (pi ** 2))
        return dur_actividades

    @property
    def apostar(self):
        # Nota que la apuesta base siempre será 1
        apuesta = 1 + (CONSTANTE_APUESTA * self.ansiedad)
        apuesta = min([self.dinero, apuesta])
        return apuesta

    @property
    def duracion(self):
        if self.duracion_instalacion_ == 0:
            self.duracion_instalacion_ = abs(int(normalvariate(180, 300)))
        return self.duracion_instalacion_

    @duracion.setter
    def duracion(self, valor):
        self.duracion_ = valor

    @property
    def tiempo_en_el_bano(self):
        if self.tiempo_en_el_bano_ == 0:
            self.tiempo_en_el_bano_ = abs(int(normalvariate(180 * (
                    1 - self.lucidez), 120)))
        return self.tiempo_en_el_bano_

    @tiempo_en_el_bano.setter
    def tiempo_en_el_bano(self, valor):
        self.tiempo_en_el_bano_ = valor


class Persona(Humano):
    pers_id = 0

    def __init__(self, edad, nombre, pos_x=0, pos_y=0, parent=None):
        super().__init__(pos_x, pos_y, parent)
        self.persona_id = Persona.pers_id
        Persona.pers_id += 1
        self.edad = edad
        self.nombre = nombre
        self.amistades = dict()
        self.decision_tomada = None
        self.destino = None
        self.llega_a_objetivo = False
        self.trampa = False
        self.tiempo = 0
        self.tini = False
        self.tiempo_total = 0
        self.en_el_casino = False
        self.turnos_contando_cartas = 0
        self.boost_ansiedad = False
        self.hizo_trampa_alguna_vez = False
        self.razones_salida = {"personales": 0, "dinero": 0, "trampa": 0}

    def abandonar_idea_por_falta_de_dinero(self):
        self.destino = None
        self.decision_tomada = "retirarse"
        self.llega_a_objetivo = False
        self.tiempo = 0
        self.tiempo_en_el_bano = 0
        self.duracion = 0

    # Ir a juegos/ instalaciones ----------------------------------------------
    def caminar_hacia_destino(self, elecciones, juego=False):
        if juego:
            if self.dinero < 1 and self.decision_tomada is None:
                self.abandonar_idea_por_falta_de_dinero()
                return
        if self.destino is None:
            final = choice(elecciones)
            if not juego:
                if self.dinero < final.costo:
                    self.abandonar_idea_por_falta_de_dinero()
                    return
            final.agregar_futuro_cliente(self)
            self.destino = (final.x, final.y)
        else:
            self.ir_a_instalacion(self.destino)
            if self.llega_a_objetivo:
                self.tiempo += 1

    def retirarse(self):
        self.destino = (50, -15)
        self.ir_a_instalacion(self.destino)
        if self.llega_a_objetivo:
            if self.dinero == 0:
                self.razones_salida["dinero"] += 1
            elif self.dinero != 0 and not self.trampa:
                self.razones_salida["personales"] += 1
            self.llega_a_objetivo = False
            self.en_el_casino = False
            self.decision_tomada = None
            self.destino = None

    # Actividades --------------------------------------------------------------
    def hablar(self, lugar_de_habla):
        if self.destino is None:
            lugar_de_habla.agregar_futuro_cliente(self)
        else:
            self.ir_a_instalacion(self.destino)
            if self.llega_a_objetivo:
                self.tiempo += 1

    def contar_cartas(self):
        if self.personality == "kibitzer":
            if len(self.amistades) > 0:
                probabilidad = uniform(0, 1)
                if probabilidad <= self.deshonestidad:
                    self.trampa = True
                    self.decision_tomada = "ruleta"
                    self.llega_a_objetivo = False
                    self.destino = None
                    self.hizo_trampa_alguna_vez = True
                    return
        self.decision_tomada = None
        self.llega_a_objetivo = False
        self.destino = None

    def ir_a_instalacion(self, pos_lugar):
        """
        Los clientes buscaran la ruta siempre de la misma forma, iran en
        linea recta hasta la parte superior, buscaran el
        pasilllo de su destino y se entonces bajaran o subiran hasta donde
        esta este
        :param instalacion:
        :return: None
        """
        if self.x + 25 == pos_lugar[0] and self.y == pos_lugar[1]:
            self.llega_a_objetivo = True
        elif self.x + 25 == pos_lugar[0]:
            if self.y >= pos_lugar[1]:
                self.y -= 1
            else:
                self.y += 1
        elif self.y == 10:
            if self.x + 25 >= pos_lugar[0]:
                self.x -= 1
            else:
                self.x += 1
        else:
            if self.y > 10:
                self.y -= 1
            else:
                self.y += 1

    def tomar_decision(self):
        decision = choices(["juego", "instalacion", "actividad", "retirarse"],
                           [self.p_jugar, self.p_ir_instalacion,
                            self.p_participar_en_actividad,
                            self.p_retirarse])[0]

        acciones = {"juego": ["ruleta", "tragamonedas"],
                    "instalacion": ["tarot", "restobar", "bano"],
                    "actividad": ["tini", "hablar", "coludirse", ],
                    "retirarse": ["retirarse"]}
        self.decision_tomada = choice(acciones[decision])

    def ejecutar_accion(self, ruleta, tragamoneda, tarot, restobar, bano,
                        lugar_de_habla, tini_il_padrino):
        decisiones = {"ruleta": (ruleta, True), "tragamonedas": (tragamoneda,
                                                                 True),
                      "tarot": (tarot, False), "restobar": (restobar, False),
                      "bano": (bano, False), "tini": ([tini_il_padrino], False)}
        if self.en_el_casino:
            self.tiempo_total += 1
            if self.decision_tomada is not None:
                if self.decision_tomada in decisiones:
                    self.caminar_hacia_destino(*decisiones[
                        self.decision_tomada])
                elif self.decision_tomada == "coludirse":
                    self.contar_cartas()
                elif self.decision_tomada == "hablar":
                    self.hablar(lugar_de_habla)
                elif self.decision_tomada == "retirarse":
                    self.retirarse()
            else:
                self.tomar_decision()
        else:
            if self.dinero > 0:
                if uniform(0, 1) <= PROB_LLEGADA:
                    # Si entra se resetean los valreos que puedan influir en
                    # otras acitvidades
                    self.trampa = False
                    self.llega_a_objetivo = False
                    self.decision_tomada = None
                    self.en_el_casino = True
                    self.tiempo = 0
                    self.duracion = 0
                    self.tiempo_en_el_bano = 0
            else:
                if uniform(0,1) <= P_RECARGA:
                    self.dinero += C_RECARGA

