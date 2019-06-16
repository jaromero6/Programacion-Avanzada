"""
server.py -- un simple servidor
"""
import os
import pickle
from socket import socket

HOST = '127.0.0.1'


class Server:
    """
    Una clase que representa un servidor.
    """

    def __init__(self, port):
        self.host = HOST
        self.port = port
        self.client = None
        self.socket = socket()
        self.commands = {
            "ls": self.list_filenames,
            "download": self.send_file,
            "upload": self.save_file,
            "logout": self.disconnect,
        }

    def run(self):
        """
        Enciende el servidor que puede conectarse
        y recibir comandos desde un único cliente.
        """

        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print(f"Escuchando en {self.host}:{self.port}.")

        while self.client is None:
            self.client, _ = self.socket.accept()
            print("¡Un cliente se ha conectado!")

            while self.client:
                command, args = pickle.loads(self.receive())
                self.commands[command](*args)

        print("Arrivederci.")

    def send(self, message):
        """
        [COMPLETAR]
        Envía datos binarios al cliente conectado por el socket,
        cumpliendo con el protocolo establecido en el enunciado.
        """
        length_message = len(message)
        to_send = length_message.to_bytes(4, byteorder="big") + message
        self.client.sendall(to_send)

    def receive(self):
        """
        [MODIFICAR]
        Recibe datos binarios del cliente, a través del socket,
        cumpliendo con el protocolo establecido en el enunciado.
        """
        response_bytes_length = self.client.recv(4)
        response_length = int.from_bytes(response_bytes_length,
                                         byteorder="big")
        response = bytearray()
        while len(response) < response_length:
            response += self.client.recv(4096)
        return response



    def list_filenames(self):
        """
        [COMPLETAR]
        Envía al cliente una lista que contiene los nombres de
        todos los archivos existentes en la carpeta del servidor.
        """
        files_list = os.listdir(os.getcwd())
        self.send(pickle.dumps(files_list))

    def send_file(self, filename):
        """
        [COMPLETAR]
        Envía al cliente un archivo ubicado en el directorio del servidor.
        """
        with open(filename, "rb") as file:
            self.send(file.read())

    def save_file(self, filename):
        """
        [COMPLETAR]
        Guarda un archivo recibido desde el cliente.
        """
        response = self.receive()
        with open(filename, "wb") as file:
            file.write(response)

    def disconnect(self):
        self.client = None
        print("El cliente se ha desconectado.")


if __name__ == '__main__':
    port_ = input("Escriba el puerto: ")
    server = Server(int(port_))
    server.run()
