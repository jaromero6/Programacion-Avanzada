from os import path, remove
from random import sample


# ------ Encriptación ------

def codificador(string):
    """
    Debe retornar el string codificado por la clave arquetipos.

    Usa funcional al programar esta función.
    """
    encrpt = dict(
        zip(list("arquetipos"), map(lambda x: str(x), list(range(10)))))
    desencrpt = dict(zip(list(encrpt.values()), list(encrpt.keys())))
    return "".join(list(map(lambda x: encrpt[x] if x in encrpt.keys() else
    desencrpt[
        x] if
    x in desencrpt.keys() else x, list(string))))


# ------ Decoradores -------


def pasaprogra(funcion):
    """Decorador que chequea si la persona respondió 'pasaprogra'."""

    def dec(*args, **kwargs):
        if args[0] == "pasaprogra":
            return args[0], 0
        else:
            return funcion(*args, **kwargs)

    return dec


def esconder_palabra(funcion):
    """
    Decorador que se encarga de esconder la palabra en la oración.

    La función 'camuflar', definida más abajo, te puede ser útil.
    """

    def dec(*args, **kwargs):
        for i in funcion(*args, **kwargs):
            yield i[0], i[1].replace("palabra", camuflar(i[0]))

    return dec


def desencriptar(funcion_decodificadora):
    """
    Decorador que permite desencriptar las palabras.

    La desencriptación requiere de una función decodificadora.
    """

    def dec1(funcion):
        def dec2(*args, **kwargs):
            for i in funcion(*args, **kwargs):
                yield funcion_decodificadora(i[0]), funcion_decodificadora(i[1])

        return dec2

    return dec1


def encriptar(funcion_codificadora):
    """
    Decorador para encriptar las respuestas de los jugadores y guardarlas.

    La encriptación requiere de una función codificadora.
    Las palabras encriptadas deben ser guardadas en 'resultados_encr.txt'.
    """

    def dec1(funcion):
        def dec2(*args, **kwargs):
            with open("resultados_encr.txt", "a", encoding="utf-8") as archivo:
                respuesta_encriptada = funcion_codificadora(args[0]) + "\n"
                archivo.write(respuesta_encriptada)
            return funcion(*args, **kwargs)
        return dec2
    return dec1


# ------------------------------------------------------------

# --------- NO MODIFICAR LAS FUNCIONES, SOLO DECORAR ---------

# ------------------------------------------------------------


def camuflar(palabra):
    """
    Devuelve una palabra con la mitad de sus letras,
    escogidas al azar, camufladas con guiones bajos.

    Utilízala en tus decoradores!

    Ejemplos:
    ========
    - 'hola': --> '_ol_'
    - 'mundo': ---> '_un__'
    - 'palabra': ---> '_a__br_'
    """
    muestra = sample(palabra, round(len(palabra) / 2))
    for letra in muestra:
        palabra = palabra.replace(letra, '_', 1)
    return palabra


@desencriptar(codificador)
def leer_archivo(ruta_archivo):
    """
    Esta función recibe una ruta (path) y retorna un generador con los datos.

    Nota que es cada línea se divide sólo con la primera coma, por lo que
    siempre hace yield de dos elementos.

    Decorar para:
    =============
    - Entregar los datos desencriptados.
    """
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            # ¿Por qué usar split con maxsplit=1?
            # Porque solo queremos dividir el string con la primera coma
            yield linea.strip().split(',', maxsplit=1)


@esconder_palabra
def juego_ahorcado(ruta_archivo_ahoracado):
    """
    Esta función generadora entrega las oraciones del juego ahorcado.

    Decorar para:
    =============
    - Esconder la palabra a adivinar dentro de la oración.
    """
    print('Juego: AHORCADO')
    print('En este juego se te dará una oración con una palabra',
          'incompleta que debes adivinar')
    yield from leer_archivo(ruta_archivo_ahoracado)
    print('-' * 80)


def juego_rosca(ruta_archivo_rosca):
    """
    Esta funcion genera las definiciones del juego rosca.

    Es una función generadora.
    """
    print('Juego: ROSCA')
    print('En este juego se te dará una definición y',
          'deberá adivinar la palabra asociada')
    yield from leer_archivo(ruta_archivo_rosca)
    print('-' * 80)


@encriptar(codificador)
@pasaprogra
def jugar(respuesta, palabra_correcta):
    """
    Esta función verifica si la respuesta es igual a la palabra correcta.

    Si la respuesta es correcta, entrega 1 punto. En caso contrario, -1.

    Decorar para:
    =============
    - Poder pasar y dar 0 puntos en ese caso.
    - Encriptar la respuesta.
    """
    if respuesta.lower() == palabra_correcta.lower():
        print(f"{respuesta}: Correcto! has ganado 1 punto :)")
        return respuesta, 1
    print(f"{respuesta}: Incorrecto! la respuesta era {palabra_correcta},",
          "has perdido 1 punto :(")
    return respuesta, -1


if __name__ == '__main__':
    # Limpia el archivo de resultados encriptados
    if path.exists('resultados_encr.txt'):
        remove('resultados_encr.txt')
    # Sigue con la ejecución
    RUTA_JUEGO_AHORCADO = 'ahorcado_encriptada.txt'
    RUTA_JUEGO_ROSCA = 'rosca_encriptada.txt'
    puntaje = 0
    nombre = input('Ingresa tu nombre: ')
    print(f'BIENVENIDO A PASAPROGRA {nombre}')

    for palabra_correcta, oracion in juego_ahorcado(RUTA_JUEGO_AHORCADO):
        print(f'Tienes {puntaje} puntos!')
        print(oracion)
        respuesta_jugador = input('Ingrese su respuesta: ')
        _, puntos_ganados = jugar(respuesta_jugador, palabra_correcta)
        puntaje += puntos_ganados

    for palabra_correcta, definicion in juego_rosca(RUTA_JUEGO_ROSCA):
        print(f'Tienes {puntaje} puntos!')
        print(definicion)
        respuesta_jugador = input('Ingrese su respuesta: ')
        _, puntos_ganados = jugar(respuesta_jugador, palabra_correcta)
        puntaje += puntos_ganados

    print(f"Terminaste con {puntaje} puntos")
