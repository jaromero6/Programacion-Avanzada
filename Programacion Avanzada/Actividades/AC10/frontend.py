import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QObject, pyqtSignal, Qt
from backend import UserChecker, Character, Fruit


class FirstWindow(QWidget):  # Es la primera ventana
    check_name_signal = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 300, 300)
        self.name_label = QLabel('Ingrese nombre', self)
        self.line_input = QLineEdit("", self)
        self.start_game_button = QPushButton('Inicio', self)
        self.start_game_button.clicked.connect(self.check_function)
        self.user_checker = UserChecker(self)
        #self.check_name_signal.connect(self.user_checker.check)

        vbox = QVBoxLayout()
        vbox.addWidget(self.name_label) # Label que pide nombre
        vbox.addWidget(self.line_input) # Espacio para ingresar el nombre
        vbox.addWidget(self.start_game_button)
        self.setLayout(vbox)

    def check_function(self):
        name = self.line_input.text()
        self.user_checker.check(name)  # Se verifica si el nombre es correcto

    def open_Window(self, state):
        if state:
            self.hide()
            self.maingame = MainGame()
            self.maingame.show()
        else:
            self.name_label.setText("Nombre ingresado no valido")

class MainGame(QWidget):
    move_character = pyqtSignal(str)
    appear_new_fruit = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 550, 603)
        self._frame = 0
        # Fondo de pantalla
        self.background= QLabel(self)
        self.background.setPixmap(QPixmap("sprites/map.png"))
        # Personaje
        self.backend_character = Character(self)
        self.move_character.connect(self.backend_character.move)
        self.front_character = QLabel(self)
        self.front_character.setPixmap(QPixmap('sprites/pacman_D_1.png'))


    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        if value > 3:
            self._frame = 1
        else:
            self._frame = value

    def keyPressEvent(self, e):
        self.frame += 1
        if e.key() == Qt.Key_Right:
            self.front_character.setPixmap(
                QPixmap(f'sprites/pacman_D_{self.frame}.png'))
            self.move_character.emit('R')
        if e.key() == Qt.Key_Left:
            self.front_character.setPixmap(
                QPixmap(f'sprites/pacman_L_{self.frame}.png'))
            self.move_character.emit('L')
        if e.key() == Qt.Key_Up:
            self.front_character.setPixmap(
                QPixmap(f'sprites/pacman_U_{self.frame}.png'))
            self.move_character.emit('U')
        if e.key() == Qt.Key_Down:
            self.front_character.setPixmap(
                QPixmap(f'sprites/pacman_D_{self.frame}.png'))
            self.move_character.emit('D')
        if e.key() == Qt.Key_Space:
           self.appear_new_fruit.emit(self.fruit.add_new_fruit_to_map())

    def new_position(self, event):
        self.front_character.move(event['x'], event['y'])

    def show_new_fruit(self, new_pos):
        fruit = QLabel(self)
        fruit.setPixmap(QPixmap("sprites/cherry.png"))




app = QApplication([])
form = FirstWindow()
try:
    form.show()
except Exception as err:
    print(err)

sys.exit(app.exec_())