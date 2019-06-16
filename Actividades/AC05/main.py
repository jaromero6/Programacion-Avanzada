# Aqui abajo debes escribir el código de tus clases
from abc import ABC,abstractmethod
class Personaje(ABC):
    def __init__(self, *args, **kwargs):
        self.nombre = args[0]
        self.fuerza = args[1]
        self.resistencia = args[2]
        if args[3] >= 0:
            self.vida = args[3]
        else:
            self.vida = 0
        self.ki = args[4]


    @abstractmethod
    def atacar(self, enemigo,perdida_de_vida):
        if perdida_de_vida < 0:  # Supuesto: Si perdida_de_vida < 0 entonces
            # se toma la parte positiva pero disminuida 5 veces
            perdida_de_vida = abs(perdida_de_vida)/10
        if enemigo.vida - perdida_de_vida > 0:
            enemigo.vida -= perdida_de_vida
            print(self.nombre, "le quita", perdida_de_vida, "a", enemigo.nombre)
        else:

            print(self.nombre,"le quita",enemigo.vida,"a",enemigo.nombre)
            print(enemigo.nombre,"ha muerto")
            enemigo.vida = 0

    def perder_ki(self, perdida):
        self.ki = self.ki * perdida
        return self.ki


class Humano(Personaje):
    def __init__(self,*args,inteligencia=100):
        super().__init__(*args)
        self.inteligencia = inteligencia

    def atacar(self, enemigo,perdida_de_vida=0):
        perdida_de_vida = self.ki*((1+self.fuerza - enemigo.fuerza)/2)
        super().atacar(enemigo,perdida_de_vida)

    def meditar(self):
        self.ki += (self.inteligencia/100)
        print("Yo",self.nombre,"estoy meditando")


class Extraterrestre(Personaje):
    def __init__(self,*args,**kwargs):
        super().__init__(*args)

    def atacar(self, enemigo):
        perdida_de_vida = self.ki*(1 + self.fuerza - enemigo.resistencia)
        self.fuerza = self.fuerza*1.3
        super().atacar(enemigo,perdida_de_vida)

class Suypersaiyayin(Extraterrestre, Humano):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.cola = True

    def perder_cola(self):
        if self.cola:
            self.cola = False
            self.resistencia = self.resistencia*0.4
            print(self.nombre,"perdio la cola")


class Hakashi(Extraterrestre):
    def __init__(self,*args):
        super().__init__(*args)

    def robar_ki(self,*adversarios):
        print(self.nombre,"ha robado ki")
        self.ki += sum([x.perder_ki(0.5) for x in adversarios])

if __name__ == '__main__':
    """
    A continuación debes instanciar cada uno de los objetos pedidos,
    para que puedas simular la batalla.
    """
    krilin = Humano("Krilin",10,10,10,10)
    goku = Suypersaiyayin("Goku",50,50,50,50,50)
    vegeta = Suypersaiyayin("Vegeta",50,50,50,50)
    bill = Hakashi("Bill",100,100,100,100)
    champa = Hakashi("Champa",100,100,100,100)
    bill.robar_ki(goku,vegeta)
    goku.perder_cola()
    vegeta.perder_cola()
    champa.robar_ki(krilin)
    krilin.meditar()
    krilin.atacar(bill)
    bill.atacar(krilin)
    # Goku se hace la genkidama
    goku.meditar()
    goku.meditar()
    goku.meditar()
    goku.meditar()
    vegeta.atacar(champa)
    vegeta.atacar(champa)
    goku.atacar(champa)
    goku.atacar(bill)
    vegeta.atacar(bill)



