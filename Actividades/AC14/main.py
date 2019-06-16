import json
import re
from time import sleep
import requests

from credenciales import API_KEY


API_URL = "https://api.nasa.gov/planetary/apod"
DIR_IMAGENES = 'imagenes'
PATH_RESULTADOS = 'resultados.txt'


def limpiar_fecha(linea):
    '''
    Esta función se encarga de limpiar el texto introducido a las fechas

    :param linea: str
    :return: str
    '''
    filtrado = re.sub("</?[0-9a-zA-Z]+>", "",linea)
    return filtrado


def chequear_fecha(fecha):
    '''
    Esta función debe chequear si la fecha cumple el formato especificado

    :param fecha: str
    :return: bool
    '''
    pattern = "(^[0-9]{4}-[0-9]{2}-[0-9]{2}$)"
    return bool(re.match(pattern, fecha))



def obtener_fechas(path):
    '''
    Esta función procesa las fechas para devolver aquellas que son útiles
    para realizar las consultas a la API

    :param path: str
    :return: iterable
    '''
    with open(path) as file:
        for i in file:
            limpio = limpiar_fecha(i.strip())
            if chequear_fecha(limpio):
                yield limpio


def obtener_info(fecha):
    '''
    Recibe una fecha y retorna un diccionario
    con el título, la fecha y el url de la imagen
    :param fecha: str
    :return: dict
    '''
    response = requests.get("https://api.nasa.gov/planetary/apod",params={
        "date":fecha, "hd":False, "api_key":API_KEY})
    return response.json()

def escribir_respuesta(datos):
    with open("resultados.txt", "a+") as file:
        linea  = datos["date"] + "-->" + datos["title"] + ":" + datos["url"] \
                 + "\n"
        file.write(linea)
    descargar_imagen(datos["url"], "imagenes/" + datos["title"] + ".jpg")

    '''
    Esta función debe escribir las respuestas de la API en el archivo
    resultados.txt

    :param datos_respuesta: dict
    '''
    pass


def descargar_imagen(url, path):
    '''
    Recibe la url de una imagen y guarda los datos en un archivo en path

    :param url: str
    :param path: str
    '''
    respuesta = requests.get(url, stream=True)
    if respuesta.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in respuesta:
                f.write(chunk)


if __name__ == "__main__":
    PATH_FECHAS = 'fechas_secretas.txt'

    for fecha in obtener_fechas(PATH_FECHAS):
        respuesta = obtener_info(fecha)
        escribir_respuesta(respuesta)
