<El algoritmo que usará esta tarea para calcular la demanda total será el algoritmo de DFS, aunque
se le harán algunas modificaciones para el correcto funcionamiento de este.
La idea consiste en llegar lo más profundo posible al grafo, lo que se hace principalmente mediante DFS.
Una vez se llega a lo más profundo se calcula la demanda energetica se necesita, en este paso pueden
dos casos/a>
* El nodo tiene solo un padre (No es colgado), entonces se retorna o se pasa al nodo de más arriba la potencia
total.
* El nodo tiene más de un padre (Es colgado), entonces se retorna la potencia dividida en el número de padres que tiene.


<Posterior a eso, se le añade a esta suma la pérdida de energía correspondiente al cable (Aún no decido si el cálculo de
la potencia périda por la resistencia del cable irá en el nodo hijo o en el nodo padre, pero el paso se que va despúes de obtener la
potencia que requiere el nodo desde el padre). Luego se aplica este procedimiento para todos los nodos hijos del nodo actual obteniendo una
suma de potencia total que requiere ese nodo, a esta se le añade además la potencia que requiere el nodo mismo y se repite el proceso
para los nodos que están más arriba, siempre retornando el valor de la potencia acumulada al nodo padre. Notar que para los nodos
que están colgados es necesario visitarlo una vez por cada padre que tenga (Es decir si un nooo colgado tiene 5 padres,
entonces hay que visitarlo 5 veces), ya que así nos aseguramos de mandar por cada rama del grafo la cantidad
necesario de potencia. El algoritmo debe preocuparse de:/a>
* No quedarse atrapado en loops de ida y vuelta entre dos nodos
* Ir acumulando la suma de potencias, dividiéndola en la cantidad de nodos padres

