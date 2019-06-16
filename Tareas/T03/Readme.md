# Tarea 3: Electromatic :school_satchel:


## Consideraciones generales :octocat:

<Descripción de lo qué hace y qué **_no_** hace la tarea que entregaron junto
con detalles de último minuto y consideraciones como por ejemplo cambiar algo
en cierta línea del código o comentar una función>

### Cosas implementadas y no implementadas :white_check_mark: :x:

* Parte <Red<sub></sub>>: Hecha completa
* Parte <Calculo de potencia<sub></sub>>: Hecha completa
* Parte <Consultas<sub></sub>>: Hecha completa
* Parte <Excepciones<sub></sub>>: Hecha completa
* Parte <Testing<sub></sub>>: Hecha completa


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```csv```-> ```reader() / read.py```
2. ```unittest```-> ```assertEqual, assertRaises, TestCase / test.py```
3. ```math ``` -> ```inf / usert_interact.py, queries.py ```


### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```data_structures.py```-> Contiene las class **_List_**, **_IdList_**, **_Graph_**, que son las estructuras que
   se usaton para almacenar datos durantte toda la tarea.
2. ```exceptions.py``` -> Contiene las clases de la excpeciones que se pidieron para la tarea
3. ``` entities.py``` -> Contiene a la clase **_Entity_** y a todas sus subclases, que se encargan de modelar la red eléctrica
y cada entidad del grafo.
4. ```read_db.py``` -> Contiene las funciones necesarias para leer la base de datos y cargar el grafo
5. ``` queries.py``` -> Contiene las funciones que se encargan de ejecutar las consultas pedidas para la tarea.
6. ``` modification_system.py``` -> Contiene las funciones que se encargan de modificar la red acorde a lo pedido para esta tarea.
7. ``` user_interact.py``` -> Contiene las funciones que se encargan de pedir los inputs y ejecutar las acciones pedidas por el usuario.
8. ```test.py``` -> Se encarga de la parte de **_testing_**.
9. ```main.py``` -> Módulo principal de la tarea.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. <La parte de modificar de forma ficticia y real la red se interpretó como la forma ficticia comprueba si es posible el cambio
,en caso de ser posible se le pregunta si se quiere aplicar el cambio de forma permanente y se aplica en caso de ser necesario,
si no es posible el cambio se muestra el error de porque no se puede hacer/a>
2. <Se trabajó con las unidades en mW/a>
3. <Para la consulta de consumo total por comuna, se consideró como consumo lo que consume la entidad (dado por la base de datos) en caso de que
le llegue la suficiente energí, en caso contrario es lo que le llegó/a>
4. <Para el cliente con el mayor y menor consumo se consideró la energía total que les llega a cada consumidor/a>
5. <Se pueden siempre agregar nodos, siempre, ya que agregarlo lo único que hace es unirlo a la lista, pero este no lo dejará unirlo a la lista si la conexión no es posible ( y por ende
su demanda no afectará a la red y tampoco le llegara flujo). /a>
6. <No se verifica si se añade un nodo con una comuna que no exista, es decir es posible añadir un nodo de una comuna
que no exsite, pero si este es una casa por ejemplo no se podrá unir a nada, ya que no se permite unir casas de distintas comuna./a>
7. <Se asume que no se ingresaraán inputs que generen ciclos en la red./a>


## Descuentos
La guía de descuentos se encuentra (link)[https://github.com/IIC2233/syllabus/blob/master/Tareas/Descuentos.md]