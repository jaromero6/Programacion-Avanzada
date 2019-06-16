import socket
import threading as th
import pickle

HOST = 'DESKTOP-J6DHMFK'
PORT = 8081


class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = HOST
        self.port = PORT
        # Estas funciones se asginan en el backend
        self.log_in_function = None
        self.sign_in_function = None
        self.update_position_function = None
        self.uppdate_score_function = None
        self.join_function = None
        self.chat_function = None
        self.color_function = None
        self.update_window_function = None
        self.update_settings_function = None
        self.update_scores_function = None
        self.update_name_function = None
        self.counting_function = None
        self.start_game_function = None
        self.receive_game_settings_function = None
        self.pause_function = None
        self.show_new_power_up_function = None
        self.change_direction_function = None
        self.stop_turning_function = None
        self.apply_trio_function = None
        self.leader_command_function = None
        self.kill_player_function = None
        self.connected = True
        try:
            self.client_socket.connect((self.host, self.port))
            listen_thread = th.Thread(target=self.server_listener,
                                      daemon=True)
            listen_thread.start()

        except ConnectionRefusedError:
            self.stop_connection()

    def server_listener(self):
        while self.connected:
            try:
                print(f"Listen to server")
                lenght_message = self.client_socket.recv(4)
                lenght_message = int.from_bytes(lenght_message,
                                                byteorder="big")
                content_message = bytearray()
                while len(content_message) < lenght_message:
                    content_message += self.client_socket.recv(min(
                        lenght_message, 4096))
                print(content_message)
                decoded_message = pickle.loads(content_message)
                print("Receiving data .... handle data")
                self.handle_command(decoded_message)
            except ConnectionResetError:
                self.stop_connection()

    def handle_command(self, command):
        print("Working with the data ....")
        if command["action"] == "log_in":
            self.log_in_function(command["result"])
        elif command["action"] == "sign_in":
            self.sign_in_function(command["result"])
        elif command["action"] == "join":
            self.join_function(command["leader"], command["id_match"],
                               command["id_player"])
        elif command["action"] == "update_name":
            self.update_name_function(command["names"])
        elif command["action"] == "message":
            self.chat_function(command["all_messages"])
        elif command["action"] == "color":
            self.color_function(command["changes"], command["player"])
        elif command["action"] in ["speed", "score", "powers"]:
            self.update_settings_function(command["action"], command["value"])
        elif command["action"] == "update_window":
            self.update_window_function(command["names"], command["colors"],
                                        command["speed"], command["score"],
                                        command["powers"], command["leader"])
        elif command["action"] == "starting":
            self.counting_function(command["seconds"])
        elif command["action"] == "start_game":
            self.start_game_function(command["colors"])
        elif command["action"] == "game_settings":
            self.receive_game_settings_function(command["names"], command[
                "points"], command["positions"], command["colors"], command[
                                                    "paint"],
                                                command["no_paint"])
        elif command["action"] == "change_direction":
            self.change_direction_function(command["direction"], command[
                "name"])
        elif command["action"] == "new_leader":
            self.leader_command_function()
        elif command["action"] == "update_position":
            self.update_position_function(command["position"], command[
                "paint"], command["color"])
        elif command["action"] == "pause":
            self.pause_function()
        elif command["action"] == "kill_player":
            self.kill_player_function(command["name"])
        elif command["action"] == "update_score":
            self.update_scores_function(command["scores"], command["winner"],
                                        command["restart"])
        elif command["action"] == "new_power_up":
            self.show_new_power_up_function(command["power_up"], command[
                "position"])
        elif command["action"] == "stop_turning":
            self.stop_turning_function(command["name"])
        elif command["action"] == "trio":
            self.apply_trio_function(command["powers"])
        elif command["action"] in ["logout", "quit"]:
            self.stop_connection()

    def send(self, mensaje):
        """
        coded_message = json.dumps(mensaje)
        content_message = coded_message.encode("utf-8")
        lenght_message = len(content_message).to_bytes(4, byteorder="big")
        """
        coded_message = pickle.dumps(mensaje)
        # content_message = coded_message.encode("utf-8")
        length_message = len(coded_message).to_bytes(4, byteorder="big")
        self.client_socket.send(length_message + coded_message)

    def stop_connection(self):
        print("Finish connection")
        self.connected = False
        self.client_socket.close()
