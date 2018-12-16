# Tarea 2: DCCasino :school_satchel:


## Consideraciones generales :octocat:

<Descripción de lo qué hace y qué **_no_** hace la tarea que entregaron junto
con detalles de último minuto y consideraciones como por ejemplo cambiar algo
en cierta línea del código o comentar una función>

### Cosas implementadas y no implementadas :white_check_mark: :x:

* Parte Inicialiazación: Hecha completa
* Parte Entidades:Hecha completa
* Parte Actividades: Hecha completa
* Parte Estadisticas: Hecha completa

...

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```random```-> ```choice, choices, randint, uniform, normalvariate, triangular/ módulo : casino.py, clientes.py, personal.py, juegos.py, instalaciones.py```
2. ```names```-> ```get_full_name() / casino.py``` (**_debe instalarse_**)
3. ``` colections ``` -> ```deque() / juegos.py, instalaciones,py ```
...

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```clientes.py```-> Contine a ```Personas``` y  ```Humano``` que se encargan modelar el comportamiento de una persona, dándole una personalidad y vinculando a esta
con la interfaz
2. ```juegos.py```-> Contiene a ```Juegos``` y sus respectivas subclases que se encargan de modelar el funicionamiento de los juegos del
casino (ruleta y tragamonedas)
3. ```personal.py``` -> Contiene a ```Personal``` con sus subclases y a ```Admistracion```, ambas modelan el comportamiento de el personal del casino
4. ```instalaciones.py``` -> Contiene a ```Instalacion``` y sus subclases que se encargan de modelar el comportamiento de las instalaciones del casino
(restobar, tarot y baño), además se le añadiron las clases EspacioConversa y TiniIlPadrino que se encargan de modelar la acción de conversar y hablar con Tini respecivamente
5. ```parameters.py``` -> Contiene las constantes que se pueden ir modificar para crear distintas instancias de simulación
6. ```casino.py``` -> Contiene a ```Casino``` que junta a todas las clases y lleva a cabo la simulación
7. ```main.py``` -> Archovo donde se debe ejecutar la tarea
...

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. <Para la tarea se consideró un universo de clientes los cuales pueden entrar (Con una probabilidad p acorde al enunciado)
 y al salir del casino pueden volver a entrar, esto es para mantener un grupo de gente y no sobrepoblar la simulación /a>

2. <Los clientes que son expulsados cambian su decision a "retirarse" y se marchan como cualquier otro cliente ( aunque si se cuenta como razon
de salida que fue expulsado/a>
3. <Se consideró que así como los juegos/instalaciones tienen una capacidad máxima, tambien la tiene la cantidad de gente que está a esperando
a usar dicho juego/instalacion, simulando un poco lo que ocurre en la vida real al ir a un lugar con mucha gente esperando y decidir simplemente irse
del lugar/a>
4. <La gente al tomar una decisión no tiene conocimiento sobre que instalación/juego está funcionando o no, ya que no tendría como saberlo en la vida real
a no ser que vaya al lugar y vea que no funciona, es por esto que los clientes pueden decidir ir a un lugar que no funcione sin embargo al llegar a este deben decidir
otra vez/a>
5. <Al momento de asignar personal a la instalación se priorizán aquellas que no estén funcionando de modo de no tener por ejemplo 50 bartenders en un restobar
y tener todos los otros restobares cerrados/a>
7. <Cuando los clientes deciden ir a hablar con Tini il Padrino estos van hacia la posición 600,400 (Un poco más abajo y a la derecha del Tarot) y conversan con él/a>
8. <El espacio que se aprecia en la esquina superior derecha del casino corresponde a el EspacioConversa, los clientes que quieren conversar
van a este y relizan la accion/a>
9. <Al momento de realizar apuestas se consideró que el casino siempre tendría dinero poder pagar la apuesta./a>
10. <Se consideró que los clientes que se van y ya no tienen dinero, pueden volver a entrar, al poder "ir a buscar más dinero" una vez salen del casino/a>
11. <No se hace el gui.set_size ya que la disposición de los elementos se pensó con las figuras más pequeñas y al cambiarlo
todo se desproporciona ( Cuando se inicia sin el set_size hay que agrandar un poco la ventana que se abre porque queda una parte tapada).
12. <Se consideran tres razones de salidas: Personales (Simplemente deciden salir), Dinero ( Se quedan con dinero = 0) , Trampa (Fue descubierto haciendo tramapa por un dealer)
el total de estas razones se toma en cuenta respecto al total de salidas (ya que un cliente puede salir y entrar más de una vez) /a>
13. <El hablar con Tini il Padrino no se considera una ganancia para el casino, ya que se supone que este personaje es externo al casino y esas ganacias son de él/a>
14. <Un tick de la simulación equivale a un segundo en el casino/a>
15. <Se cuenta como gente que hizo trampa a la gente que decidió hacer trampa y no necesariamente a la que descubrienron/a>
16. <Para el calculo de las estadísticas se consideró que la ganancia del tragamonedas es solo el 10% que se va para el casino y el pozo no se consdieró, ya que este está destinado
a ser entregado como premio/a>
17. <Toda dinero que use el cliente dentro del casino se consideró como dinero que estos perdieron en este en la parte de estadísticas/a>
18. <En la estidística 9 se consideraron todas las intalaciones y todos los juegos del casino/a>
19. La simulación solo puede durar dias eneteros/a>.

...

PD: <una última consideración (de ser necesaria) o comentario hecho anteriormente que se quiera **recalcar**>


-------




## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1.



## Descuentos
La guía de descuentos se encuentra (link)[https://github.com/IIC2233/syllabus/blob/master/Tareas/Descuentos.md]