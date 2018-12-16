"""
client.py -- un simple cliente
"""

import pickle
from socket import socket, SHUT_RDWR

HOST = '127.0.0.1'


"""
Al momento de hacer download se ejecuta el metodo pero el archivo no se envia
correctamente, esto genera un fallo si se quiere hacer luego upload a este 
archivo, sin embargo upload manda correctamente el archivo y este luego se 
puede descargar (la descarga tendra el problema menciondo)
"""

class Client:
    """
    Una clase que representa un cliente.
    """

    def __init__(self, port):
        self.host = HOST
        self.port = port
        self.socket = socket()
        self.connected = False

        # Este diccionario tiene los comandos disponibles.
        # Puedes modificarlo para agregar nuevos comandos.
        self.commands = {
            "help": self.help,
            "ls": self.ls,
            "logout": self.logout,
            "upload": self.upload,
            "download": self.download
        }

    def run(self):
        """
        Enciende el cliente que puede conectarse
        para enviar algunos comandos al servidor.
        """

        self.socket.connect((self.host, self.port))
        self.connected = True

        while self.connected:
            command, *args = input('$ ').split()
            function = self.commands.get(command)

            if function is None:
                print(f"El comando '{command}' no existe.")
                print("Escribe 'help' para obtener ayuda.")
            elif command == 'help':
                self.help()
            else:
                self.send(pickle.dumps((command, args)))
                function(*args)

    def send(self, message):
        """
        [MODIFICAR]
        Envía datos binarios al servidor conectado por el socket,
        cumpliendo con el protocolo establecido en el enunciado.
        """
        lenght = len(message).to_bytes(4, byteorder="big")
        self.socket.sendall(lenght + message)

    def receive(self):
        """
        [COMPLETAR]
        Recibe datos binarios del servidor, a través del socket,
        cumpliendo con el protocolo establecido en el enunciado.
        """
        length_message = self.socket.recv(4)
        length_message = int.from_bytes(length_message, byteorder="big")
        content_message = bytearray()
        while len(content_message) < length_message:
            content_message += self.socket.recv(4096)
        return content_message

    def help(self):
        print("Esta es la lista de todos los comandos disponibles.")
        print('\n'.join(f"- {command}" for command in self.commands))

    def ls(self):
        """
        [COMPLETAR]
        Este comando recibe una lista con los archivos del servidor.

        Ejemplo:
        $ ls
        - doggo.jpg
        - server.py
        """
        response = self.receive()  # Se obtiene la solicitud
        for i in pickle.loads(response):
            print(i)

    def upload(self, filename):  # No se implemento el bonus
        """
        [COMPLETAR]
        Este comando envía un archivo hacia el servidor.
        """
        with open(filename, "rb") as file:
                self.send(file.read())

    def download(self, *filename):  # Se implemento que se puedan mandar mas
        # de un archivo
        """
        [COMPLETAR]
        Este comando recibe un archivo ubicado en el servidor.
        """
        for i in filename:
            with open(i, "wb") as file:
                file.write(self.receive())
                #pickle.dump(self.receive(), file)

    def logout(self):
        self.connected = False
        self.socket.shutdown(SHUT_RDWR)
        self.socket.close()
        print("Arrivederci.")


if __name__ == '__main__':
    port_ = input("Escriba el puerto: ")
    client = Client(int(port_))
    client.run()
