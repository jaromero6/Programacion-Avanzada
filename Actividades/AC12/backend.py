import json
import os
import os.path as path
import pickle

from clases import Comida, ComidaEncoder, Receta

BOOK_PATH = 'recetas.book'


class PyKitchen:
    def __init__(self):
        self.recetas = []
        self.comidas = []
        self.despachadas = []

    def cargar_recetas(self):
        '''Esta función se encarga de cargar el archivo recetas.book'''
        pass


    def guardar_recetas(self):
        '''Esta función se encarga de guardar las recetas (instancias), en el
        archivo recetas.book'''
        pass

    def cocinar(self):
        '''Esta funcion debe:
        - filtrar recetas verificadas
        - crear comidas a partir de estas recetas
        - guardar las comidas en la carpeta horno
        '''
        for i in self.recetas:
            if i.verificada:
                with open(f"horno/{i.nombre}.json", "w") as file:
                    file.write(json.dumps(Comida.de_receta(i)))


    def despachar_y_botar(self):
        ''' Esta funcion debe:
        - Cargar las comidas que están en la carpeta horno.
            Pro tip: string.endswith('.json') retorna true si un string
            termina con .json
        - Crear instancias de Comida a partir de estas.
        - Guardar en despachadas las que están preparadas
        - Imprimir las comidas que están quemadas
        - Guardar en comidas las no preparadas ni quemadas
        '''
        path = os.listdir("horno/")
        for i in path:
            if i.endswith('.json'):
                with  open(f"horno/{i}", "r") as file:
                    com = json.dump(i, file, cls=ComidaEncoder,
                                            indent=4)
                    if not com.preparado and not com.quemado:
                        self.comidas.append(com)

                    elif com.quemado:
                        print(com.nombre)
                    elif not com.quemado and com.preparado:
                        self.despachadas.append(com)


