from PyQt5.QtCore import QObject, pyqtSignal, QPoint, QRect, QSize, QTimer
from threading import Thread
from time import sleep


class PowerUp(QObject):

    id_class = 0
    dissapear_signal = pyqtSignal(int)

    def __init__(self, pos_x, pos_y, type_power,parent):
        super().__init__()
        self.id_power = PowerUp.id_class
        PowerUp.id_class += 1
        self.type_power = type_power
        self.rect = QRect(QPoint(pos_x + 250, pos_y + 20), QSize(20, 20))
        self.dissapear_signal.connect(parent.dissapear_power_up)
        self.own_timer = QTimer(self)
        self.time = 0
        self.is_alive = True
        self.time_effect = None
        self.own_timer = Thread(target=self.appear)
        self.own_timer.start()


    def appear(self):
        while self.time <= 6 and self.is_alive:
            self.time += 1
            sleep(1)
        if self.is_alive:
            self.dissapear_signal.emit(self.id_power)
