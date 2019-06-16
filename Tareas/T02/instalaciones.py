from gui.entities import Building
from collections import deque
from random import choice, uniform
from parameters import TIEMPO_ESPERA_INSTALACION, EFECTO_MR_T, MAXIMO_ESPERA, \
    TIEMPO_ESPERA_HABLA, EFECTO_ANSIEDAD_CONVERSA, \
    EFECTO_DESHONESTIDAD_CONVERSA, INFLUENCIA_TINI

"""
Tanto juegos como instalaciones funcionan de la misma forma (Hubo problemas 
con la multiherencia por eso no se dejó una clase base de la que Instalacion y 
Juegos pudieran heredar al mismo tiempo, de dicha clase base y su respectiva 
entidad) A grandes rasgos todas implementan una funcion agregar_futuro_cliente 
que añade al cliente a una lista de los que estaran por llegar, la instalacion 
se preocupa de estar viendo quien de esta lista llego (en la funcion 
recibir_clientes) en caso de que llego los añade a la lista de gente en 
espera, a su vez tambien se encarga de ver en gente en espera quien puede entrar
 (comprobando si no se ha excedido el maximo de la instalacion) o quien ya lleva
 mucho tiempo esperando y lo saca . Finalmente ve en realizar accion ,aparte 
 de hacer el llamado a los dos metodos y en caso que la instalacion no 
 funcione se llama a revisar que vacia las lista, se ve si en atendiendo el 
 primero que entró cumplio el tiempo de duracion de la atención, en ese caso 
 se le aplican los efectos y se saca de la instlaacion.
"""


class Instalacion(Building):
    inst_id = 0

    def __init__(self,casino_pertenencia, tipo, costo, cap_max, pos_x=0, \
                                                                     pos_y=0):
        super().__init__(tipo, pos_x, pos_y)
        self.casino_pertenencia = casino_pertenencia
        self.instalacion_id = Instalacion.inst_id
        Instalacion.inst_id += 1
        self.tipo = tipo
        self.costo = costo
        self.gente_en_espera = deque()
        self.capacidad_maxima = cap_max
        self.personal_instalacion = list()
        self.funcionando = False
        self.tiempo_nfuncionando = 0
        self.por_llegar = list()
        self.atendiendo = deque()
        self.maximo_personal = None

    def sacar_a_cliente(self, cliente):
        cliente.tiempo = 0
        cliente.decision_tomada = None
        cliente.llega_a_objetivo = False
        cliente.destino = None
        cliente.duracion = 0
        cliente.tiempo_en_el_bano = 0

    def causar_efectos(self, cliente):
        self.sacar_a_cliente(cliente)
        cliente.dinero -= self.costo
        self.casino_pertenencia.dinero += self.costo

    def agregar_futuro_cliente(self, cliente):
        self.por_llegar.append(cliente)

    def recibir_clientes(self):
        """
        Se reciben a los que llegaron (Lo indica su atributo
        llega_a_objetivo) Y se añanden a la fila de espera si es que esta no
        supera su maximo
        """
        llegaron = filter(lambda x: x.llega_a_objetivo, self.por_llegar)
        for i in llegaron:
            llega = self.por_llegar.pop(self.por_llegar.index(i))
            if len(self.gente_en_espera) < MAXIMO_ESPERA:
                self.gente_en_espera.append(llega)
            else:
                self.sacar_a_cliente(llega)

    def atender_clientes(self):
        """
        Siempre se atendera de la primera persona que esta en la fila de espera
        """
        if len(self.atendiendo) < self.capacidad_maxima:
            if len(self.gente_en_espera) > 0:
                atender = self.gente_en_espera.popleft()
                atender.tiempo = 0  # Se reinicia su tiempo
                self.atendiendo.append(atender)
        se_van = filter(lambda x: x.tiempo > TIEMPO_ESPERA_INSTALACION,
                        self.gente_en_espera)
        for i in se_van:
            self.sacar_a_cliente(i)
        # Se actualiza la fila de espera
        self.gente_en_espera = deque(filter(lambda x: x.tiempo <=
                                                      TIEMPO_ESPERA_INSTALACION,
                                            self.gente_en_espera))

    def sacar_a_los_que_cambian_de_opinion(self):
        # Este metodo tendra algunas diferencias en cada sublclase, pero su
        # finaidad es quitar las personas que estan en la fila y tiene
        # decision None o destino None
        cambian_de_parecer = filter(lambda x: x.decision_tomada is None or
                                              x.destino is None,
                                    self.gente_en_espera)
        for i in cambian_de_parecer:
            self.sacar_a_cliente(i)
        self.gente_en_espera = deque(filter(lambda x: x.decision_tomada is not
                                                      None and x.destino is
                                                               not None,
                                            self.gente_en_espera))
        cambian_de_parecer = filter(lambda x: x.decision_tomada is None or
                                              x.destino is None,
                                    self.atendiendo)
        for i in cambian_de_parecer:
            self.sacar_a_cliente(i)
        self.atendiendo = deque(filter(lambda x: x.decision_tomada is not
                                                 None and x.destino is not
                                                        None, self.atendiendo))

    def revisar(self):
        # Este metodo se ajustara mas en cada subclase
        if not self.funcionando:
            for i in self.gente_en_espera:
                self.sacar_a_cliente(i)
            for i in self.atendiendo:
                self.sacar_a_cliente(i)
            self.atendiendo = deque()
            self.gente_en_espera = deque()

    def ejecutar_accion(self):
        # Este metodo se desarollara mas en cada subclase, según corresponda
        self.recibir_clientes()
        self.atender_clientes()
        self.sacar_a_los_que_cambian_de_opinion()

class Restobar(Instalacion):
    def __init__(self,casino, pos_x=0, pos_y=0):
        super().__init__(casino, "restobar", 2, 20, pos_x, pos_y)

    @property
    def tiempo_atencion(self):
        tiempo = max([600, int(uniform(600, 3000 // max([1, len(
            self.personal_instalacion)])))])
        return tiempo

    def causar_efectos(self, *args):
        super().causar_efectos(args[0])
        if args[1] == "bebida":
            args[0].lucidez = max([0, args[0].lucidez - 0.2])
            args[0].ansiedad = max([0, args[0].ansiedad - 0.15])
            args[0].p_retirarse = max([0, args[0].p_retirarse - 0.3])
        else:
            args[0].lucidez = min([1, args[0].lucidez + 0.1])
            args[0].ansiedad = max([0, args[0].ansiedad - 0.2])

    def revisar(self):
        # La clase Administracion se encarga de asignar el personal correcto
        # a cada instalacion, por lo que aqui solo se revisa si se cumple con
        #  el minimo de personal
        if len(self.personal_instalacion) >= 1:
            self.funcionando = True
        else:
            self.funcionando = False
        super().revisar()

    def ejecutar_accion(self):
        super().ejecutar_accion()
        self.revisar()
        if not self.funcionando:
            self.tiempo_nfuncionando += 1
        if len(self.atendiendo) > 0:
            if self.atendiendo[0].tiempo >= self.tiempo_atencion:
                atendido = self.atendiendo.popleft()
                if atendido.lucidez > atendido.ansiedad:  # Compra bebida -----
                    self.causar_efectos(atendido, "bebida")
                elif atendido.lucidez < atendido.ansiedad:  # Compra comida ----
                    self.causar_efectos(atendido, "comida")
                else:  # Eleccion al azar entre beibida y comida
                    elige = choice(["bebida", "comida"])
                    self.causar_efectos(atendido, elige)


class Tarot(Instalacion):
    def __init__(self, casino, pos_x=0, pos_y=0):
        super().__init__(casino, "tarot", 10, 1, pos_x, pos_y)
        self.maximo_personal = 1

    def causar_efectos(self, *args):
        super().causar_efectos(args[0])
        if args[1] == "retirarse":
            args[0].p_retirarse = min([1, args[0].p_retirarse + EFECTO_MR_T])
        else:
            args[0].p_suerte = min([1, args[0].suerte + EFECTO_MR_T])

    def revisar(self):
        if len(self.personal_instalacion) == 1:
            self.funcionando = True
        else:
            self.funcionando = False
        super().revisar()

    def ejecutar_accion(self):
        super().ejecutar_accion()
        self.revisar()
        if not self.funcionando:
            self.tiempo_nfuncionando += 1
        if len(self.atendiendo) > 0:
            if self.atendiendo[0].tiempo >= self.atendiendo[0].duracion:
                atendido = self.atendiendo.popleft()
                efecto = choice(["suerte", "retirarse"])
                self.causar_efectos(atendido, efecto)


class Bano(Instalacion):
    def __init__(self, casino, pos_x=0, pos_y=0):
        super().__init__(casino, "baños", 0.2, 20, pos_x, pos_y)

    def causar_efectos(self, cliente):
        super().causar_efectos(cliente)
        cliente.ansiedad = cliente.ansiedad - 0.1

    def ejecutar_accion(self):
        super().ejecutar_accion()
        if not self.funcionando:
            self.tiempo_nfuncionando += 1
        if len(self.atendiendo) > 0:
            terminaron = filter(lambda x: x.tiempo >= x.tiempo_en_el_bano,
                                self.atendiendo)
            for i in terminaron:
                self.causar_efectos(i)
            self.atendiendo = deque(filter(lambda x: x.tiempo <
                                                     x.tiempo_en_el_bano,
                                           self.atendiendo))



"""
Si bien no se define como una instalacion un espacio para conversar, 
se designa un espacio a donde iran todos los clientes que quieran hablar, 
de este modo se esta clase es la que se encarga de modificar los atributos y 
emparejar clientes, del mismo modo se designa una clase para TiniIlPadrino
"""


class EspacioConversa:
    def __init__(self):
        self.personas_hablando = list()
        self.personas_en_espera = deque()
        self.por_llegar = list()
        self.ancho = [400, 700]
        self.largo = [50, 150]

    def agregar_futuro_cliente(self, cliente):
        lugar_donde_espera = (int(uniform(*self.ancho)), int(uniform(
            *self.largo)))
        cliente.destino = lugar_donde_espera
        self.por_llegar.append(cliente)

    def recibir_personas(self):
        llegaron = filter(lambda x: x.llega_a_objetivo, self.por_llegar)
        for i in llegaron:
            llega = self.por_llegar.pop(self.por_llegar.index(i))
            self.agregar_persona(llega)

    def sacar_personas(self, persona):
        persona.tiempo = 0
        persona.destino = None
        persona.llega_a_objetivo = False
        persona.decision_tomada = None

    def agregar_persona(self, persona):
        if len(self.personas_en_espera) == 0:
            self.personas_en_espera.append(persona)
        else:
            persona_2 = self.personas_en_espera.popleft()
            duracion_conversa = max([persona.duracion_actividades,
                                     persona_2.duracion_actividades]) + \
                                persona_2.tiempo
            persona.tiempo = 0
            persona_2.tiempo = 0
            persona.destino = (persona_2.destino[0] + 10, persona_2.destino[1])
            self.personas_hablando.append(
                (persona_2, persona, duracion_conversa))

    def quitar_personas(self):
        if len(self.personas_en_espera) > 0:
            if self.personas_en_espera[0].tiempo >= TIEMPO_ESPERA_HABLA:
                se_va = self.personas_en_espera.popleft()
                self.sacar_personas(se_va)

    def causar_efectos(self, pareja_hablante):
        self.sacar_personas(pareja_hablante[0])
        pareja_hablante[0].ansiedad *= (1 - EFECTO_ANSIEDAD_CONVERSA)
        pareja_hablante[0].deshonestidad = min(1,
                                               pareja_hablante[
                                                   0].deshonestidad +
                                               EFECTO_DESHONESTIDAD_CONVERSA)
        pareja_hablante[0].amistades[pareja_hablante[1].persona_id] = \
            pareja_hablante[1]
        self.sacar_personas(pareja_hablante[1])
        pareja_hablante[1].ansiedad *= (1 - EFECTO_ANSIEDAD_CONVERSA)
        pareja_hablante[1].deshonestidad = min(1,
                                               pareja_hablante[
                                                   1].deshonestidad +
                                               EFECTO_DESHONESTIDAD_CONVERSA)
        pareja_hablante[1].amistades[pareja_hablante[0].persona_id] = \
            pareja_hablante[0]

    def sacar_a_los_que_cambian_de_opinion(self):
        cambian_de_parecer = filter(lambda x: x.decision_tomada is None or
                                              x.destino is None,
                                    self.personas_en_espera)
        for i in cambian_de_parecer:
            self.sacar_personas(i)
        self.personas_en_espera = list(filter(lambda x: x.decision_tomada is
                                                        not None and
                                                        x.destino is not None,
                                              self.personas_en_espera))

    def ejecutar_accion(self):
        self.recibir_personas()
        self.quitar_personas()
        terminaron = filter(lambda x: x[0].tiempo >= x[2],
                            self.personas_hablando)
        for i in terminaron:
            se_van = self.personas_hablando.pop(
                self.personas_hablando.index(i))
            self.causar_efectos(se_van)


class TiniIlPadrino:
    def __init__(self):
        self.x = 600
        self.y = 400
        self.cap_maxima = 5
        self.costo = 20
        self.por_llegar = list()
        self.atendiendo = list()

    def sacar_a_persona(self, persona):
        persona.decision_tomada = None
        persona.llega_a_objetivo = False
        persona.tiempo = 0
        persona.destino = None

    def causar_efectos(self, persona):
        self.sacar_a_persona(persona)
        persona.dinero -= self.costo
        persona.tini = True
        persona.p_retirarse += INFLUENCIA_TINI

    def agregar_futuro_cliente(self, persona):
        self.por_llegar.append(persona)

    def recibir_clientes(self):
        llegaron = filter(lambda x: x.llega_a_objetivo, self.por_llegar)
        for i in llegaron:
            if len(self.atendiendo) < self.cap_maxima:
                self.atendiendo.append(i)
            else:
                self.sacar_a_persona(i)
        self.por_llegar = deque(filter(lambda x: not x.llega_a_objetivo,
                                       self.por_llegar))

    def sacar_a_los_que_cambian_de_opinion(self):
        cambian_de_parecer = filter(lambda x: x.decision_tomada is None,
                                    self.por_llegar)
        for i in cambian_de_parecer:
            self.sacar_a_persona(i)
        self.por_llegar = list(filter(lambda x: x.decision_tomada is not
                                                None, self.por_llegar))
        cambian_de_parecer = filter(lambda x: x.decision_tomada is None,
                                    self.atendiendo)
        for i in cambian_de_parecer:
            self.sacar_a_persona(i)
        self.atendiendo = list(filter(lambda x: x.decision_tomada is not None,
                                      self.atendiendo))

    def ejecutar_accion(self):
        self.recibir_clientes()
        self.sacar_a_los_que_cambian_de_opinion()
        for i in self.atendiendo:
            if i.tiempo >= i.duracion_actividades:
                se_va = self.atendiendo.pop(self.atendiendo.index(i))
                self.causar_efectos(se_va)
