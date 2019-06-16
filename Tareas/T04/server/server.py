import socket
import threading as th
import pickle
from database_functions import check_correct_log_in, check_correct_sign_in
from match_organizer import MatchOrganizer


"""
Codigo hecho en base a los contenidos y ayudantia de la semama 13
Todos los mensajes que envia y recibe el diccionario son de la forma {
action:nombre, paramtetos} se hace algo de acuerdo al valor de action
"""


HOST = socket.gethostname()
print(HOST)
PORT = 8081


class Server:
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.bind((self.host, self.port))
        self.socket_server.listen(4)  # Maximo de ususarios por partida
        thread = th.Thread(target=self.accept_connection_thread, daemon=True)
        thread.start()
        self.sockets = {}
        self.organizer = MatchOrganizer(self.send)

    def accept_connection_thread(self):
        while True:
            client_socket, _ = self.socket_server.accept()
            print(f"Accepting connection {client_socket}, {_}")
            self.sockets[client_socket] = None
            listening_client_thread = th.Thread(
                target=self.listen_to_client,
                args=(client_socket,),
                daemon=True
            )
            listening_client_thread.start()

    def listen_to_client(self, client_socket):
        while client_socket in self.sockets:
            try:
                response_bytes_length = client_socket.recv(4)
                response_length = int.from_bytes(response_bytes_length,
                                                 byteorder="big")
                response = bytearray()
                while len(response) < response_length:
                    response += client_socket.recv(min(response_length, 4096))
                print(response)
                decoded = pickle.loads(response)
                print("Data received... Send to Handle data")
                self.handle_command(decoded, client_socket)
            except ConnectionResetError:
                exit()
                break

    def handle_command(self, response, sockt):
        print("Sending response ...")
        if response["action"] == "log_in":
            result = check_correct_log_in(response["username"], response[
                "password"])
            to_send = {"action": "log_in", "result": result}
            self.send(to_send, sockt)
        elif response["action"] == "sign_in":
            result = check_correct_sign_in(response["username"], response[
                "password"])
            to_send = {"action": "sign_in", "result": result}
            self.send(to_send, sockt)
        elif response["action"] == "enter":
            self.organizer.new_user(sockt, response["name"])
        elif response["action"] == "update_window":
            self.organizer.send_all_settings(response["match"])
        elif response["action"] == "update_name":
            self.organizer.set_new_name(response["name"], response["match"],
                                        response["player_id"])
        elif response["action"] == "message":
            self.organizer.new_message(response["content"], response["match"])
        elif response["action"] == "color":
            self.organizer.assign_color(response["color"], response["match"],
                                        response["player_id"])
        elif response["action"] == "speed":
            self.organizer.change_speed(response["speed"], response["match"])
        elif response["action"] == "power":
            self.organizer.change_powers(response["powers"], response["match"])
        elif response["action"] == "score":
            self.organizer.change_score(response["score"], response["match"])
        elif response["action"] == "start":
            self.organizer.start_count(response["match"])
        elif response["action"] == "start_game":
            self.organizer.open_game_window(response["match"])
        elif response["action"] == "change_direction":
            self.organizer.change_direction(response["direction"], response[
                "match"], response["name"])
        elif response["action"] == "stop_turning":
            self.organizer.stop_turning(response["name"], response["match"])
        elif response["action"] == "new":
            self.organizer.new_game(response["match"], sockt)
        elif response["action"] == "game_settings":
            self.organizer.send_game_settings(sockt, response["match"])
        elif response["action"] == "update_position":
            self.organizer.update_position(response["match"], response[
                "position"], response["paint"], response["color"])
        elif response["action"] == "pause":
            self.organizer.pause_game(response["match"])
        elif response["action"] == "collision":
            self.organizer.check_collision(response["name"], response["match"])
        elif response["action"] == "restart_game":
            self.organizer.restart_game(response["match"])
        elif response["action"] == "trio":
            self.organizer.send_triple_powers(response["match"])
        elif response["action"] == "add_nebcoin":
            self.organizer.add_nebcoin(response["match"], response["name"])
        elif response["action"] == "logout":
            self.organizer.logout_user(response["match"], sockt, response[
                "name"])
            self.send({"action": "quit"}, sockt)
            self.stop_connection(sockt)
        elif response["action"] == "quit":
            self.send({"action": "quit"}, sockt)
            self.stop_connection(sockt)

    @staticmethod
    def send(response, client):
        msg_bytes = pickle.dumps(response)
        msg_length = len(msg_bytes).to_bytes(4, byteorder="big")
        client.send(msg_length + msg_bytes)

    def stop_connection(self, sockt):
        del self.sockets[sockt]


server = Server()
while True:
    pass
