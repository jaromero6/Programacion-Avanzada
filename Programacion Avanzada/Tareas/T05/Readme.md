# Tarea 5: DCConnect :school_satchel:


## Consideraciones generales :octocat:

<La interaccion de la tarea se realiza mediante consola, los inputs que se revisan son los de correo, contraseña (No se deja
ingresar si escriben mal y los inputs de categorias (Si no existen se reemplazan por espacio vacio), mientras que los de descripción
del lugar no se revisan pero de ser algo inválido la consulta no arrojará resultados.
Antes de correr la tarea se debe rellenar las variables del archivo **settings.py**, de lo contrario el programa
no funcionará\>

### Cosas implementadas y no implementadas :white_check_mark: :x:

* Parte <Inicio de sesión<sub></sub>>: Hecha completa
* Parte <Flujo de informacion y consumo de API<sub></sub>>: Hecha completa
* Parte <Consola<sub></sub>>: Hecha completa


...

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```re```-> ```match, split / checker.py, mail_validation.py```
2. ```request```-> ```get / webservices.py``` (debe instalarse)
3. ```datetime``` -> ```datetime.srtptime/ interaction.py```

...

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```main.py```-> Módulo a ejecutar de la tarea.
2. ```interaction.py```-> Contiene las funciones que reciben inputs del usuario y muestran resultados.
3. ```mail_validation.py``` -> Contiene las funciones que validan correo y contraseña.
4. ```checker.py``` -> Contiene funciones que se encargan de validar ciertos inputs.
5. ```webservices.py``` -> Contiene funciones que se encargan de hacer consultas a cada API, además de encargarse
   del flujo de información.
6. ```settings.py``` -> Contiene las variables para poder hacer uso de cada API, se debe rellenar a mano, ya que todas las variables
 están en None lo que no dejaría funcionar el programa.

...

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. <El programa solo entrega viajes que lleguen de forma directa (No haciendo combinacion de viajes) /a>
2. <Modificar el return **get_current_position** del módulo **webservices.py** para poder obtener una posición
más precisa o donde sea más fácil testear./a>
3. <Se toman en cuenta solo paraderos y recorridos activos./a>
4. <Por temas de tiempo de ejecución del programa se puso un limit de 15 obtener 15 paraderos, ya que si eran más
se demora mucho en encontrar un paradero (Esto es porque se buscan todas las posibles combinaciones de los paraderos de inicio con los de destino, para aumentar
la posibilidad de que entregue un viaje el programa./a>
5. <Se usó un radio de 30 km desde las coordenadas -33.4372,-70.6506 que según Google son las del centro de Santiago y con el radio se espera
abarcar todo este. Si se quiere abarcar más espacio modificar la linea 18 del módulo **webservices.py**/a>
6. <La API del transantiago entregaba a veces un tiempo de viaje inconsistente, es decir, viajes que duraban muy poco en comparación con lo que entrega
Google Maps, sin embargo lo dejé así ya que no tenía forma de comrpbar que era un número válido y por otra parte los valores los entregaba la API (El programa
lo único que hace es ver el tiempo en que pasaba cada micro en el paradero de inicio y final, los transforma a
datetime y se restan./a>
7. <Las distancia que entrega el programa son en linea recta/a>
8. <Para las categorias se debe ingresar el nombre tal cual es, es decir aunque puede ser ya sea en su forma plural, abreviada o normal/a>
9. <Se considera un viaje que sirve solo si este pasa primero por donde esta el usuario y luego por el destino, es decir la opcion de tomar una micro llegar al terminal
y luego devolverse no fue considerada, sin embargo se exploran ambas posiblidades (Es decir, se ve por separado si le sirve el viaje de ida o el de vuelta)/a>
10. <Para el correo el punto cuenta dentro de los caracteres/a>
11. <Encontrar la ruta para el paradero le puede tomar unos cuantos minutos al programa (Los recorridos que probé se demoraba
de 1-3 minutos)/a>
...

PD: **Recalcar que antes de probar la tarea deben rellenar el archivo *_settings.py_*, de lo contrario la tarea no
funcionará**

-------


## Descuentos
La guía de descuentos se encuentra (link)[https://github.com/IIC2233/syllabus/blob/master/Tareas/Descuentos.md]