import threading
import time
from itertools import chain
from random import randint

NebilLockBottom = threading.Event()
HayGanador = threading.Event()
NebilLockBottom.set()
global_lock = threading.Lock()


class Equipo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.hacker = Hacker(self)
        self.cracker = Cracker(self)

    def es_ganador(self):
        if self.cracker.termino and self.hacker.termino:
            print(f"{self.nombre} ha terminado, es el equipo ganador")
            HayGanador.set()  # Avisan que terminaron

    def administrar_equipos(self):
        th1 = threading.Thread(target=self.hacker.escribir_lineas, daemon=True)
        th2 = threading.Thread(target=self.cracker.escribir, daemon=True)
        th1.start()
        th2.start()


class Hacker:
    def __init__(self, equipo):
        self.equipo = equipo
        self.tiempo = randint(4, 13)
        self.termino = False

    def escribir_lineas(self):
        time.sleep(self.tiempo)  # Se espera el tiempo necesario
        with global_lock:
            desencriptar("pista.txt")
        print(f"Hacker de {self.equipo.nombre} ha terminado")
        self.termino = True  # Indica que ya terminó
        self.equipo.es_ganador()  # Se ve si termino


class Cracker:
    def __init__(self, equipo):
        self.equipo = equipo
        self.velocidad = randint(5, 15)
        self.lineas_escritas = 0
        self.termino = False

    @property
    def total_lineas(self):
        return self.lineas_escritas

    @total_lineas.setter
    def total_lineas(self, valor):
        self.lineas_escritas = min([50, valor])

    def escribir(self):
        while self.total_lineas < 50:
            time.sleep(1)
            sufre_ataque = randint(0, 101)
            if sufre_ataque <= 20:  # 20% de probabilidad de sufrir ataque
                with global_lock:
                    print(f"Cracker de equipo {self.equipo.nombre} ha sido atacado")
                    NebilLockBottom.wait()  # Espera a que lo desbloquee
                    print(f"NebilLockBottom inicia ayuda a equipo {self.equipo.nombre}")
                    time.sleep(randint(1, 4)) # Tiempo que se deomora en desbloquearlo
                    NebilLockBottom.set()  # Deja disponible nuebamente a NebilBottom
                    print(f"NebilLockBottom termina ayudar a equipo {self.equipo.nombre}")
            self.total_lineas += self.velocidad

        print(f"Cracker de {self.equipo.nombre} ha terminado")
        self.termino = True
        self.equipo.es_ganador() # Se ve si ya terminó


class Mision:
    def __init__(self):
        # Se añaden los equipos a la simulacion
        self.eq_1 = Equipo("Equipo 1")
        self.eq_2 = Equipo("Equipo 2")
        self.eq_3 = Equipo("Equipo 3")
        self.lista_equipos = [self.eq_1, self.eq_2, self.eq_3]

    def mostrar_resultados(self):
        for i in self.lista_equipos:
            print(f"{i.nombre}:")
            print(f"Termino Hacker: {i.hacker.termino}")
            print(f"Lineas Cracker: {i.cracker.total_lineas}")

    def run(self):
        HayGanador.wait()  # Espera a que exista un ganador
        self.mostrar_resultados() # Una vez que hay uno muestra los resultados
        HayGanador.set()
        exit()


def desencriptar(nombre_archivo):
    """
    Esta simple (pero útil) función te permite descifrar un archivo encriptado.
    Dado el path de un archivo, devuelve un string del contenido desencriptado.
    """

    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        murcielago, numeros = "murcielago", "0123456789"
        dic = dict(chain(zip(murcielago, numeros), zip(numeros, murcielago)))
        return "".join(
            dic.get(char, char) for linea in archivo for char in linea.lower())


if __name__ == "__main__":
    mision = Mision()
    # Los threadings de equipos
    th_eq_1 = threading.Thread(target=mision.eq_1.administrar_equipos,
                               daemon=True)
    th_eq_2 = threading.Thread(target=mision.eq_2.administrar_equipos, daemon=True)
    th_eq_3 = threading.Thread(target=mision.eq_3.administrar_equipos,
                               daemon=True)
    # Se ejecuta el threading principal
    th_main = threading.Thread(target=mision.run)
    th_eq_1.start()
    th_eq_2.start()
    th_eq_3.start()
    th_main.start()

