from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, Qt, QPoint, QRect, QSize
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QPixmap, QPainter, QPen, QBrush, QImage, QColor
from client.game.backend import game_user

PATH = "client/game/frontend/gui_ui/"
IMAGES = "client/game/frontend/images/"

game_window, class_window = uic.loadUiType(PATH + "game_window.ui")


class GameMap(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.img = QImage(IMAGES + "font.png")
        self.pixmap = QPixmap(self.img)
        self.setGeometry(250, 20, 1041, 641)
        self.pixmap.fill(Qt.transparent)
        self.red_sprite = QLabel(self)
        self.blue_sprite = QLabel(self)
        self.green_sprite = QLabel(self)
        self.yellow_sprite = QLabel(self)
        self.red_sprite.hide()
        self.blue_sprite.hide()
        self.green_sprite.hide()
        self.yellow_sprite.hide()

    def create_sprites(self, color):
        image = QPixmap(IMAGES + color + "_sprite.png")
        getattr(self, f"{color}_sprite").setPixmap(image)
        getattr(self, f"{color}_sprite").show()

    def move_sprite(self, pos, color):

        getattr(self, f"{color}_sprite").move(pos[0]  ,
                                              pos[1] - 5)

    def draw_method(self, signal):
        colors = {"blue": Qt.blue, "red": Qt.red, "green": Qt.green,
                  "yellow": Qt.yellow}
        painter = QPainter(self.img)
        painter.setRenderHint(QPainter.Antialiasing)
        brush = QBrush(colors[signal[1]])
        pen = QPen(colors[signal[1]], 5)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawLine(QPoint(*signal[0][0]), QPoint(*signal[0][1]))
        painter.end()
        self.update()

    def show_power_up(self, power, position):
        power_up_label = QLabel(self)
        img = QPixmap(IMAGES + f"{power}_sprite.png")
        power_up_label.setPixmap(img)
        power_up_label.move(position[0], position[1])
        power_up_label.show()
        return power_up_label

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.img)

    def get_color(self, pixel_pos):
        return QColor(self.img.pixel(*pixel_pos)).getRgb()


class GameWindow(game_window, class_window):
    back_signal = pyqtSignal(bool)
    new_signal = pyqtSignal(bool)
    direction_signal = pyqtSignal(int)
    add_rect_signal = pyqtSignal(tuple)
    pause_signal = pyqtSignal(bool)
    restart_signal = pyqtSignal(bool)
    stop_turning_signal = pyqtSignal(bool)
    color_signal = pyqtSignal(tuple)
    disconnect_signal = pyqtSignal(bool)

    def __init__(self, name, left_key, right_key, color, match_id, n_player,
                 client, max_score, powers, speed, WaitingRoomClass,
                 FirstWindowClass):
        super().__init__()
        self.setupUi(self)
        self.WaitingRoomClass = WaitingRoomClass
        self.FirstWindowClass = FirstWindowClass
        self.backend_user = game_user.GameUser(name, left_key, right_key,
                                               color, match_id, n_player,
                                               client, max_score, powers,
                                               speed, self)
        self.game_map = GameMap(self)
        self.game_map.show()
        # Se conectan los botones
        self.pause_button.clicked.connect(self.pause)
        self.back_button.clicked.connect(self.back)
        self.new_button.clicked.connect(self.new_game)
        # Se conectan las señales
        self.back_signal.connect(self.backend_user.back_request)
        self.new_signal.connect(self.backend_user.new_request)
        self.direction_signal.connect(self.backend_user.change_direction)
        self.add_rect_signal.connect(self.backend_user.add_rect)
        self.pause_signal.connect(self.backend_user.send_to_pause)
        self.restart_signal.connect(self.backend_user.restart_game)
        self.stop_turning_signal.connect(self.backend_user.stop_turn)
        self.color_signal.connect(self.backend_user.check_collision)
        self.disconnect_signal.connect(self.backend_user.logout)

    def new_game(self):
        self.new_signal.emit(True)

    def pause(self):
        self.pause_signal.emit(True)

    def back(self):
        self.back_signal.emit(True)

    def back_to_first_window(self, signal):
        self.hide()
        self.first_window = self.FirstWindowClass()
        self.first_window.show()

    def back_to_waiting_room(self, signal):
        self.hide()
        self.waiting_room = self.WaitingRoomClass(signal[0], signal[1],
                                                  signal[2], signal[3],
                                                  signal[4], signal[5],
                                                  signal[6])
        self.waiting_room.show()

    def show_max_score(self, score):
        text = self.win_score_label.text().replace("50", str(score))
        self.win_score_label.setText(text)
        self.win_score_label.setStyleSheet(
            "background-color: rgb(21, 173, 255);"
            "color:white;font: 87 36pt Segoe UI Black")

    def show_names(self, signal):
        getattr(self, "name_" + str(signal[0])).setText(signal[1])
        getattr(self, "color_" + str(signal[0])).setStyleSheet(
            f"background-color:{signal[2]}")
        getattr(self, "name_" + str(signal[0])).setStyleSheet("color:white;"
                                                              "font: 87 12pt "
                                                              "Segoe UI Black")

    def show_scores(self, signal):
        getattr(self, "score_" + str(signal[0])).setText(str(signal[1]))
        getattr(self, "score_" + str(signal[0])).setStyleSheet("color:white;"
                                                               "font: 87 12pt "
                                                               "Segoe UI Black")

    def show_characters(self, signal):
        self.game_map.create_sprites(signal[0])
        self.game_map.move_sprite(signal[1], signal[0])

    def keyPressEvent(self, e):
        if not e.isAutoRepeat():
            self.direction_signal.emit(e.key())

    def keyReleaseEvent(self, e):
        if not e.isAutoRepeat():
            self.stop_turning_signal.emit(True)

    def move_character(self, signal):
        self.game_map.move_sprite((signal[1][0], signal[1][1]), signal[2])

    def draw_trail(self, signal):
        self.game_map.draw_method(signal)
        rect_trail = QRect(QPoint(*signal[0][0]), QSize(2.5, 2.5))
        sprite_rect = QRect(QPoint(*signal[0][1]), QSize(2.5, 2.5))
        self.add_rect_signal.emit((rect_trail, sprite_rect, signal[2]))

    def show_final_message(self, signal):
        self.result_label.setText(signal)
        self.result_label.setStyleSheet("color:white;font: 87 8pt Segoe UI "
                                        "Black")

    def show_power_up(self, signal):
        r = self.game_map.show_power_up(signal[0], signal[1])
        r.show()
        signal[2].append(r)

    def restart_screen(self):
        self.game_map.close()
        self.game_map = GameMap(self)
        self.game_map.show()
        self.restart_signal.emit(True)

    def clean_map(self):
        self.game_map = GameMap(self)
        self.game_map.show()

    def get_color(self, signal):
        color = self.game_map.get_color(signal)
        self.color_signal.emit(color[0:3])

    def closeEvent(self, event):
        self.disconnect_signal.emit(True)
