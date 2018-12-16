from time import sleep
from threading import Thread
from game_server import Game

"""
La clase Match se encarga de transmitirles la informacion solo a los miembros de 
una misma partida, asi como tambien asignarlos a ciertos colores, verificar 
cuales son ocupados, guardar los poderes y parametros que el lider decida.
 PPor otra parte MatchOrganizer se encarga principalmente de recibida una 
 intruccion buscar el match que corresponde y hacer que este ejecute la 
 instruccion
"""


class Match:
    class_id = 0

    def __init__(self, send_function):
        self.send_function = send_function
        self.participants = []
        self.game_slot = {1: None, 2: None, 3: None, 4: None}
        self.match_id = self.class_id
        self.names = ["Player 1", "Player 2", "Player 3", "Player 4"]
        self.available_to_join = True
        Match.class_id += 1
        self.speed = 1
        self.powers = set()
        self.max_score = 1
        self.default_colors = {1: "red", 2: "blue", 3: "green", 4: "yellow"}
        self.assigned_color = {"red": None, "blue": None, "green": None,
                               "yellow": None}
        self.users_positions = [(0, 0), (0, 0), (0, 0), (0, 0)]
        self.users_points = [0, 0, 0, 0]
        self.seconds_to_start = 10
        self.count_signals = 0
        self.count_thread = Thread(target=self.decrease_count_thread,
                                   daemon=True)
        self.game = None

    @property
    def leader(self):
        if len(self.participants) > 0:
            for i in self.game_slot:
                if self.game_slot[i] == self.participants[0]:
                    return i
        return 1

    def assign_slot(self, socket):
        for i in range(1, 5):
            if self.game_slot[i] is None:
                self.game_slot[i] = socket
                return i

    def add_new_client(self, socket, name):
        to_send = {"action": "join", "id_match": self.match_id, "leader":
            False, "id_player": 0}
        if len(self.participants) == 0:
            to_send["leader"] = True  # Se manda true si es lider
        self.participants.append(socket)
        if len(self.participants) >= 4:
            self.available_to_join = False
        n_player = self.assign_slot(socket)
        to_send["id_player"] = n_player
        self.names[n_player - 1] = name
        self.send_function(to_send, socket)

    def update_participants(self, information):
        """
         Recibe informacion y la manda a todos su participantes. Con esto se
         asegura de solo mandar la informaion de una partida a los usuarios
         de dicha partida.
        """
        for i in self.participants:
            self.send_function(information, i)

    def lost_connection(self, socket, name=None):
        socket_index = self.participants.index(socket)
        self.participants.pop(socket_index)
        self.names[socket_index] = f"Player {socket_index + 1}"
        self.game_slot[socket_index + 1] = None
        # Se libera el color
        if self.game is None:
            self.assigned_color[self.default_colors[socket_index + 1]] = None
            if len(self.participants) > 0 and socket_index \
                    == 0:  # Significa que se esta en la sala de espera
                self.send_function({"action": "new_leader"},
                                   self.participants[0])
            # Se cambia de lider
            elif len(self.participants) == 0:
                return True
            self.send_settings()  # Se actualizan todos
        else:
            result = self.game.withdraw_user(name)
            self.update_participants({"action": "kill_player", "name":
                name})
            return result  # Si se salen todos se acaba el juego ya que
            # result seria True

    def add_new_message(self, message):
        send_to_client = {"action": "message",
                          "all_messages": message}
        self.update_participants(send_to_client)  # Se le manda a todos la
        # informacion

    def set_new_name(self, name, player_id):
        self.names[player_id - 1] = name
        to_send = {"action": "update_name", "names": self.names}
        self.update_participants(to_send)

    def assign_color(self, color, player_id):
        response_to_send = {"action": "color", "changes": None,
                            "player": player_id}
        if self.assigned_color[color] is None:
            self.assigned_color[color] = player_id  # Se le asigna al jugador
            new_default_color = self.default_colors[player_id]  # Se deja libre
            # el color
            for i in self.default_colors:
                if self.default_colors[i] == color:
                    self.default_colors[
                        i] = new_default_color  # Se intercambian
            self.default_colors[player_id] = color  # Se actualiza el color
            response_to_send["changes"] = self.default_colors
        self.update_participants(response_to_send)  # Se le envia a todos los
        #  nuevos colores

    def set_speed(self, speed):
        self.speed = speed
        to_send = {"action": "speed", "value": self.speed}
        self.update_participants(to_send)

    def change_powers(self, powers):
        self.powers = set()
        for i in powers:
            self.powers.add(i)
        response = {"action": "powers", "value": list(self.powers)}
        self.update_participants(response)

    def change_score(self, score):
        self.max_score = int(score)
        response = {"action": "score", "value": self.max_score}
        self.update_participants(response)

    def send_settings(self):
        names = self.names
        colors = list(self.default_colors.values())
        speed = self.speed
        score = self.max_score
        powers = list(self.powers)
        to_send = {"action": "update_window", "names": names, "colors": colors,
                   "speed": speed, "score": score, "powers": powers,
                   "leader": self.names[self.leader - 1]}
        self.update_participants(to_send)

    def start_count(self):
        if len(self.participants) > 1:  # Cambiar esta linea si desea probar
            # simplemente con un solo jugador, aunque se caera en caso de una
            #  colision, pero puede ser util para probar power ups
            self.available_to_join = False
            self.scores = {self.names[0]: 0, self.names[1]: 0, self.names[2]: 0,
                           self.names[3]: 0}
            self.count_thread.start()

    def decrease_count_thread(self):
        while self.seconds_to_start >= 0:
            to_send = {"action": "starting", "seconds": self.seconds_to_start}
            self.update_participants(to_send)
            sleep(1)
            self.seconds_to_start -= 1

    def withdraw_user(self, socket, finish=True):
        index_user = self.participants.index(socket)
        name_user = self.names[index_user]
        self.participants.pop(index_user)
        result = self.game.withdraw_user(name_user)
        if finish:
            self.update_participants({"action": "kill_player", "name":
                name_user})
        return result, name_user

    def open_game_window(self):
        to_send = {"action": "start_game", "colors": list(
            self.default_colors.values())}
        self.update_participants(to_send)

    def send_game_settings(self, socket):
        if self.game is None:
            self.game = Game(self.game_slot, self.names, self.default_colors,
                             self.powers,
                             self)
        to_send = self.game.get_game_information()
        to_send["action"] = "game_settings"
        self.count_signals = 0
        self.send_function(to_send, socket)

    def change_direction(self, direction, name):
        to_send = {"action": "change_direction", "direction": direction,
                   "name": name}
        self.update_participants(to_send)

    def update_position(self, position, paint, color):
        to_send = self.game.update_position(position, paint, color)
        self.update_participants(to_send)

    def pause_game(self):
        to_send = {"action": "pause"}
        self.update_participants(to_send)

    def check_collision(self, names):
        result = self.game.check_collision(names)
        to_send = {"action": "update_score", "scores": result,
                   "winner": self.game.check_winner(self.max_score), "restart":
                       self.game.ask_for_restart_round()}
        if to_send["restart"]:
            self.game.start_new_round()
        self.update_participants(to_send)

    def restart_game(self):
        self.count_signals += 1
        if self.count_signals >= len(self):
            to_send = self.game.get_game_information()
            to_send["action"] = "game_settings"
            self.update_participants(to_send)
            self.count_signals = 0

    def stop_turning(self, name):
        to_send = {"action": "stop_turning", "name": name}
        self.update_participants(to_send)

    def send_triple_powers(self):
        powers = self.game.apply_trio_power()
        if powers is not None:
            to_send = {"action": "trio", "powers": powers}
            self.update_participants(to_send)

    def add_nebcoin(self, name):
        self.game.add_nebcoin(name)

    def __eq__(self, other):
        return self.match_id == other.mach_id

    def __contains__(self, item):
        return item in self.participants

    def __len__(self):
        return len(self.participants)


class MatchOrganizer:
    def __init__(self, send_function):
        self.send_function = send_function
        self.matches = {}

    def new_user(self, socket, name):
        """
        A la llegada de un nuevo usuario, verifica si este se puede unir a
        una partida ya existente o se crea una nueva
        """
        for i in self.matches.values():  # Si hay creadas se buscan disponibles
            if i.available_to_join:
                i.add_new_client(socket, name)
                return
        # Si no se encontraron disponibles entonces se crea una
        new_match = Match(self.send_function)
        self.matches[new_match.match_id] = new_match
        new_match.add_new_client(socket, name)

    def set_new_name(self, name, id_match, player_id):
        self.matches[id_match].set_new_name(name, player_id)

    def new_message(self, message, id_match):
        self.matches[id_match].add_new_message(message)

    def assign_color(self, color, match, id_player):
        self.matches[match].assign_color(color, id_player)

    def change_speed(self, speed, match_id):
        self.matches[match_id].set_speed(speed)

    def change_powers(self, powers, match_id):
        self.matches[match_id].change_powers(powers)

    def change_score(self, score, match_id):
        self.matches[match_id].change_score(score)

    def send_all_settings(self, match_id):
        self.matches[match_id].send_settings()

    def start_count(self, match_id):
        self.matches[match_id].start_count()

    def open_game_window(self, match_id):
        self.matches[match_id].open_game_window()

    def logout_user(self, match_id, socket, name):
        result = self.matches[match_id].lost_connection(socket, name)
        if result:
            del self.matches[match_id]  # Se borra, ya que se
            # vacio completamente el juego o la sala de espera

    def new_game(self, match_id, socket):
        result = self.matches[match_id].withdraw_user(socket, False)
        if result[0]:
            del self.matches[match_id]
        self.new_user(socket, result[1])

    def send_game_settings(self, socket, match_id):
        self.matches[match_id].send_game_settings(socket)

    def change_direction(self, direction, match_id, name):
        self.matches[match_id].change_direction(direction, name)

    def update_position(self, match_id, position, paint, color):
        self.matches[match_id].update_position(position, paint, color)

    def pause_game(self, match_id):
        self.matches[match_id].pause_game()

    def check_collision(self, names, match_id):
        self.matches[match_id].check_collision(names)

    def restart_game(self, match_id):
        self.matches[match_id].restart_game()

    def stop_turning(self, name, match_id):
        self.matches[match_id].stop_turning(name)

    def send_triple_powers(self, match_id):
        self.matches[match_id].send_triple_powers()

    def add_nebcoin(self, match_id, name):
        self.matches[match_id].add_nebcoin(name)

    def __getitem__(self, item):
        return self.matches[item]
