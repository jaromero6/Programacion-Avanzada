from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QLabel
from client.game.backend import user
from client.game.frontend import game_window

PATH = "client/game/frontend/gui_ui/"

first_window_name, base_class_1 = uic.loadUiType(PATH + "first_window.ui")
log_in_window_, base_class_2 = uic.loadUiType(PATH + "log_in_window.ui")
sig_in_window, base_class_3 = uic.loadUiType(PATH + "sign_in_window.ui")
select_window, base_class_4 = uic.loadUiType(PATH + "control_selection.ui")
waiting_room, base_class_5 = uic.loadUiType(PATH + "waiting_room.ui")


class FirstWindow(first_window_name, base_class_1):
    def __init__(self, client=None):
        super().__init__()
        self.setupUi(self)
        self.client = client
        # Se conectan los botones con los metodos
        self.log_in_button.clicked.connect(self.log_in)
        self.sign_in_button.clicked.connect(self.sign_in)

    def log_in(self):
        self.hide()
        self.login_window = LogInWindow(self.client)
        self.login_window.show()

    def sign_in(self):
        self.hide()
        self.sign_window = SignInWindow(self.client)
        self.sign_window.show()


class LogInWindow(log_in_window_, base_class_2):
    information_signal = pyqtSignal(tuple)
    back_signal = pyqtSignal(bool)
    disconnect_signal = pyqtSignal(bool)

    def __init__(self, client=None):
        super().__init__()
        self.setupUi(self)
        self.warning_text.hide()  # Se esconde el mensaje de advertencia
        self.log_in_button.clicked.connect(self.send_to_check)
        self.back_button.clicked.connect(self.request_back)
        # Se crea la instancia del backend
        self.backend_user = user.User(self, client)
        # Se conectan las señales con el backend
        self.information_signal.connect(
            self.backend_user.send_log_in_information)
        self.back_signal.connect(self.backend_user.back)
        self.disconnect_signal.connect(self.backend_user.end_connection)

    def send_to_check(self):
        username = self.name_input.text()
        password = self.password_input.text()
        self.information_signal.emit((username, password))

    def done(self, signal):
        self.hide()
        self.selection_window = ControlSelectionWindow(signal[0], signal[1])
        self.selection_window.show()

    def show_warning(self, signal):
        self.warning_text.show()

    def request_back(self):
        self.back_signal.emit(True)

    def back(self, signal):
        self.hide()
        self.first_window = FirstWindow(signal)
        self.first_window.show()

    def closeEvent(self, e):
        self.disconnect_signal.emit(True)
        self.close()


class SignInWindow(sig_in_window, base_class_3):
    information_signal = pyqtSignal(tuple)
    back_signal = pyqtSignal(bool)
    disconnect_signal = pyqtSignal(bool)

    def __init__(self, client=None):
        super().__init__()
        self.setupUi(self)
        # Se esconden los mensajes de advertencia
        self.invalid_username.hide()
        self.invalid_password.hide()
        self.backend_user = user.User(self, client)
        # Se conenctan los botones
        self.sign_in_button.clicked.connect(self.send_to_check)
        self.back_button.clicked.connect(self.back)
        self.information_signal.connect(
            self.backend_user.send_sign_in_information)
        self.disconnect_signal.connect(self.backend_user.end_connection)

    def send_to_check(self):
        self.invalid_username.hide()
        self.invalid_password.hide()
        username = self.name_input.text()
        password = self.password_input.text()
        verification = self.verification_input.text()
        self.information_signal.emit((username, password, verification))

    def request_back(self):
        self.back_signal.emit(True)

    def back(self, signal):
        self.hide()
        self.first_window = FirstWindow(signal)
        self.first_window.show()

    def show_warning(self, signal):
        getattr(self, "invalid_" + signal).show()

    def done(self, signal):
        self.hide()
        self.login_window = LogInWindow(self.backend_user.client)
        self.login_window.show()

    def closeEvent(self, e):
        self.disconnect_signal.emit(True)
        self.close()


class ControlSelectionWindow(select_window, base_class_4):
    selection_key_signal = pyqtSignal(bool)
    current_key_signal = pyqtSignal(int)
    disconnect_signal = pyqtSignal(bool)

    def __init__(self, client, name):
        super().__init__()
        self.setupUi(self)
        self.backend_user = user.KeyControlUser(client, name, self)
        self.warning_text.hide()
        self.right_label.hide()
        self.select_button.clicked.connect(self.send_key)
        self.current_key_signal.connect(self.backend_user.receive_key)
        self.selection_key_signal.connect(self.backend_user.set_key)
        self.disconnect_signal.connect(self.backend_user.end_connection)

    def send_key(self):
        self.warning_text.hide()
        self.selection_key_signal.emit(True)

    def show_warning_text(self, signal):
        self.warning_text.show()

    def keyPressEvent(self, e):
        self.current_key_signal.emit(e.key())

    def request_for_another_key(self, signal):
        self.left_label.hide()
        self.right_label.show()

    def enter_to_waiting_room(self, signal):
        self.hide()
        self.waiting_room = WaitingRoom(signal[0], signal[1], signal[2],
                                        signal[3]
                                        , signal[4], signal[5], signal[6])
        self.waiting_room.show()

    def closeEvent(self, e):
        self.disconnect_signal.emit(True)
        self.close()


class WaitingRoom(waiting_room, base_class_5):
    message_signal = pyqtSignal(str)
    color_selected_signal = pyqtSignal(str)
    speed_signal = pyqtSignal(int)
    powers_signal = pyqtSignal(list)
    score_signal = pyqtSignal(int)
    start_signal = pyqtSignal(bool)
    disconnect_signal = pyqtSignal(bool)

    def __init__(self, client, name, leader, match_id, left, right, n_player):
        super().__init__()
        self.setupUi(self)
        self.warning_message.hide()
        self.backend_user = user.WaitingRoomUser(client, name, leader, match_id,
                                                 left, right, n_player, self)
        self.chat_label = QLabel("", self)
        self.chat_label.setAlignment(Qt.AlignTop)
        self.scrollchat.setWidget(self.chat_label)
        self.power_label.setAlignment(Qt.AlignTop)
        # Se conectan los botones
        self.sender_button.clicked.connect(self.send_message)
        self.sender_color.clicked.connect(self.choose_color)
        self.speed_selecter.valueChanged.connect(self.change_speed)
        self.score_box.valueChanged.connect(self.change_max_score)
        self.start_button.clicked.connect(self.start_game)
        for i in range(1, 10):
            getattr(self, "checkBox_" + str(i)).stateChanged.connect(
                self.add_remove_power)
        # Se conenctan las señales
        self.message_signal.connect(self.backend_user.send_message)
        self.color_selected_signal.connect(self.backend_user.send_color_request)
        self.speed_signal.connect(self.backend_user.change_speed)
        self.powers_signal.connect(self.backend_user.change_powers)
        self.score_signal.connect(self.backend_user.change_score)
        self.start_signal.connect(self.backend_user.start)
        self.disconnect_signal.connect(self.backend_user.end_connection)

    def show_name(self, signal):
        for i in range(1, 5):
            if i == signal[1]:
                getattr(self, "player_" + str(i)).setText(" " + signal[0])
                break

    def show_leader_commands(self):
        self.start_button.show()
        self.speed_title.show()
        self.score_title.show()
        self.power_title.show()
        self.speed_selecter.show()
        self.score_box.show()
        self.settings_label.show()
        for i in range(1, 10):
            getattr(self, "checkBox_" + str(i)).show()

    def hide_leader_options(self, signal):
        # Se esconde la parte del lider
        self.start_button.hide()
        self.speed_title.hide()
        self.score_title.hide()
        self.power_title.hide()
        self.speed_selecter.hide()
        self.score_box.hide()
        self.settings_label.hide()
        for i in range(1, 10):
            getattr(self, "checkBox_" + str(i)).hide()

    def send_message(self):
        text_to_send = self.message_line.text()  # Se extrae el texo de la
        # linea de mensaje
        self.message_line.setText("")
        self.message_signal.emit(text_to_send)

    def choose_color(self):
        self.warning_message.hide()
        colors = ["red", "green", "blue", "yellow"]
        for i in range(1, 5):
            if getattr(self, "radioButton_" + str(i)).isChecked():
                self.color_selected_signal.emit(colors[i - 1])

    def change_speed(self, value):
        self.speed_signal.emit(value)

    def add_remove_power(self):
        checked_boxed = []
        for i in range(1, 10):
            checked_boxed.append(getattr(self, "checkBox_" + str(
                i)).isChecked())
        self.powers_signal.emit(checked_boxed)

    def change_max_score(self):
        self.score_signal.emit(self.score_box.value())

    def show_color_changes(self, changes):
        for i in range(1, 5):
            getattr(self, "player_" + str(i)).setStyleSheet(
                f"background-color : {changes[i - 1]}")

    def show_warning(self, signal):
        self.warning_message.show()

    def show_speed(self, value):
        self.speed_label.setText("Velocidad: " + str(value))
        self.speed_label.setStyleSheet("color:white")

    def show_score(self, value):
        self.score_label.setText("Puntaje Máximo: " + str(value))
        self.score_label.setStyleSheet("color:white")

    def show_powers(self, value):
        self.power_label.setText("Poderes\n" + value)
        self.power_label.setStyleSheet("color:white")

    def show_new_message(self, message):
        self.chat_label.setText(message)

    def show_seconds(self, seconds):
        self.counting_label.setText(f"Empieza en {seconds} segundos")
        self.counting_label.setStyleSheet("color:white")

    def start_game(self):
        #self.start_button.hide()
        self.start_signal.emit(True)

    def hide_buttons(self, signal):
        self.hide_leader_options(True)
        self.sender_button.hide()
        self.sender_color.hide()

    def enter_game_room(self, signal):
        self.hide()
        self.game_window = game_window.GameWindow(*signal,
                                                  self.score_label.text(),
                                                  self.power_label.text(),
                                                  self.speed_label.text(),
                                                  WaitingRoom, FirstWindow)

        self.game_window.show()

    def closeEvent(self, e):
        self.disconnect_signal.emit(True)
        self.close()
