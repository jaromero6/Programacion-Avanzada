from PyQt5.QtCore import QObject, pyqtSignal, QRect, QPoint, QSize
from math import cos, sin, tau
from threading import Thread, Lock
from time import sleep

HIGHT = 641
WIDTH = 1041

power_lock = Lock()


class Character(QObject):
    move_signal = pyqtSignal(tuple)
    collision_signal = pyqtSignal(str)
    clean_signal = pyqtSignal(bool)
    invert_key_signal = pyqtSignal(bool)
    trio_signal = pyqtSignal(str)
    atraviessa_signal = pyqtSignal(bool)
    add_nebcoin_signal = pyqtSignal(str)

    def __init__(self, name, x, y, color,
                 speed, own_color, drawing_time, not_drawing_time, parent):
        super().__init__()
        self.name = name
        self.color = color
        self.own_color = own_color  # Es el color del cliente desde donde se
        # ejecuta
        self.speed = speed
        self._x = x
        self._y = y
        self.current_x = x
        self.current_y = y
        self._angle = 0
        self.x_direction = 1
        self.y_direction = 0
        self.drawing = True
        self.rects = list()
        self.head_rects = {"blue": None, "red": None, "green": None,
                           "yellow": None}
        self.sprite_rect = None
        self.is_alive = True
        self.drawing_time = drawing_time
        self.not_drawing_time = not_drawing_time
        self._time = 0
        self.pause = False
        self.continue_game = True
        self.turning = False
        self.current_direction = None
        self.move_signal.connect(parent.update_positions)
        self.clean_signal.connect(parent.clean_map)
        self.invert_key_signal.connect(parent.invert_key)
        self.trio_signal.connect(parent.request_trio_power)
        self.atraviessa_signal.connect(parent.apply_atraviessa_effect)
        self.collision_signal.connect(parent.collision)
        self.add_nebcoin_signal.connect(parent.add_nebcoin)
        self.is_sinrastro_effect = False
        self.sinrastro_threads = 0
        self.is_tau_effect = False
        self.is_atraviessa_effect = False

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        if not 4 < self.x < WIDTH - 4:
            if not self.is_atraviessa_effect:
                self.collision_signal.emit(self.name)
                self.is_alive = False
            else:
                if self.x < 4:
                    self._x = WIDTH
                    self.current_x = WIDTH - 4
                else:
                    self._x = 9
                    self.current_x = 4

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        if not 4 < self.y < HIGHT - 5:
            if not self.is_atraviessa_effect:
                self.collision_signal.emit(self.name)
                self.is_alive = False
            else:
                if self._y < 4:
                    self._y = HIGHT - 5
                    self.current_y = HIGHT - 90
                else:
                    self._y = 9
                    self.current_y = 4

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value
        if self.drawing and self.time > self.drawing_time:
            self._time = 0
            self.drawing = False

        elif not self.drawing and self.time > self.not_drawing_time:
            self._time = 0
            self.drawing = True
        if self.is_sinrastro_effect:
            self.drawing = False

    @property
    def front_point(self):
        return (self.x + (12 * self.x_direction),
                self.y + (12 * self.y_direction))

    @property
    def head(self):
        return QRect(QPoint(self.x + 250, self.y + 20), QSize(2.5, 2.5))

    def change_direction(self, direction):

        if not self.is_tau_effect:
            if direction == "l":
                self.turning =True
                self.angle -= 0.05 * (self.speed / 2)  # Esto es para ajustar el
                # angulo conforme se mueve más rápido
            elif direction == "r":
                self.turning = True
                self.angle += 0.05 * (self.speed / 2)
        else:
            if direction == "l":
                self.turning = True
                self.angle -= (tau / 4)
            elif direction == "r":
                self.turning = True
                self.angle += (tau / 4)
        self.current_direction = direction
        self.x_direction = cos(self.angle)
        self.y_direction = sin(self.angle)

    def stop_turn(self):
        self.turning = False
        self.current_direction = None

    def move_tick(self):
        if self.continue_game and not self.pause:
            if self.is_alive:
                if self.turning:
                    self.change_direction(self.current_direction)
                self.x += (self.speed * self.x_direction)
                self.y += (self.speed * self.y_direction)
                self.time += 1
                self.emit_position()

    def emit_position(self):
        self.move_signal.emit((((self.current_x, self.current_y), (self.x,
                                                                   self.y)),
                               self.drawing, self.color))
        self.current_x = self.x
        self.current_y = self.y

    def pause_game(self):
        self.pause = not self.pause

    def apply_effect(self, power):
        print(power.type_power)
        if power.type_power == "Nebolt":
            thr = Thread(target=self.nebolt_effect, daemon=True)
            thr.start()
        elif power.type_power == "Limpiessa":
            self.clean_signal.emit(True)
        elif power.type_power == "Cervessa":
            thr = Thread(target=self.cervessa_effect, daemon=True)
            thr.start()
        elif power.type_power == "Nebcoin":
            self.nebcoin_effect()
        elif power.type_power == "SinRastro":
            thr = Thread(target=self.sinrastro)
            thr.start()
        elif power.type_power == "Trio":
            self.trio_signal.emit(self.name)
        elif power.type_power == "Somnolencia":
            thr = Thread(target=self.somnolencia_effect)
            thr.start()
        elif power.type_power == "Tau":
            thr = Thread(target=self.tau_effect)
            thr.start()
        elif power.type_power == "Atraviessa":
            self.atraviessa_signal.emit(True)

    def nebolt_effect(self):
        with power_lock:
            self.speed *= 2
        time_effect = 0
        while time_effect <= 5:
            sleep(1)
            time_effect += 1
        with power_lock:
            self.speed /= 2

    def cervessa_effect(self):
        self.invert_key_signal.emit(True)
        time_effect = 0
        while time_effect <= 5:
            sleep(1)
            time_effect += 1
        self.invert_key_signal.emit(True)

    def nebcoin_effect(self):
        self.add_nebcoin_signal.emit(self.name)

    def sinrastro(self):
        self.sinrastro_threads += 1
        self.is_sinrastro_effect = True
        time_effect = 0
        while time_effect <= 4:
            sleep(1)
            time_effect += 1
        with power_lock:
            self.sinrastro_threads -= 1
            if self.sinrastro_threads == 0:
                self.is_sinrastro_effect = False

    def somnolencia_effect(self):
        with power_lock:
            self.speed /= 2
        time_effect = 0
        while time_effect <= 5:
            sleep(1)
            time_effect += 1
        with power_lock:
            self.speed *= 2

    def tau_effect(self):
        with power_lock:
            self.is_tau_effect = True
        time_effect = 0
        while time_effect <= 6:
            sleep(1)
            time_effect += 1
        with power_lock:
            self.is_tau_effect = False

    def atraviessa_effect(self):
        with power_lock:
            self.is_atraviessa_effect = True
        time_effect = 0
        while time_effect <= 5:  # Se asumio que el efecto de Atraviessa era 5
            #  segundos
            time_effect += 1
            sleep(1)
        with power_lock:
            self.is_atraviessa_effect = False

    def start_atraviessa_effect(self):
        thr = Thread(target=self.atraviessa_effect)
        thr.start()
