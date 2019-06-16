from clientes import Persona
from juegos import Ruleta, Tragamonedas
from instalaciones import Restobar, Tarot, Bano, EspacioConversa, TiniIlPadrino
from personal import Bartender, MrT, Dealer, Administracion
from parameters import N_PERSONAS, DINERO_INICIAL
from names import get_full_name
from random import randint
import gui

class Casino:
    def __init__(self, monto_inicial, total):
        self.tiempo_total_simulacion = 86400 * total
        self.dinero = monto_inicial
        self.dinero_al_iniciar_el_dia = monto_inicial
        self.dinero_perdido_ganado = list()
        self.mundo = dict()
        self.personal = dict()
        self.instalaciones = list()
        self.lugar_de_habla = None
        self.lugar_de_tini = None
        self.juegos = list()
        self.administracion = None
        self.ganancias_diarias = list()
        self.tiempo_segundos = 0

    @property
    def tarots(self):
        return list(filter(lambda x: x.tipo == "tarot", self.instalaciones))

    @property
    def restobars(self):
        return list(filter(lambda x: x.tipo == "restobar", self.instalaciones))

    @property
    def banos(self):
        return list(filter(lambda x: x.tipo == "baños", self.instalaciones))

    @property
    def ruletas(self):
        return list(filter(lambda x: x.tipo == "ruleta", self.juegos))

    @property
    def tragamonedas(self):
        return list(filter(lambda x: x.tipo == "tragamonedas", self.juegos))

    @property
    def dealers(self):
        return list(filter(lambda x: x.tipo ==
                                     "dealer", self.personal.values()))

    @property
    def bartenders(self):
        return list(filter(lambda x: x.tipo == "bartender",
                           self.personal.values()))

    @property
    def mrts(self):
        return list(filter(lambda x: x.tipo == "mr_t", self.personal.values()))

    def disponer_tragamonedas(self):
        for j in [75, 150]:
            for i in range(100, 351, 50):
                tragamon = Tragamonedas(self, j, i)
                self.juegos.append(tragamon)
                gui.add_entity(tragamon)

    def disponer_ruletas(self):
        for j in [225, 300]:
            for i in range(100, 351, 50):
                ruleta = Ruleta(self, j, i)
                self.juegos.append(ruleta)
                gui.add_entity(ruleta)

    def agregar_espacios(self):
        self.lugar_de_habla = EspacioConversa()
        self.lugar_de_tini = TiniIlPadrino()

    def agregar_instalaciones(self):
        # Se añaden los restobars
        for j in [200, 250]:
            for i in range(400, 626, 75):
                res_1 = Restobar(self,i, j)
                self.instalaciones.append(res_1)
                gui.add_entity(res_1)
        # Se agregan los baños
        for i in range(200, 401, 25):
            ban_1 = Bano(self, 720, i)
            self.instalaciones.append(ban_1)
            gui.add_entity(ban_1)

        # Se agregan los tarots
        res_1 = Tarot(self, 475, 300)
        self.instalaciones.append(res_1)
        gui.add_entity(res_1)

    def cargar_personas(self):
        for i in range(N_PERSONAS):
            nombre = get_full_name()
            edad = randint(18, 66)
            nueva_persona = Persona(edad, nombre, 25, -40)
            self.mundo[nueva_persona.persona_id] = nueva_persona
            gui.add_entity(nueva_persona)

    def cargar_personal(self):
        for i in range(55):
            nombre = get_full_name()
            edad = randint(21,66)
            nuevo_bartender = Bartender(nombre, edad)
            self.personal[nuevo_bartender.id_personal] = nuevo_bartender
        for i in range(62):
            nombre = get_full_name()
            edad = randint(21, 66)
            nuevo_dealer = Dealer(nombre, edad)
            self.personal[nuevo_dealer.id_personal] = nuevo_dealer
        for i in range(3):
            nombre = get_full_name()
            edad = randint(21, 66)
            nuevo_mrt = MrT(nombre, edad)
            self.personal[nuevo_mrt.id_personal] = nuevo_mrt

    def iniciar_casino(self):
        self.disponer_tragamonedas()
        self.disponer_ruletas()
        self.agregar_espacios()
        self.agregar_instalaciones()
        self.cargar_personal()
        self.cargar_personas()
        self.administracion = Administracion(self.tarots, self.restobars,
                                             self.ruletas, self.tragamonedas,
                                             self.mrts,
                                             self.bartenders, self.dealers)

    def ganancia_promedio_por_persona(self):
        print("----------------------------------------------------")
        print("Ganancias promedio por persona:\n")
        total = 0
        for i in self.mundo.values():
            total += (i.dinero - i.monto_inicial)
        res = total / max([1, len(self.mundo)])
        print(res)
        with open("estadisticas.txt", "w", encoding="utf-8") as archivo:
            archivo.write("Resultados -------------------------- \n")
            archivo.write("Ganancia promedio por persona")
            archivo.write(str(res) + "\n")

    def ganancia_promedio_por_personalidad(self):
        print("---------------------------------------------------------------")
        print("Ganancias promedio por tipo de personalidad")
        personalidades = {"ludopata": [], "kibitzer": [], "millonario": [],
                          "dieciochero": [], "ganador": []}
        for i in self.mundo.values():
            personalidades[i.personality].append(i.dinero - i.monto_inicial)
        with open("estadisticas.txt", "a", encoding="utf-8") as archivo:
            archivo.write("Ganancia promedio por personalidad:\n")
            for i, j in personalidades.items():
                res = i + ":" +  str(sum(j) / max([1, len(personalidades[
                                                              i])]))
                print(res)
                archivo.write(res + "\n")

    def tiempo_estadia_promedio_por_persona(self):
        print("--------------------------------------------------------")
        print("Tiempo promedio por persona")
        total = 0
        for i in self.mundo.values():
            total += i.tiempo_total
        res = total / max([1, len(self.mundo)])
        print(res, "segundos")
        with open("estadisticas.txt", "a", encoding="utf-8") as archivo:
            archivo.write("Tiempo promedio por persona:\n")
            archivo.write(str(res) + " segundos\n")

    def tiempo_estadia_promedio_por_personalidad(self):
        print("----------------------------------------------------------")
        print("Tiempo promedio por personaldiad")
        personalidades = {"ludopata": [], "kibitzer": [], "millonario": [],
                          "dieciochero": [], "ganador": []}
        for i in self.mundo.values():
            personalidades[i.personality].append(i.tiempo_total)
        with open("estadisticas.txt", "a", encoding="utf-8") as archivo:
            archivo.write("Tiempo promedio por personalidad\n")
            for i, j in personalidades.items():
                resul = i +  ":" + str(sum(j) / max([1, len(personalidades[
                                                            i])])) + " segundos"
                archivo.write(resul + "\n")
                print(resul)


    def ganancias_promedio_diarias(self):
        print("---------------------------------------------------------------")
        print("Ganancias diarias:")
        res = sum(self.ganancias_diarias) / max([1,len(self.ganancias_diarias)])
        print(res)
        with open("estadisticas.txt", "a", encoding="utf-8") as archivo:
            archivo.write("Ganancias en promedio diarias:\n")
            archivo.write(str(res) + "\n")

    def juego_que_genero_mas_ganancias(self):
        print("--------------------------------------------------------------")
        print("Juego que genero mas ganacias en relacion al dinero que perdio")
        gana = sorted(self.juegos, key=lambda x: (x.dinero_ganado_total /
                                                    max([1,
                                                x.dinero_perdido_total])),
                      reverse=True)[0]
        print("Tipo:", gana.tipo)
        print("Id:", gana.juegos_id)
        print("Razon de ganancias (Ganancia / Perdida):",
              (gana.dinero_ganado_total / max([1,
                                                gana.dinero_perdido_total])))
        with open("estadisticas.txt", "a", encoding="utf-8") as archivo:
            archivo.write("Juego que generó más ganancias:\n")
            archivo.write("Tipo: " + str(gana.tipo) + "\n")
            archivo.write("Id: " + str(gana.juegos_id) + "\n")
            archivo.write("Raxon de ganancias: " +
                          str(gana.dinero_ganado_total / max([1,
                                                gana.dinero_perdido_total]))
                          + "\n")
    def porcentaje_gente_que_conto_cartas(self):
        print("-------------------------------------------------------------")
        print("Porcentaje de gente que hizo trampa")
        total_hicieron_trampa = list(filter(lambda x:
                                            x.hizo_trampa_alguna_vez,
                                            self.mundo.values()))
        print("Porcentaje: ", 100 * len(total_hicieron_trampa) / len(
            self.mundo),
              "%")
        with open("estadisticas.txt", "a", encoding="utf-8") as archivo:
            archivo.write("Porcentaje de gente que contó cartas:\n")
            archivo.write("Porcentaje: "+ str(100 * len(
                total_hicieron_trampa) / len(
            self.mundo)) + "\n")

    def razones_de_salida_del_casino(self):
        print("-------------------------------------------------------------")
        print("Razones de salida (Razon de salida / Razones totales de salida)")
        razones_salidas = {"personales": 0, "dinero": 0, "trampa": 0}
        for i in self.mundo.values():
            for j in razones_salidas:
                razones_salidas[j] += i.razones_salida[j]
        with open("estadisticas.txt", "a", encoding="utf-8") as archivo:
            archivo.write("Razones de salida del casino\n")
            for i, j in razones_salidas.items():
                res = i +  ":" +  str(j / max([1, sum(razones_salidas.values(
                ))]))
                archivo.write(res + "\n")
                print(res)

    def tiempo_total_sin_funcionar(self):
        print("---------------------------------------------------------------")
        print("Tiempo total sin funcionar de cada instalacion")
        with open("estadisticas.txt", "a", encoding="utf-8") as archivo:
            archivo.write("Tiempo sin funcionar de cada instalacion\n")
            for i in self.instalaciones:
                tip = "Tipo:" +  str(i.tipo)
                id_ = "Id:" + str(i.instalacion_id)
                tiempo = "Iiempo sin funcionar: " + str(
                      i.tiempo_nfuncionando) + " segundos"
                archivo.write(tip + "\n")
                archivo.write(id_ + "\n")
                archivo.write(tiempo + "\n")
                print(tip)
                print(id_)
                print(tiempo)
            for i in self.juegos:
                tip = "Tipo:" + str(i.tipo)
                id_ = "Id:" + str(i.juegos_id)
                tiempo = "Iiempo sin funcionar: " + str(
                    i.tiempo_nfuncionando) + " segundos"
                archivo.write(tip + "\n")
                archivo.write(id_ + "\n")
                archivo.write(tiempo + "\n")
                print(tip)
                print(id_)
                print(tiempo)

    def numero_de_personas_que_visito_cada_juego(self):
        print("--------------------------------------------------------------")
        print("Numero total de visitas a cada juego")
        print("ruleta:", sum([ i.total_visitas for i in self.ruletas]),
              "visitas")
        print("tragamonedas:",sum([i.total_visitas for i in
                                   self.tragamonedas]), "visitas")
        with open("estadisticas.txt", "a", encoding="utf-8") as archivo:
            archivo.write("Numero total de visitas por juego\n")
            archivo.write("ruleta: " +  str(sum([i.total_visitas for i in
                                          self.ruletas])) +
             "visitas"+ "\n")
            archivo.write("tragamonedas: " + str(sum([i.total_visitas for i in
                                                self.tragamonedas])) +
                          "visitas" + "\n")

    def mostrar_estadisticas(self):
        self.ganancia_promedio_por_persona()
        self.ganancia_promedio_por_personalidad()
        self.tiempo_estadia_promedio_por_persona()
        self.tiempo_estadia_promedio_por_personalidad()
        self.ganancias_promedio_diarias()
        self.juego_que_genero_mas_ganancias()
        self.porcentaje_gente_que_conto_cartas()
        self.razones_de_salida_del_casino()
        self.tiempo_total_sin_funcionar()
        self.numero_de_personas_que_visito_cada_juego()

    def tick_simulacion(self):
        self.administracion.tick_de_instalaciones()
        for i in self.banos:
            if not i.funcionando:
                i.funcionando = True
            else:
                i.ejecutar_accion()
        self.lugar_de_habla.ejecutar_accion()
        self.lugar_de_tini.ejecutar_accion()
        for i in self.mundo:
            self.mundo[i].ejecutar_accion(self.ruletas, self.tragamonedas,
                                          self.tarots, self.restobars,
                                          self.banos, self.lugar_de_habla,
                                          self.lugar_de_tini)
            if self.tiempo_segundos == 86400:
                self.ganancias_diarias.append(self.dinero -
                                             self.dinero_al_iniciar_el_dia)
                self.tiempo_segundos = 0
                self.dinero_al_iniciar_el_dia = self.dinero
            if len(self.ganancias_diarias) == self.tiempo_total_simulacion //\
                    86400:
                self.mostrar_estadisticas()
                exit()
        self.tiempo_segundos += 1


def pedir_numero_de_dias():
    print("Ingresar numero de dias que dura la simulacion")
    duracion = input()
    if not duracion.isdigit():
       return  pedir_numero_de_dias()
    return int(duracion)


def realizar_simulacion():
    duracion = pedir_numero_de_dias()
    gui.init()
    casino = Casino(DINERO_INICIAL, duracion)
    casino.iniciar_casino()
    gui.run(casino.tick_simulacion, 100/16)

