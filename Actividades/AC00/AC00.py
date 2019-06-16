import math

class Circulo:
    def __init__(self,radio,centro):
        self.radio = radio # int
        self.centro = centro # Ingresa como lista


    def __str__(self):
        return "Centro: "+ str(self.centro[0])+" , "+str(self.centro[1]) + "  Radio: "+str(self.radio)


    def obtener_area(self):
        return math.pi*(self.radio**2)

    def obtener_permietro(self):
        return math.pi*2*self.radio


class Rectangulo:
    def __init__(self,vertice_1,vertice_2,vertice_3,vertice_4):
        # Cada uno sera una lista
        self.vertice_1 = vertice_1
        self.vertice_2 = vertice_2
        self.vertice_3 = vertice_3
        self.vertice_4 = vertice_4


    def obtener_area(self):
        largo = abs(self.vertice_1[0] - self.vertice_2[0])
        if abs(self.vertice_1[0] - self.vertice_3[0])>largo:
            largo = abs(self.vertice_1[0] - self.vertice_3[0])
        ancho = abs(self.vertice_1[1] - self.vertice_2[1])
        if abs(self.vertice_1[1] - self.vertice_3[1])>ancho:
            ancho = abs(self.vertice_1[1] - self.vertice_3[1])
        return largo*ancho

    def obtener_perimetro(self):
        largo = abs(self.vertice_1[0] - self.vertice_2[0])
        if abs(self.vertice_1[0] - self.vertice_3[0]) > largo:
            largo = abs(self.vertice_1[0] - self.vertice_3[0])
        ancho = abs(self.vertice_1[1] - self.vertice_2[1])
        if abs(self.vertice_1[1] - self.vertice_3[1]) > ancho:
            ancho = abs(self.vertice_1[1] - self.vertice_3[1])
        return 2*(largo + ancho)

    def es_cuadrado(self): # Retorna True si es un cuadrado
        largo = abs(self.vertice_1[0] - self.vertice_2[0])
        if abs(self.vertice_1[0] - self.vertice_3[0]) > largo:
            largo = abs(self.vertice_1[0] - self.vertice_3[0])
        ancho = abs(self.vertice_1[1] - self.vertice_2[1])
        if abs(self.vertice_1[1] - self.vertice_3[1]) > ancho:
            ancho = abs(self.vertice_1[1] - self.vertice_3[1])
        return ancho == largo
rectangulo = Rectangulo([3,4],[0,3],[0,4],[0,0])
circulo = Circulo(10,[10,10])