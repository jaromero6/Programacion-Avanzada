from collections import namedtuple
from statistics import mean
from functools import reduce
# NO MODIFICAR ESTA FUNCION
def foreach(function, iterable):
    for elem in iterable:
        function(elem)


# Named tuples para cada entidad
Ciudad = namedtuple("Ciudad", ["sigla_pais", "nombre"])
Pais = namedtuple("Pais", ["sigla", "nombre"])
Persona = namedtuple("Persona", [
    "nombre", "apellido", "edad", "sexo", "ciudad_residencia",
    "area_de_trabajo", "sueldo"
])

###########################


def leer_ciudades(ruta_archivo_ciudades):
    with open(ruta_archivo_ciudades, encoding="utf-8") as archivo:
        for i in archivo:
            yield Ciudad(*i.strip().split(","))

    '''
    :param ruta_archivo_ciudades: str
    :return: generador
    '''


def leer_paises(ruta_archivo_paises):
    with open(ruta_archivo_paises, encoding="utf-8") as archivo:
        for a in archivo:
            yield Pais(*a.strip().split(","))
    '''
    :param ruta_archivo_paises: str
    :return: generador
    '''

def bastardo(a):
    with open(a, encoding="utf-8") as arc:
        return arc.readlines()

def leer_personas(ruta_archivo_personas):
    with open(ruta_archivo_personas,"r",encoding="utf-8") as archivo:
        for i in archivo:
            yield Persona(*i.strip().split(","))
    '''
    :param ruta_archivo_personas: str
    :return: generador
    '''


def sigla_de_pais(nombre_pais, paises):
    resultado = list(filter(lambda x: nombre_pais == x.nombre, paises))[0]
    '''
    :param nombre_pais: str
    :param paises: iterable de Paises (instancias)
    :return: sigla correspondiente al pais nombre_pais: str
    '''
    return resultado.sigla


def ciudades_por_pais(nombre_pais, paises, ciudades):
    sigla = sigla_de_pais(nombre_pais, paises)
    return filter(lambda x: x.sigla_pais == sigla, ciudades)


def personas_por_pais(nombre_pais, paises, ciudades, personas):
    ciud = list(ciudades_por_pais(nombre_pais, paises, ciudades))
    return filter(lambda x,y: x.nombre == y.ciudad_residencia,ciud)



def sueldo_promedio(personas):
    return mean(map(lambda x:int(x),map(lambda x:x.sueldo,personas)))


def cant_personas_por_area_de_trabajo(personas):
    trabajos = {}
    for i in personas:
        if i.area_de_trabajo in trabajos.keys():
            trabajos[i.area_de_trabajo] += 1
        else:
            trabajos[i.area_de_trabajo] = 1
    return trabajos


if __name__ == '__main__':
    RUTA_PAISES = "Paises.txt"
    RUTA_CIUDADES = "Ciudades.txt"
    RUTA_PERSONAS = "Personas.txt"
    # (1) Ciudades en Chile
    ciudades_chile = ciudades_por_pais('Chile', leer_paises(RUTA_PAISES),
                                       leer_ciudades(RUTA_CIUDADES))
    foreach(lambda ciudad: print(ciudad.sigla_pais, ciudad.nombre), ciudades_chile)

    # (2) Personas en Chile
    personas_chile = personas_por_pais('Chile', leer_paises(RUTA_PAISES),
                                       leer_ciudades(RUTA_CIUDADES),
                                       leer_personas(RUTA_PERSONAS))
    # foreach(personas_chile, lambda p: print(p.nombre, p.ciudad_residencia))

    # (3) Sueldo promedio de personas del mundo
    sueldo_mundo = sueldo_promedio(leer_personas(RUTA_PERSONAS))
    # print('Sueldo promedio: ', sueldo_mundo)

    # (4) Cantidad de personas por profesion
    dicc = cant_personas_por_area_de_trabajo(leer_personas(RUTA_PERSONAS))
    # foreach(lambda elem: print(f"{elem[0]}: {elem[1]}"), dicc.items())
