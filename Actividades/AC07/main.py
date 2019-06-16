from math import inf
from collections import deque

class Terreno:

    def __init__(self, nombre):
        self.nombre = nombre
        self.vecinos = set()

    def __repr__(self):
        return self.nombre

    def agregar_vecino(self, vecino):
        self.vecinos.add(vecino)

    def eliminar_vecino(self,vecino):
        self.vecinos.remove(vecino)

    def es_vecino(self,vecino):
        return vecino in self.vecinos


    def __eq__(self, other):
        return self.nombre == other



class Ciudad:

    def __init__(self, path):
        self.nodos = dict()
        with open(path) as archivo:
            for terreno in archivo:
                terr, vecinos = terreno.strip().split(":")
                self.nodos[terr] = Terreno(terr)
                for i in vecinos.split(","):
                        self.agregar_calle(terr.strip(),i.strip())

    def agregar_calle(self, origen, destino):
        if origen not in self.nodos:
            self.nodos[origen] = Terreno(origen)
        if destino not in self.nodos:
            self.nodos[destino] = Terreno(destino)
        if origen == destino:  # Si el origen es igual al destino no se hace
            # nada
            return None
        if destino not in self.nodos[origen].vecinos:
            self.nodos[origen].agregar_vecino(destino)

    def eliminar_calle(self, origen, destino):
        if origen not in self.nodos or destino not in self.nodos:
            return tuple()
        if destino not in self.nodos[origen].vecinos:
            return tuple()
        self.nodos[origen].eliminar_vecino(destino)
        return (origen, destino)

    @property
    def terrenos(self):
        return {i for i in self.nodos.keys()}

    @property
    def calles(self):
        conjunto_de_calles = set()
        for i in self.nodos:
            for j in self.nodos[i].vecinos:
                conjunto_de_calles.add((i,j))
        return conjunto_de_calles

    def verificar_ruta(self, ruta):
        if ruta == []:
            return True
        if len(ruta) == 1:
            return ruta[0] in self.nodos
        if ruta[0] in self.nodos and ruta[1] in self.nodos:
            if self.nodos[ruta[0]].es_vecino(self.nodos[ruta[1]]):
                return True and self.verificar_ruta(ruta[1:])
        else:
            return False

    def entregar_ruta(self, origen, destino,visitados=list(), ruta=list()):
        if origen not in self.nodos or destino not in self.nodos:
            return []
        if origen == destino:
            if len(ruta) == 0:
                return [origen]
            return ruta
        if origen in visitados:
            return ruta
        visitados.append(origen)
        ruta.append(origen)
        for i in self.nodos[origen].vecinos:
            resultado = self.entregar_ruta(i, destino, visitados, ruta)
            if resultado is not None:
                return resultado
            if len(ruta) > 0:
                ruta.pop(-1)
        return ruta



    def ruta_corta(self, origen, destino):
        pass


    def ruta_entre_bombas(self, origen, *destinos):
        if origen not in self.nodos:
            return []
        if len(destinos) == 0:
            return [origen]
        for i in destinos:
            if i not in self.nodos:
                return []
        inicio = 0
        fin = 1
        total = [origen] + destinos
        respuesta = []
        while fin < len(total) - 1:
            camino_a_b = self.entregar_ruta(total[inicio], total[fin])
            if len(camino_a_b) == 0:
                return []
            respuesta += camino_a_b
            inicio +=1
            fin+=1
        return respuesta



    def ruta_corta_entre_bombas(self, origen, *destinos):
        pass




if __name__ == '__main__':
    grafo = Ciudad("facil.txt")
    print(grafo.entregar_ruta("A","D"))
