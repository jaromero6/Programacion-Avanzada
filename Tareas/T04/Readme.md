# Tarea 4: DCCurve :school_satchel:


## Consideraciones generales :octocat:

<La logica del juego en si está bien implementada pero no va bien al implementar networking
lo que podría causar ciertos problemas a la hora de probar ciertas cosas como los poderes. El host se obtiene por
el metodo gethostname de socket, el server printa este host para poder copiar y pegarlo en el cliente.>
### Cosas implementadas y no implementadas :white_check_mark: :x:

* Parte <Redes<sub></sub>>: Hecha completa
* Parte <Interfaces<sub></sub>>: Hecha completa
* Parte <Juego<sub></sub>>: Hecha completa
* Parte <Poderes<sub></sub>>: Hecha completa
* Parte <Redes<sub></sub>>: Hecha completa
* Parte <Bonus<sub></sub>> : Se hicieron los poderes pero faltó el multijugador



## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```, para ejecutar el server
ir a la carpteta **server** y ejecutar el archivo ```server.py```


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```socket```-> Usada para las clases de los modulos ```server.py``` y ```client.py```
2. ```hashlib```-> ```encript / database_functions.py```
3. ```random``` -> ```randint, choice / game_server.py , ```
4. ```time``` ->   ```sleep / game_server.py, character.py```
5. ``` datetime``` -> ```datetime.now / user.py```
6. ```sys``` -> ```argv, __excepthook__ , exit/ main.py```
7. ```threading``` -> ```Thread, Lock  / character.py, game_server.py, client.py, server.py```
8. ```pyqt5``` -> Usado en todos los modulos de la carpeta ```game```
9. ```binascii``` -> ```hexlify, unhexlify / database_functions.py```
10. ```os``` -> ```exit / database_fucnitons.py```


...

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```server.py```-> Se encarga correr el programa del servidor
2. ```client.py``` -> Se encarga de recibi y eniviar datos al servidor
3. ```database_functions.py``` -> Se encarga de trabajar con el archivo user_informations.csv que es la base de datos del juego
4. ```match_organizer.py``` -> Se encarga de asignar clientes a cada sala de espera, de mandar y recibir informacion solo entre clientes
 de una misma sala de espera
5. ```game_server.py``` -> Se encarga de correr la parte del juego que debería ser igual para todos los usuarios, como por ejemplo el tiempo de los poderes
o de almacenar su puntaje o de asignar puntaje
6. ```pregame_windows.py``` -> Contiene todas las ventanas qe son antes del juego (Desde ventana de inicio hasta sala de espera)
7. ```game_window.py``` -> Contiene a la ventana del juego
8. ```user.py``` -> Contiene los backend correspondientes a las ventanas que estan en el archivo pregame_windows.py
9. ```game_user.py``` -> Es el backend de la sala de juego
10. ```character.py``` -> Se encarga de ejecutar las acciones del personaje en el juego, como doblar o avanzar
11. ```power_up.py``` -> Contiene la clase que representa los poderes del juego

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. <Se asume que el server siempre estará corriendo (Esto es que primero se correra el server y luego el main y siempre
que se corra el main es porque el server ya esta corriendo)/a>
2. <Se asumio que el poder de Fernando Atraviessa duraba 5 segundos/a>
3. <El host usado es lo que devuelve **socket.gethostname()** pero el servidor lo printea al inciarlo lo que permite saber si
el cliente está bien conectado/a>
4. <El programa no funciona correctamente al usar las flechas de direccion/a>
5. <El programa corre con lag al usar networikng si bien se ve todo sincronizado (Aunque muy pegado)
se recomienda para probar los poderes cambiar la **linea 154** del modulo match_organizer.py, a que sea > 0, para que se puede testear con
uno aunque en caso de perder el server se caerá (Ya que esa parte asume que hay mas de 1 jugador)/a>

...


-------



Para realizar mi tarea saqué código de:
Me base en lo que se mencionaban en los siguientes links
1. Timer en un juego: ttps://www.parallelcube.com/es/2017/10/25/por-que-necesitamos-utilizar-delta-time/
2. networking: http://www.pythondiario.com/2015/01/simple-programa-clienteservidor-socket.html
3. dibujar : https://stackoverflow.com/questions/47982140/pyqt5-add-line-one-by-one-using-a-pausehttps://stackoverflow.com/questions/47982140/pyqt5-add-line-one-by-one-using-a-pause
4. Uso de QImage : https://wiki.python.org/moin/PyQt/Painting%20an%20overlay%20on%20an%20image
5. Sha256  :https://www.programcreek.com/python/example/103982/sha3.sha3_256
6. Mantener tecla presionada : https://stackoverflow.com/questions/46489933/pyqt-keypressevent-and-keyreleaseevent-holding-press-without-debounce
7. Sprites de poderes : thenounproject.com
A esto se le añade la ayudantia de networking e interfaces.


## Descuentos
La guía de descuentos se encuentra (link)[https://github.com/IIC2233/syllabus/blob/master/Tareas/Descuentos.md]