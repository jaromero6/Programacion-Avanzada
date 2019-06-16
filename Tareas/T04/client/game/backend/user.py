from PyQt5.QtCore import QObject, pyqtSignal, Qt
from client import client
from datetime import datetime

# Se encarga de comprobar el registro de usuario

### Como funciona ###
"""
Cuando en el frontend se capta un evento que necesita comnicarselo a los demas 
clientes o bien mandar al server para verificar como es el caso de las 
contraseñas, este le manda una señal al backend, el cual tiene un atributo 
que es una instancia de la clase cliente y mediante este se comunica con el 
server. Para la recepcion, el cliente tiene atributos que son metodos del 
backend ( Es como hacer un connect a mano) que los ejecuta acorde a la 
instruccuion
"""


class User(QObject):
    sign_in_signal = pyqtSignal(bool)  # Retornan True si el proceso fue exitoso
    log_in_signal = pyqtSignal(tuple)
    show_warning_signal = pyqtSignal(str)
    back_signal = pyqtSignal(tuple)

    def __init__(self, parent, clnt):
        super().__init__()
        self.name = None
        if clnt is not None:
            self.client = clnt  # Se inicia una comunicacion con el
        # server
        else:
            self.client = client.Client()
        # Se añaden las funciones a ejecutar segun la respuesta que reciba
        self.client.log_in_function = self.receive_log_in_response
        self.client.sign_in_function = self.receive_sign_in_response
        # Se conectan las señales
        self.log_in_signal.connect(parent.done)
        self.sign_in_signal.connect(parent.done)
        self.show_warning_signal.connect(parent.show_warning)
        self.back_signal.connect(parent.back)

    def receive_log_in_response(self, response):
        if not response:
            self.show_warning_signal.emit("show")
        else:
            self.log_in_signal.emit((self.client, self.name))

    def receive_sign_in_response(self, response):
        if not response:
            self.show_warning_signal.emit("username")
        else:
            self.sign_in_signal.emit(True)

    def send_log_in_information(self, information):
        self.name = information[0]  # Se actualiza el posible del usuario
        dictionary_to_server = {"action": "log_in", "username": information[
            0], "password": information[1]}

        self.client.send(dictionary_to_server)

    def send_sign_in_information(self, information):
        if information[1] == information[2]:
            dictionary_to_server = {"action": "sign_in",
                                    "username": information[
                                        0], "password": information[1]}
            self.client.send(dictionary_to_server)
        else:
            self.show_warning_signal.emit("password")

    def back(self, signal):
        self.back_signal.emit((self.client,))

    def end_connection(self, signal):
        self.client.send({"action": "quit"})


class KeyControlUser(QObject):
    checked_signal = pyqtSignal(bool)
    enter_waiting_room_signal = pyqtSignal(tuple)
    warning_signal = pyqtSignal(bool)

    def __init__(self, client, name, parent):
        super().__init__()
        self.client = client
        self.name = name
        self.client.join_function = self.receive_server_response
        self.left_key = None
        self.right_key = None
        self.receive = "left"  # se asigna primero a la tecla izquierda
        self.key_to_assign = None
        self.warning_signal.connect(parent.show_warning_text)
        self.enter_waiting_room_signal.connect(parent.enter_to_waiting_room)
        self.checked_signal.connect(parent.request_for_another_key)
        self.leader = None

    def receive_key(self, key):
        if key != Qt.Key_Space:  # No se asigna la tecla espacio ya que esta
            # tendrá un uso más adelante
            self.key_to_assign = key

    def set_key(self, signal):
        if self.receive == "left" and self.key_to_assign is not None:
            self.left_key = self.key_to_assign
            self.receive = "right"
            self.checked_signal.emit(True)
        elif self.key_to_assign is not None:  # Entonces receive es right
            if self.key_to_assign != self.left_key:
                self.right_key = self.key_to_assign
                self.send_final_request()
            else:
                self.warning_signal.emit(True)

    def send_final_request(self):
        to_send = {"action": "enter", "name": self.name}
        self.client.send(to_send)

    def receive_server_response(self, leader, match_id, n_player):
        self.enter_waiting_room_signal.emit((self.client, self.name, leader,
                                             match_id,
                                             self.left_key, self.right_key,
                                             n_player))

    def end_connection(self, signal):
        self.client.send({"action": "quit"})


class WaitingRoomUser(QObject):
    not_leader_signal = pyqtSignal(bool)
    leader_signal = pyqtSignal(bool)
    show_message_signal = pyqtSignal(str)
    change_colors_signal = pyqtSignal(list)
    warning_color_signal = pyqtSignal(bool)
    name_signal = pyqtSignal(tuple)
    speed_signal = pyqtSignal(int)
    score_signal = pyqtSignal(int)
    power_signal = pyqtSignal(str)
    seconds_signal = pyqtSignal(int)
    start_signal = pyqtSignal(tuple)
    hide_buttons_signal = pyqtSignal(bool)

    def __init__(self, client, name, leader, match_id, left, right, n_player,
                 parent):
        super().__init__()
        self.name = name
        self.client = client
        self.leader = leader
        self.match_id = match_id
        self.left_key = left
        self.right_key = right
        self.n_player = n_player
        self.chat_messages = ""
        # Se asginan las respectivas funciones al ciente ------------------
        self.client.chat_function = self.receive_message
        self.client.color_function = self.receive_color_changes
        self.client.update_settings_function = self.update_settings
        self.client.update_window_function = self.update_window
        self.client.update_name_function = self.update_name
        self.client.counting_function = self.counting
        self.client.start_game_function = self.open_window
        self.client.leader_command_function = self.show_leader_options
        # Se realizan las conexiones de señales --------------------
        self.not_leader_signal.connect(parent.hide_leader_options)
        self.show_message_signal.connect(parent.show_new_message)
        self.change_colors_signal.connect(parent.show_color_changes)
        self.warning_color_signal.connect(parent.show_warning)
        self.name_signal.connect(parent.show_name)
        self.speed_signal.connect(parent.show_speed)
        self.score_signal.connect(parent.show_score)
        self.power_signal.connect(parent.show_powers)
        self.seconds_signal.connect(parent.show_seconds)
        self.start_signal.connect(parent.enter_game_room)
        self.leader_signal.connect(parent.show_leader_commands)
        self.hide_buttons_signal.connect(parent.hide_buttons)

        if not self.leader:  # Se oculta la ventana del lider -------
            self.not_leader_signal.emit(True)
        self.request_for_update_window()

    def show_leader_options(self):
        self.leader_signal.emit(True)

    def send_name(self):  # Envia el nombre al server para actualizarlo
        to_send = {"action": "update_name", "name": self.name,
                   "match": self.match_id, "player_id": self.n_player}
        self.client.send(to_send)

    def update_name(self, names, leader):  # Recibe los nombres de
        #  p1,p2,...
        c = 1
        for i in names:
            if i != leader:
                self.name_signal.emit((i, c))
            else:
                self.name_signal.emit((i + "(Lider)", c))
            c += 1

    def send_message(self, message):
        # Primero se envia el mensaje con cierto formato
        if message != "":
            message_to_send = (self.name + "\n" +
                               datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
                               " : " + message + "\n")
            to_send = {"action": "message", "content": message_to_send,
                       "match": self.match_id}
            self.client.send(to_send)

    def send_color_request(self, color):
        request_to_send = {"action": "color", "color": color,
                           "match": self.match_id, "player_id": self.n_player}
        self.client.send(request_to_send)

    def receive_message(self, message):
        self.chat_messages += message
        self.show_message_signal.emit(self.chat_messages)

    def receive_color_changes(self, changes, player_id):
        if changes is not None:
            new_color = []
            # Se envian en el orden player 1, player 2, ....
            for i in changes:
                new_color.append(changes[i])
            self.change_colors_signal.emit(new_color)
        else:
            if player_id == self.n_player:
                self.warning_color_signal.emit(True)

    def change_speed(self, speed):
        to_send = {"action": "speed", "speed": speed, "match": self.match_id}
        self.client.send(to_send)

    def change_powers(self, powers):
        name_power = ["Nebcoin", "Limpiessa", "SinRastro", "Cervessa",
                      "Trio", "Nebolt", "Somnolencia", "Tau", "Atraviessa"]
        power_to_use = []
        for i in range(9):
            if powers[i]:
                power_to_use.append(name_power[i])
        to_send = {"action": "power", "powers": power_to_use,
                   "match": self.match_id}
        self.client.send(to_send)

    def change_score(self, value):
        to_send = {"action": "score", "score": value, "match": self.match_id}
        self.client.send(to_send)

    def update_settings(self, setting, value):
        if setting == "speed":
            self.speed_signal.emit(value)
        elif setting == "score":
            self.score_signal.emit(value)
        elif setting == "powers":
            powers_str = ""
            c = 1
            for i in value:
                powers_str += i + ","
                if c % 2 == 0:
                    powers_str += "\n"
                c += 1
            self.power_signal.emit(powers_str)

    def request_for_update_window(self):  # Se encarga de actualizar la
        # ventana acorde a los cambios previos que a tenido esta
        self.client.send({"action": "update_window", "match": self.match_id})

    def update_window(self, names, colors, speed, score, powers, leader):
        self.update_name(names, leader)
        self.change_colors_signal.emit(colors)
        self.update_settings("speed", speed)
        self.update_settings("score", score)
        self.update_settings("powers", powers)

    def start(self, signal):
        to_send = {"action": "start", "match": self.match_id}
        self.client.send(to_send)

    def counting(self, seconds):
        if seconds == 10:
            self.hide_buttons_signal.emit(True)
        self.seconds_signal.emit(seconds)
        if seconds == 0:
            to_send = {"action": "start_game", "match": self.match_id}
            self.client.send(to_send)

    def open_window(self, colors):
        c = 1
        for i in colors:
            if c == self.n_player:
                own_color = i
                self.start_signal.emit(
                    (self.name, self.left_key, self.right_key,
                     own_color, self.match_id, self.n_player,
                     self.client))
                break
            c += 1

    def end_connection(self, signal):
        to_send = {"action": "logout", "match": self.match_id,
                   "name": self.name}
        self.client.send(to_send)
