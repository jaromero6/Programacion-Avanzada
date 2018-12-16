from gui.entities import Game
from collections import deque

from parameters import TIEMPO_ESPERA_JUEGOS, MAXIMO_ESPERA_JUEGOS, \
    P_GANAR_TRAGAMONEDAS, NUMEROS_RULETA, P_OTRA_RONDA, N_RONDAS, \
    BOOST_TRAMPA, AUMENTO_PROBABILIDAD_DE_TINI, DURACION_RONDA
from random import uniform, choice


class Juegos(Game):
    id_de_los_juegos = 0

    def __init__(self, casino, tipo, cap_max, tiempo_juego, pos_x, pos_y):
        super().__init__(tipo, pos_x, pos_y)
        self.juegos_id = Juegos.id_de_los_juegos
        Juegos.id_de_los_juegos += 1
        self.tipo = tipo
        self.capacidad_maxima = cap_max
        self.tiempo_juego = tiempo_juego
        self.funcionando = False
        self.tiempo_nfuncionando = 0
        self.por_llegar = list()
        self.atendiendo = deque()
        self.gente_en_espera = deque()
        self.dinero_perdido_total = 0
        self.dinero_ganado_total = 0
        self.total_visitas = 0
        self.casino_pertenencia = casino

    def __eq__(self, other):
        return self.juegos_id == other.juegos_id

    def sacar_clientes(self, cliente):
        cliente.tiempo = 0
        cliente.decision_tomada = None
        cliente.llega_a_objetivo = False
        cliente.destino = None

    def causar_efectos(self, cliente):
        self.sacar_clientes(cliente)

    def agregar_futuro_cliente(self, cliente):
        self.por_llegar.append(cliente)

    def recibir_clientes(self):
        llegaron = filter(lambda x: x.llega_a_objetivo, self.por_llegar)
        for i in llegaron:
            llega = self.por_llegar.pop(self.por_llegar.index(i))
            self.total_visitas += 1
            if len(self.gente_en_espera) < MAXIMO_ESPERA_JUEGOS:
                self.gente_en_espera.append(llega)
            else:
                self.sacar_clientes(llega)

    def atender_clientes(self):
        if len(self.atendiendo) < self.capacidad_maxima:
            if len(self.gente_en_espera) > 0:
                atender = self.gente_en_espera.popleft()
                atender.tiempo = 0
                self.atendiendo.append(atender)
        se_van = filter(lambda x: x.tiempo > TIEMPO_ESPERA_JUEGOS,
                        self.gente_en_espera)
        for i in se_van:
            self.sacar_clientes(i)
        self.gente_en_espera = deque(filter(lambda x: x.tiempo <=
                                                      TIEMPO_ESPERA_JUEGOS,
                                            self.gente_en_espera))

    def sacar_a_los_que_cambian_de_opinion(self):
        # Si un cliente cambia por X su decision a None, entonces se reitra y
        #  no se le aplicaran los efectos del juego
        cambian_de_parecer = filter(lambda x: x.decision_tomada is None or
                                              x.destino is None,
                                    self.gente_en_espera)
        for i in cambian_de_parecer:
            self.sacar_clientes(i)
        self.gente_en_espera = deque(filter(lambda x: x.decision_tomada is
                                                      not None and x.destino
                                                                   is not None,
                                            self.gente_en_espera))
        cambian_de_parecer = filter(lambda x: x.decision_tomada is None or
                                              x.destino is None,
                                    self.atendiendo)
        for i in cambian_de_parecer:
            self.sacar_clientes(i)
        self.atendiendo = deque(filter(lambda x: x.decision_tomada is not
                                                 None and x.destino is not
                                                          None,
                                       self.atendiendo))

    def revisar(self):
        if not self.funcionando:
            for i in self.gente_en_espera:
                self.sacar_clientes(i)
            for i in self.atendiendo:
                self.sacar_clientes(i)
            self.gente_en_espera = deque()
            self.atendiendo = deque()

    def ingresar_apuesta(self, cliente):
        apuesta = cliente.apostar
        cliente.dinero -= apuesta  # Se realiza la apuesta
        return apuesta

    def realizar_accion(self):
        self.recibir_clientes()
        self.atender_clientes()
        self.revisar()
        self.sacar_a_los_que_cambian_de_opinion()


class Tragamonedas(Juegos):
    def __init__(self, casino, pos_x, pos_y):
        super().__init__(casino, "tragamonedas", 30, 180, pos_x, pos_y)
        self.angle += 90
        self.pozo = 0
        self.maximo_personal = 1
        self.tiempo_funcionando = 0
        self.personal_instalacion = list()

    def ingresar_apuesta(self, cliente):
        apuesta = super().ingresar_apuesta(cliente)

        self.casino_pertenencia.dinero += 0.1 * apuesta
        self.pozo += 0.9 * apuesta
        return apuesta

    def causar_efectos(self, cliente):
        apuesta = self.ingresar_apuesta(cliente)
        p_ganar = max([0, P_GANAR_TRAGAMONEDAS + (0.2 * cliente.suerte) - 0.1])
        intento = uniform(0, 1)
        if intento <= p_ganar:
            cliente.dinero += self.pozo
            self.dinero_perdido_total += self.pozo
            self.pozo = 0
        else:
            # El dinero que gana esta instalacion es solo el 0.1
            self.dinero_ganado_total += apuesta * 0.1
        super().causar_efectos(cliente)  # Finalmente el cliente sale de la
        # instalacion

    def ejecutar_accion(self):
        if len(self.personal_instalacion) == self.maximo_personal:
            self.funcionando = True
        else:
            self.funcionando = False
        if not self.funcionando:
            self.tiempo_nfuncionando += 1
        super().realizar_accion()
        if len(self.atendiendo) > 0:
            if self.atendiendo[0].tiempo >= self.tiempo_juego:
                atendido = self.atendiendo.popleft()
                self.causar_efectos(atendido)


class Ruleta(Juegos):
    def __init__(self, casino, pos_x, pos_y):
        super().__init__(casino, "ruleta", 15, 180, pos_x, pos_y)
        self.numeros_de_la_ruleta = {"verde": [0], "rojo": list(filter(lambda
                        x: x % 2 == 0, range(1, NUMEROS_RULETA + 1))),
                        "negro": list(filter(lambda x: x % 2 != 0,
                        range(1, NUMEROS_RULETA + 1)))}
        self.maximo_personal = None
        self.personal_instalacion = list()

    @property
    def dealer_coludido(self):
        for i in self.personal_instalacion:
            if i.comprado_por_la_mafia:
                return True
        return False

    def ingresar_apuesta(self, cliente):
        apuesta = super().ingresar_apuesta(cliente)
        # Se deja la apuesta en un monto que el casino pueda pagar en caso de
        #  esta ser superior al casino
        return apuesta

    def causar_efectos(self, cliente):
        apuesta = self.ingresar_apuesta(cliente)
        eleccion = choice(["numero", "color"])
        if eleccion == "color":
            eleccion = choice(["verde", "rojo", "negro"])
        if eleccion == "numero" or eleccion == "verde":
            probabilidad_juego = 1 / (NUMEROS_RULETA + 1)
            multiplicador = 5
        else:
            probabilidad_juego = 1 / (2 * (NUMEROS_RULETA + 1))
            multiplicador = 1.5
        intento = uniform(0, 1)
        if cliente.trampa:
            probabilidad_juego = min([1, probabilidad_juego * (1 +
                                                               BOOST_TRAMPA)])
        if cliente.tini and self.dealer_coludido:
            probabilidad_juego = min([1, probabilidad_juego * (1 +
                                            AUMENTO_PROBABILIDAD_DE_TINI)])
        if intento <= max([0, probabilidad_juego + (0.2 * cliente.suerte) -
                0.1]):
            gana_cliente = min([multiplicador * apuesta,
                                self.casino_pertenencia.dinero])
            cliente.dinero += gana_cliente
            self.dinero_perdido_total += gana_cliente
        else:
            self.casino_pertenencia.dinero += apuesta
            self.dinero_ganado_total += apuesta

    def descubir_tramposos(self):
        # Hace que cada dealer busque sospechosos
        [i.descubrir_tramposo(self.atendiendo) for i
         in self.personal_instalacion]

    def quitar_gente(self):
        # Quita a la gente sin dinero o que fue expulsada de la cola de gente
        #  que se esta atendiendo
        self.descubir_tramposos()
        se_van = filter(lambda x: x.dinero < 1 or
                                  x.decision_tomada == "retirarse",
                        self.atendiendo)
        for i in se_van:
            self.sacar_clientes(i)
        self.atendiendo = deque(filter(lambda x: x.dinero >= 1 or
                                                 x.decision_tomada != "retirarse",
                                       self.atendiendo))

    def ejecutar_accion(self):
        if len(self.personal_instalacion) > 0:
            self.funcionando = True
        else:
            self.funcionando = False
        if not self.funcionando:
            self.tiempo_nfuncionando += 1
        super().realizar_accion()
        self.quitar_gente()
        if len(self.atendiendo) > 0:
            if self.atendiendo[0].tiempo >= DURACION_RONDA:
                otra_ronda = uniform(0, 1)
                if otra_ronda <= P_OTRA_RONDA:
                    cliente = self.atendiendo[0]
                    cliente.tiempo = 0
                    if cliente.trampa:
                        if cliente.turnos_contando_cartas <= N_RONDAS:
                            cliente.turnos_contando_cartas += 1
                        else:
                            cliente.trampa = False
                            cliente.turnos_contando_cartas = 0
                else:
                    cliente = self.atendiendo.popleft()
                    self.sacar_clientes(cliente)
                self.causar_efectos(cliente)
