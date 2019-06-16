from random import randint, choice
from threading import Thread, Lock
from time import sleep

alive_lock = Lock()

"""
La clase player contiene atributos que se deben mantener entre todos lo 
clientes de un juego, como por ejemplo la posicion inicial, el tiempo que 
dibujan y el que no y almacena las mondeas, ya que el calculo de asignacion 
de puntaje se lleva a cabo en el server
"""


class Player:
    def __init__(self, name, x, y, color):
        self.name = name
        self.color = color
        self.x = x
        self.y = y
        self.points = 0
        self.coins = 0
        self.drawing_time = randint(100, 150)
        self.not_drawing_time = randint(5, 20)
        self.is_alive = True

    def __eq__(self, other):
        return self.name == other.name


"""
La clase Game se encarga de realizar los cálculos de asignacion de puntaje, 
posicion inicial y de señalar cuando termina una ronda o el juego, asi mismo 
tambien es la que calcula cuando aparecen los poderes en el mapa,donde 
aparecen y cuales aparecen
"""


class Game:
    def __init__(self, participants, names, default_colors, powers, parent):
        self.sender_function = parent.update_participants
        self.powers = powers
        c = 0
        self.game_information = {}
        self.players = {}
        self.used_positions = set()
        self.current_time = 0
        self.power_up_time = randint(5, 10)
        self.is_alive = True  # Es true si se está jugando el juego
        for i in participants:
            if participants[i] is not None:
                self.game_information[names[c]] = [default_colors[c + 1], 0, 0]
            c += 1
        for i in self.game_information:
            self.players[i] = Player(i, 0, 0, self.game_information[i][0])
        self.set_initial_positions()
        if self.powers:
            self.appear_power_up_thread = Thread(target=self.power_up_tick)
            self.appear_power_up_thread.start()

    def set_initial_positions(self):
        zones = [(randint(100, 300), randint(100, 250)),
                 (randint(400, 600), randint(100, 250)),
                 (randint(100, 300), randint(300, 500)),
                 (randint(400, 600), randint(300, 500))]
        c = 0
        for i in self.game_information:
            self.game_information[i][2] = zones[c]
            self.players[i].x, self.players[i].y = zones[c]
            self.used_positions.add(zones[c])
            c += 1

    def get_game_information(self):
        dict_to_return = {"action": "game_settings"}
        names = []
        colors = []
        points = []
        positions = []
        t_paint = []
        nt_paint = []
        for i in self.players.values():
            names.append(i.name)
            colors.append(i.color)
            points.append(i.points)
            positions.append([i.x, i.y])
            t_paint.append(i.drawing_time)
            nt_paint.append(i.not_drawing_time)
        dict_to_return["names"] = names
        dict_to_return["colors"] = colors
        dict_to_return["points"] = points
        dict_to_return["positions"] = positions
        dict_to_return["paint"] = t_paint
        dict_to_return["no_paint"] = nt_paint
        return dict_to_return

    @staticmethod
    def update_position(position, paint, color):
        return {"action": "update_position", "position": position,
                "paint": paint, "color": color}

    def check_collision(self, names):
        """
         Este metodo asigna los puntajes, acorde a los nombres de los que
         chocaron, es decir, si viene solo un nombre entonces le suma 1 punto a
         todos, en cambio si vienen 2 le suma solo 2 puntos ya que le
         llegaran dos señales de cada colision (Ya que cada cliente informa
         su choque sin diferenciar si choco con un ratro o muralla o con un
         sprite
        """
        if len(names) == 1:
            if names[0] in self.players:  # Puede que se haya salido
                self.players[names[0]].is_alive = False
                for i in self.players:
                    if self.players[i].is_alive:
                        self.players[i].points += 1
        else:
            for i in names:
                if i in self.players:
                    self.players[i].is_alive = False
                self.solve_draw(*names)
                for i in self.players:
                    if self.players[i].is_alive:
                        self.players[i].points += 0.5
        return [player.points for player in self.players.values()]

    def check_winner(self, max_score):
        """
        Verifica si hay un ganador segun los dos criterios: un jugador
        alcanza el puntaje maximo o la diferencia entre el primero y el
        segundo es mayor o igual a 2
        """
        winners = []
        for i in self.players:
            if i in self.players:
                if self.players[i].points >= max_score:
                    winners.append(self.players[i])
        if winners:
            with alive_lock:
                self.is_alive = False
            return sorted(winners, key=lambda x: x.coins)[0].name
        else:
            player_list = sorted(list(map(lambda x: (x.name, x.points),
                                          self.players.values())),
                                 key=lambda x: x[1],
                                 reverse=True)
            if player_list[0][1] - player_list[1][1] >= 2:  # Se verifica que
                #  existan 2 puntos de ventaja
                with alive_lock:
                    self.is_alive = False
                return player_list[0][0]
        return False

    def ask_for_restart_round(self):
        """
        Retorna True en caso de que solo exista uno o ningun jugador vivo,
        con lo que indica que se debe iniciar una nueva ronda
        """
        players_alive = 0
        for i in self.players:
            if self.players[i].is_alive:
                players_alive += 1
        return players_alive <= 1

    def start_new_round(self):
        # Resetea el juego
        self.used_positions = set()
        self.set_initial_positions()
        for i in self.players:
            self.players[i].is_alive = True
        return self.get_game_information()

    def solve_draw(self, name_1, name_2):
        """
        Se encarga de en caso de dos jugafores chocar, ver quien se lleva un
        punto, primero aplica el criterio de darselo al menor puntaje,
        si estan empatados a las nebccoins y en caso de estar emptados en
        nebcoins se le asgina a lo que retorne como primero el sorted
        """
        if self.players[name_1].points != self.players[name_2].points:
            points_list = sorted([self.players[name_1], self.players[name_2]],
                                 key=lambda x: x.points)
            points_list[0].points += 0.5
        else:
            coin_list = sorted([self.players[name_1], self.players[name_2]],
                               key=lambda x: x.coins)
            coin_list[0].points += 0.5

    def power_up_tick(self):
        """
        Va mandando los poderes el tiempo que corresponde
        """
        while True:
            with alive_lock:
                if not self.is_alive:
                    break
            sleep(1)  # Se hace pasar un segundo
            self.current_time += 1
            if self.current_time >= self.power_up_time:
                new_power = choice(list(self.powers))
                position = (randint(50, 650), randint(50, 500))
                to_send = {"action": "new_power_up", "power_up": new_power,
                           "position": position}
                self.sender_function(to_send)
                self.current_time = 0

    def apply_trio_power(self):
        if len(self.powers) == 1:  # Si solo se juega con el poder de Felipe
            # del Trio no tiene caso mandar 3 de lo mismo
            return None
        powers = []
        for i in range(3):
            powers.append(choice(list(self.powers)))
        power_pos = []
        for i in powers:
            position = (randint(50, 650), randint(50, 550))
            while position in self.used_positions:
                position = (randint(50, 650), randint(50, 550))
            power_pos.append((i, position))
        return power_pos

    def add_nebcoin(self, name):
        self.players[name].coins += 1

    def withdraw_user(self, name):
        """
        Saca a un usuario, en caso de no quedar detiene el thread de mandar
        poderes, retorna True para indicar que el juego esta vacio
        """
        del self.players[name]
        if len(self.players) == 0:
            with alive_lock:
                self.is_alive = False  # Se termina el thread
            return True
