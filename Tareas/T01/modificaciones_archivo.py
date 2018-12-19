import os


def verificar_existencia_de_archivos():
    if not os.path.exists("output.txt"):
        print("El archivo output.txt no existe, no se puede seleccionar esta "
              "accion")
        return False
    if not os.path.exists("numero_consulta.txt"):
        print("El archivo numero_consultas.txt no existe, no ser puede "
              "seleccionar esta accion")
        return False
    return True


def comprobar_input(accion, posibles_resultados, salida=None,
                    mensaje="Saliendo"):
    """
    :param accion:
    :param posibles_resultados:
    :param salida:
    :param mensaje:
    :return: Un input valido o salir en caso de que lo indique el input
    """
    if accion in posibles_resultados:
        return accion
    if accion == salida:
        print(mensaje, ".......")
        return "salir"
    print("Error : La accion ingresada no existe")
    return comprobar_input(input(), posibles_resultados, salida, mensaje)


def obtener_numero_consulta():
    with open("numero_consulta.txt") as archivo:
        return int(archivo.readline().strip())


def actualizar_numero_consulta(numero):
    with open("numero_consulta.txt", "w") as archivo:
        archivo.write(str(numero))


def escribir_nombre_consultas(nombre):
    with open("Nombre_consultas.txt", "a", encoding="utf-8-sig") as archivo:
        archivo.write(nombre)


def mostrar_nombre_consultas():
    with open("Nombre_consultas.txt", encoding="utf-8-sig") as archivo:
        c = 1
        for consulta in archivo:
            yield c, consulta.strip()
            c += 1


def guardar_archivo(nombre, resultado, tipo):
    with open("output.txt", "a", encoding="utf-8-sig") as archivo:
        numero = obtener_numero_consulta() + 1
        actualizar_numero_consulta(numero)
        archivo.write("-------------------- Consulta " + str(numero) + "\n")
        archivo.write(nombre)
        [archivo.write(str(i) + "\n") for i in resultado]
        escribir_nombre_consultas(nombre)
        archivo.write(str(tipo) + "\n")


def mostrar_archivo():
    nombre_cons = [i for i in mostrar_nombre_consultas()]
    [print(i[0], "-", i[1]) for i in nombre_cons]
    print("Seleccione el numero de la  consulta que desea desplegar, pulse -1 "
          "para cancelar")
    posibles = [str(i) for i in range(1, len(nombre_cons) + 1)]
    accion = comprobar_input(input(), posibles, "-1", "Cancelando ....")
    if accion == "salir":
        return "salir"
    [print(i) for i in mostrar_consulta_especifica(accion)]
    return mostrar_archivo()


def modificar_archivo():
    nombre_cons = [i for i in mostrar_nombre_consultas()]
    [print(i[0], "-", i[1]) for i in nombre_cons]
    print("Seleccione el numero de la consulta que desea eliminar, pulse 0 "
          "para borrarlas todas, para cancelar pulse -1")
    posibles = [str(i) for i in range(len(nombre_cons) + 1)]
    accion = comprobar_input(input(), posibles, "-1", "Cancelando ....")
    if accion == "salir":
        return "salir"
    eliminar_consultas(accion)
    modificar_archivo()


def mostrar_consulta_especifica(numero_cons):
    with open("output.txt", encoding="utf-8-sig") as archivo:
        consulta_correcta = False
        for i in archivo:
            if "-------------------- Consulta " + numero_cons == i.strip():
                consulta_correcta = True
            elif "-----" in i:
                consulta_correcta = False
            if consulta_correcta:
                yield i.strip()


def eliminar_consultas(numero_cons):
    if numero_cons == "0":
        print("Vaciando output.txt .............")
        with open("output.txt", "w", encoding="utf-8-sig") as archivo:
            pass
        print("Reinicindo numero_consulta.txt ...................")
        with open("numero_consulta.txt", "w") as archivo:
            archivo.write("0")
        print("Vaciando Nombre_consultas.txt")
        with open("Nombre_consultas.txt", "w") as archivo:
            pass
    else:
        modificar_parcialemente_archivo(numero_cons)


def modificar_parcialemente_archivo(numero_cons):
    guardar = [i for i in borrar_lineas_output(numero_cons)]
    copia = [i for i in borrar_nombre_consultas(numero_cons)]
    nuevo_num = modificar_numero()
    with open("output.txt", "w", encoding="utf-8-sig") as archivo:
        [archivo.write(i) for i in guardar]
    with open("Nombre_consultas.txt", "w", encoding="utf-8-sig") as archivo:
        [archivo.write(i) for i in copia]
    with open("numero_consulta.txt", "w") as archivo:
        archivo.write(nuevo_num)


def borrar_lineas_output(numero_cons):
    with open("output.txt", encoding="utf-8-sig") as archivo:
        eliminar, bajar_numero_cons = False, False
        for i in archivo:
            if "Consulta " + numero_cons in i.strip():
                eliminar = True
                bajar_numero_cons = True
            elif "-------------" in i.strip():
                eliminar = False
            if not eliminar:
                if bajar_numero_cons and "Consulta" in i.strip():
                    mantener = i.strip()[:29]
                    cambiar = str(int(i.strip()[29:]) - 1)
                    yield mantener + " " + cambiar + "\n"
                else:
                    yield i


def borrar_nombre_consultas(numero_cons):
    c = 1
    with open("Nombre_consultas.txt", encoding="utf-8-sig") as archivo:
        for i in archivo:
            if str(c) != numero_cons:
                yield i
            c += 1


def modificar_numero():
    with open("numero_consulta.txt") as archivo:
        return str(int(archivo.readline().strip()) - 1)
