from random import randint

from PyQt5.QtCore import QObject, pyqtSignal, Qt

# Acá va lo relacionado con el procesamiento de datos
class UserChecker(QObject):
    # Chequea la parte del login del usuario
    check_signal = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__()
        self.check_signal.connect(parent.open_Window)

    def check(self, name:str):
        """
        Funcion que chequea si name (del usuario) no supera los 6 caracteres
        y solo está formado por letras
        :param name:
        :return: none
        """
        letters = "abcdefghijklmnopqrstuvwxyz"
        correct_name = True
        if len(name) <= 6:
            for i in name:
                if i.lower() not in letters:
                    correct_name = False
        else:
            correct_name = False
        self.check_signal.emit(correct_name)


class Character(QObject):
    new_position_signal = pyqtSignal(dict)
    def __init__(self, parent, x=13, y=8):
        super().__init__()
        self.direction = "R"
        self._x = x
        self._y = y
        self.new_position_signal.connect(parent.new_position)

    # Properties de posicion del personaje

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if 8 <= value <= 603:
            self._y = value
            self.new_position_signal.emit({'x': self.x, 'y': self.y})

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if 13 <= value <= 550:
            self._x = value
            self.new_position_signal.emit({'x': self.x, 'y': self.y})

    def move(self, event):
        """
        Recibe 4 posibles eventos : U(Arriba), D(Abajo), L(Izquierda),
        R(Derecha), en cada caso realiza la accion correspondiente
        :param event:
        :return:
        """
        if event == "R":
            self.x += 10
            self.direction = "R"
        if event == "L":
            self.x -= 10
            self.direction = "L"
        if event == "U":
            self.y -= 10
            self.direction = "U"
        if event == "D":
            self.y += 10
            self.direction = "D"


class Fruit:
    appear_signal = pyqtSignal(tuple)
    def __init__(self, parent):
        self.appear_signal.connect(parent.appear_fruit)
        self.list_fruit = list()

    def add_new_fruit_to_map(self, event):
        x = randint(13, 550)
        y = randint(8, 603)
        return (x, y)
