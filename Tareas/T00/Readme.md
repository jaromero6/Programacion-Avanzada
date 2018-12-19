# Tarea 0: DCCorreos :school_satchel:


## Consideraciones generales :octocat:

Para ir ejecutando acciones  se debe ir presionado la tecla que se indique para dicha accion.
Las instrucciones para cada parte siempre se muestran al inicio. La base de datos de la tarea deben
estar en la carpetas llamada "datos".

### Cosas implementadas y no implementadas :white_check_mark: :x:

* Parte Correos: Hecha completa
* Parte Eventos: Hecha completa
* Parte Encriptación: Hecha completa

**_En resumen, se cumple con todos los puntos de la pauta con ciertos supuestos los que se especifican en la seccion correspondiente_**
    ...

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```datetime```-> ```date.now(),date(),datetime.now() / datetime```
2. ```random```-> ```randint```
3. ``` sys ``` -> ```exit()```

...

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```correo```-> Contine a ```Correo```, ```Mensaje```,  tiene métodos que cumplen la parte de Correos
2. ```evento```-> Contiene a Evento, tiene metodos que cumplen con la parte Calendario
3. ```interaccion```-> Cumple con la parte de Registro e Inicio de sesión, se encarga de recibir la mayor parte de inputs del usuario
4. ```funciones_tarea```-> Contiene funciones que procesan los archivos de base de datos y funciones que ayudan al funcionamiento de otros modulos
5. ```encriptacion```-> Cumple con la parte de Encriptacion

...

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Los correos se ingresan solo con un @, además debe al menos haber una letra antes y despues del punto después del @, como en los correos
   que usamos a diario.
2. Se pueden añadir destinatarios que no existan, pero no les llegará ni aparecerán en la lista de destinatarios)
   ya que no seria coherente mostrar direcciones de correo no existentes, ademas si se envia un correo a una
  a una direccion que no existe y luego esta se registra, el correo aparecería lo que no tendria sentido.
3. Se realizó la misma consideración para eventos.
4. Para el filtro de eventos por fechas, se consideró que el input fuera solo dia/mes/año
    de modo que el filtro pueda ser más eficiente desde el punto de vista del usuario (Ya que sería
    incómodo seleccionar una hora exacta para filtrar).

5. Para el filtro de eventos por fechas, se consideran los eventos que tengan por fecha de inicio la que se
   indique y tengan por fecha de termino la que se indique, por ejemplo si se esta filtrando desde el 1/7/2018
   hasta el 1/8/2018 (solo eventos del mes de julio) y hay un evento que parte en julio, pero termina en septiembre
   entonces no se mostrará.
6. Para filtrar por clasificaciones, se debe ingresar la etiqueta de forma exacta.
7. Para filtrar por nombre basta con poner una parte del nombre de los correos que se quieren filtrar.
8. Los nombres y descripciones de los eventos no pueden tener coma, al igual que el asunto del correo, esto es para evitar errores en la lectura del archivo.
   El programa obligará a ingresar , en las partes anteriormente descritas.
9. Al momento de escribir una direccion de correo en cualquier parte del programa, se le quitaran los espacios
     en blanco a la izquierda y a la derecha.
10. Al crear un evento y haber realizado filtro previamente este no se mostrará(aunque cumpla con los requisitos del filtro)
    para que se muestre se debe volver atras y mostrar

...

PD: < **Recalcar que eventos y mensajes que no involucren a destinatarios existentes no se podrán crear / enviar, al menos uno de los destinatarios debe existir, los que se ingresen y no existan no serán tomados en cuenta.**>


-------

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:

1. (http://pyspanishdoc.sourceforge.net/lib/built-in-funcs.html): este tranforma de ascii a carácter y viceversa  y está implementado en el archivo (encriptacion.py) en las líneas (7,134)
2. (https://www.programiz.com/python-programming/methods/built-in/bin) : tranforma de binario a entero y viceversa y está implementado en el archivo (encriptacion.py) en lineas (8, 133)
3 .(https://docs.python.org/2/library/datetime.html) : Se usa para trabajar con fechas y está implementado en el modulo (eventos.py) lineas (155,156,159,160), (funciones_tarea.py) en lineas (68,133,149,150,154,155)




## Descuentos
La guía de descuentos se encuentra (link)[https://github.com/IIC2233/syllabus/blob/master/Tareas/Descuentos.md]