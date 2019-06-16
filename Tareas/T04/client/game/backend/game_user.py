from random import randint
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from client.game.backend import power_up, character


class GameUser(QObject):
    back_signal = pyqtSignal(bool)
    enter_waiting_room_signal = pyqtSignal(tuple)
    names_signal = pyqtSignal(tuple)
    points_signal = pyqtSignal(tuple)
    positions_signal = pyqtSignal(tuple)
    max_score_signal = pyqtSignal(int)
    move_signal = pyqtSignal(tuple)
    trail_signal = pyqtSignal(tuple)
    winner_signal = pyqtSignal(str)
    restart_signal = pyqtSignal(bool)
    power_up_appear_signal = pyqtSignal(tuple)
    clean_signal = pyqtSignal(bool)
    color_signal = pyqtSignal(tuple)

    def __init__(self, name, left_key, right_key, color, match_id,
                 n_player, client, max_score, powers, speed, parent):
        super().__init__()
        self.name = name
        self.left_key = left_key
        self.right_key = right_key
        self.color = color
        self.match_id = match_id
        self.position = n_player
        self.client = client
        self.max_score = max_score
        self.speed = 2 + int(speed.split(":")[1])
        self.powers = powers
        self.head_rects = {"blue": None, "red": None, "green": None,
                           "yellow": None}
        self.is_alive = False
        self.drawing_time = randint(100, 150)
        self.not_drawing_time = randint(5, 20)
        self.pause = False
        self.continue_game = True
        self.power_ups = {}
        self.players = {}
        self.turning = False
        # Se conecta con el cliente -------------------------------------------
        self.client.join_function = self.enter_new_game
        self.client.update_position_function = self.receive_positions
        self.client.update_scores_function = self.update_scores
        self.client.receive_game_settings_function = self.receive_settings
        self.client.pause_function = self.pause_game
        self.client.show_new_power_up_function = self.show_new_power_up
        self.client.change_direction_function = self.receive_direction
        self.client.stop_turning_function = self.mantain_direction
        self.client.apply_trio_function = self.show_trio
        self.client.kill_player_function = self.kill_player
        # Se conecta con el frontend ------------------------------------------
        self.back_signal.connect(parent.back_to_first_window)
        self.enter_waiting_room_signal.connect(parent.back_to_waiting_room)
        self.names_signal.connect(parent.show_names)
        self.points_signal.connect(parent.show_scores)
        self.positions_signal.connect(parent.show_characters)
        self.max_score_signal.connect(parent.show_max_score)
        self.move_signal.connect(parent.move_character)
        self.trail_signal.connect(parent.draw_trail)
        self.winner_signal.connect(parent.show_final_message)
        self.restart_signal.connect(parent.restart_screen)
        self.power_up_appear_signal.connect(parent.show_power_up)
        self.clean_signal.connect(parent.clean_map)
        self.color_signal.connect(parent.get_color)
        # Se pide mostrar la informacion
        self.request_settings()
        self.show_max_score(self.max_score)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_timer)
        self.timer.start(50)

    def change_direction(self, direction):
        if not self.turning:
            if direction == self.left_key:
                self.players[self.name].change_direction("l")
            elif direction == self.right_key:
                self.players[self.name].change_direction("r")

    def stop_turn(self):
        self.turning = False
        to_send = {"action": "stop_turning", "name": self.name,
                   "match": self.match_id}
        self.client.send(to_send)

    def mantain_direction(self, name):
        self.players[name].stop_turn()

    def move_timer(self):
        if not self.pause and self.continue_game:
            for i in self.players.values():
                if i.name == self.name:
                    i.move_tick()
                    self.color_signal.emit(i.front_point)
            self.check_power_up_collision()

    def check_power_up_collision(self):
        delete_index = set()
        for i in self.power_ups:
            for j in self.players:
                if self.players[j].head is not None:
                    if self.players[j].head.intersects(self.power_ups[i][
                                                           0].rect):
                        self.players[j].apply_effect(self.power_ups[i][0])
                        self.dissapear_power_up(i)
                        return
        for i in delete_index:
            del self.power_ups[i]

    def check_collision(self, color):
        if not self.players[self.name].is_sinrastro_effect and self.players[
            self.name].is_alive:
            if color != (0, 0, 0):
                self.players[self.name].is_alive = False
                to_send = {"action": "collision", "match": self.match_id,
                           "name": [self.name]}
                self.client.send(to_send)
                return
            if self.is_alive:
                collision = [self.name]
                for i in self.players.values():
                    if i.name != self.name:
                        if self.head_rects[i.color] is not None and \
                                        self.head_rects[
                                            self.color] is not None:
                            if self.head_rects[self.color].insercts(
                                            self.head_rects[i.color] and not
                                    i.is_sinrastro_effect):
                                self.is_alive = False
                                collision.append(i)
                if len(collision) > 1:
                    to_send = {"action": "collision", "match":
                        self.match_id, "name": collision}
                    self.client.send(to_send)

    def add_rect(self, signal):
        self.head_rects[signal[2]] = signal[1]

    # Comunicacion con el server ----------------------------------------------

    def request_settings(self):  # Le pide al server la informacion para
        # desplegarla en la pantalla
        to_send = {"action": "game_settings", "match": self.match_id}
        self.client.send(to_send)

    def send_to_pause(self):
        to_send = {"action": "pause", "match": self.match_id}
        self.client.send(to_send)

    def show_max_score(self, value):
        self.max_score = value.split(":")[1]  # Se cambia a numero
        self.max_score = int(self.max_score)
        self.max_score_signal.emit(self.max_score)

    def receive_direction(self, direction, name):
        self.players[name].change_direction(direction)

    def update_positions(self, signal):
        to_send = {"action": "update_position", "position": signal[0],
                   "paint": signal[1], "color": signal[2],
                   "match": self.match_id}
        self.client.send(to_send)

    def receive_positions(self, position, paint, color):
        if color != self.color:
            for i in self.players:
                if self.players[i].color == color:
                    self.players[i].x, self.players[i].y = position[1]
        self.move_signal.emit((position[0], position[1], color))
        if paint:
            self.trail_signal.emit((position, color, self.color))

    def update_scores(self, scores, winner, restart):
        c = 1
        for i in scores:
            self.points_signal.emit((c, i))
            c += 1
        if winner:
            self.is_alive = False
            self.continue_game = False
            if self.name == winner:
                self.winner_signal.emit("¡Has ganado! Felicidades")
            else:
                self.winner_signal.emit("Más suerte para la proxima")
        elif restart:
            self.is_alive = False
            self.continue_game = False
            self.restart_signal.emit(True)

    def receive_settings(self, names, points, positions, colors, paint_time,
                         no_paint_time):
        c = 1
        for i in names:
            self.names_signal.emit((c, i, colors[c - 1]))
            self.points_signal.emit((c, points[c - 1]))
            self.positions_signal.emit((colors[c - 1], positions[c - 1]))
            player = character.Character(i, *positions[c - 1], colors[c - 1],
                                         self.speed, self.color, paint_time[c
                                                                            - 1],
                                         no_paint_time[c - 1], self)
            self.players[i] = player
            c += 1
        self.is_alive = True
        self.continue_game = True

    def back_request(self, signal):  # Vuelve a la ventana de inicio
        self.timer.stop()
        self.client.send({"action": "logout", "match": self.match_id,
                         "name":self.name})
        self.back_signal.emit(True)

    def pause_game(self):
        self.pause = not self.pause
        if not self.pause:
            self.timer.stop()
        else:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.move_timer)
            self.timer.start(50)

    def new_request(self, signal):
        self.timer.stop()
        self.client.send({"action": "new", "match": self.match_id})

    def enter_new_game(self, leader, match_id, n_player):
        self.enter_waiting_room_signal.emit((self.client, self.name, leader,
                                             match_id,
                                             self.left_key, self.right_key,
                                             n_player))

    def restart_game(self, signal):
        self.rects = []
        self.angle = 0
        for i in self.head_rects:
            self.head_rects[i] = None
        self.time = 0
        to_send = {"action": "restart_game", "match": self.match_id}
        self.client.send(to_send)

    def show_new_power_up(self, power, position):
        pow = power_up.PowerUp(*position, power, self)
        self.power_ups[pow.id_power] = [pow]
        self.power_up_appear_signal.emit((power, position, self.power_ups[
            pow.id_power]))

    def dissapear_power_up(self, signal):
        self.power_ups[signal][1].hide()
        self.power_ups[signal][0].is_alive = False
        del self.power_ups[signal]

    def clean_map(self, signal):
        self.rects = []
        self.clean_signal.emit(True)
        for i in self.players:
            self.positions_signal.emit((self.players[i].color, self.players[
                i].x, self.players[i].y))

    def invert_key(self, signal):
        aux = self.left_key
        self.left_key = self.right_key
        self.right_key = aux

    def request_trio_power(self, signal):
        if signal == self.name:
            to_send = {"action": "trio", "match": self.match_id}
            self.client.send(to_send)

    def show_trio(self, power_pos):
        for i in power_pos:
            self.show_new_power_up(i[0], i[1])

    def apply_atraviessa_effect(self, signal):
        for i in self.players:
            self.players[i].start_atraviessa_effect()

    def collision(self, signal):
        if signal == self.name:
            to_send = {"action": "collision", "match": self.match_id,
                       "name": [self.name]}
            self.client.send(to_send)

    def add_nebcoin(self, signal):
        if signal == self.name:
            to_send = {"action": "add_nebcoin", "match": self.match_id,
                       "name": signal}
            self.client.send(to_send)

    def logout(self, signal):
        self.timer.stop()
        self.client.send({"action": "logout", "match": self.match_id,
                          "name": self.name})

    def kill_player(self, name):
        self.players[name].continue_game = False
