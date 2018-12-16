# Tarea 1: Cruncher Flights :school_satchel:


**Dejar claro lo que NO pudieron implementar y lo que no funciona a la perfección. Esto puede sonar innecesario pero permite que el ayudante se enfoque en lo que sí podría subir su puntaje.**

## Consideraciones generales :octocat:

<La tarea ejecuta una o varias consultas (si es una basta con ingresarla
como diccionario, si son varias se deben ingresar como lista). Para cambiar tipo de
base de datos (large,small,medium) ir a la linea 10 del modulo funciones_aux.py
y modificar la variable **_PATH_** por la ruta que se desee usar. Además
si el output.txt está en blanco, debe existir el arhivo **_numero_consulta.txt_** y
debe tener un 0 escrito (En el último commit se sube este archivo en el formato que
corresponde).>


### Cosas implementadas y no implementadas :white_check_mark: :x:

* Parte <>Cargar Archivos>: Hecha completa
* Parte <>Consultas>: Hecha completa
* Parte <>Interaccion con Consola>: Hecha completa

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```collections```-> ```defaultdict,namedtuples / consultas.py```
2. ```datetime```-> ```datetime.strptime / funciones_aux.py```
3. ```math```-> ```asin,sin,cos,sqrt,radians / funciones_aux.py```
4. ```functools```-> ```reduce / funciones_aux.py,interaccion.py```
5. ```os```-> ```path.exist / interaccion.py, modificaciones_archivo.py```
...

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```interaccion ``` -> Hecha para < pedir inputs al usuario, ejecutarlos, y mostrar sus resultados.>
2. ```funciones_aux```-> Hecha para < cumplir con la filosofía "Do one Thing and Do it Well", estas funciones
tienen diversas funcionalidades que son aprovechadas por las funciones del módulo consultas.>
3. ```consultas ``` ->Hecha para < realizar las 11 consultas que se piden en el enunciado.>
4. ```modificaciones_archivo``` -> Hecha para < realizar las modificaciones correspondientes al archivo output.txt.>
5. ```iic2233_utils ``` -> Su utilizo la funcion parse para los inputs de consultas
...

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. <El programa solo prodrá leer outputs creados por este mismo, esto es por temas
de formato y de como este mismo al ir modificando el output.txt modifica a los archivos numero_Consulta.txt y
Nombre_consultas.txt/a>
2. <De acuerdo a lo mencianado en la issue 231 se asume que los argumentos de las consultas
estarán bien escritos/a>
3. < Los pasajeros que devuelve **_favourite_airport_** son aquellos que están tanto en el generador de **_Passengers_** como en **_Travels_**
 , del mismo modo solo se consideran los vuelos que estaban en Flights y en Travels/a>
4. <Para **_passenger_miles_** los pasajeros que no estén en travels, se considerará que recorrieron
0 millas, además no se considerarán viajes que contemplen vuelos con destino de llegada aeropuertos que no estén
en el generador de Airports/a>
5. <Para **_popular_airport_** se aplica la misma idea que en la consideración 3, solo se toman en cuenta
aeropuertos que están asociados a vuelos que vienen en viajes/a>
6. <Para los pasajeros que se consideran en **_airport_passengers_** se aplica la misma idea de a consideración 3/a>
7. <Para **_furthest_distance_** se aplica la misma idea que en la consideración 4/a>
8. <Se asume que en el caso de **_load_database_** para ingresar los viajes se usará solo la palabra
**_Travels_** y que el archivo asociado a este tendrá el nombre de **_flights_passengers.csv_**/a>
9. <Tener en cuenta que las consultas aproximadamente tardan entre 6 - 15 segundos si se usa la base de datos large./a>
10. <Tener en cuenta que para seleccionar la accion output.txt debe existir tanto el archivo **_output.txt_** y el archivo
**_numero_consulta.txt_**, además de solo usar archivos ouput.txt que sean generados por el prograna ( Ya que
Nombre_consultas.txt y numero_consulta.txt son modificados a partir de las modificaciones que se le hagan al output.txt)./a>
11. < En el módulo **_interacción_**, las lineas **_72,129,135_** contienen unos print que se usaron para testear las respectivas
funciones, sin embargo se me olvidó quitarlos al hacer el último commit de la tarea./a>


-------

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. (https://es.stackoverflow.com/questions/54979/c%C3%B3mo-obtengo-los-valores-de-un-diccionario-que-contiene-otro-dicccionario-en-py): este código obtiene las llaves de los diccionarios anidados dentro de otro cosa y está implementado en el archivo (interaccion.py) en las líneas 48-52



## Descuentos
La guía de descuentos se encuentra (link)[https://github.com/IIC2233/syllabus/blob/master/Tareas/Descuentos.md]