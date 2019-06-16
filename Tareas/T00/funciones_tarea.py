import datetime
from collections import defaultdict, namedtuple, deque
import encriptacion as encript


def existe(usuario, registro):  # Comprueba si el usuario existe
    return {usuario} <= set(list(registro.keys()))


def validar_fecha(default, filtro=False):  # Verifica si el input de una
    #  fecha es valido como input, se hace la distincion entre filtro = True
    #  si se esta llamando desde filtrar eventos (solo se requiere comprobar
    #  dia, mes y hora) y filtro = False requiere ademas especificar y validar
    #  la hora, default es un indicador que sirve para cuando se estan creando
    #  los eventos
    mes_dia = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30,
               10: 31, 11: 30, 12: 30}
    # Se especifica el input esperado
    if not filtro:
        print("Ingrese fecha en formato DD/MM/YYYY HH:MM:SS")
    else:
        print("Ingrese fecha en formato DD/MM/YYYY")
    date = input().strip(" ")
    if filtro and date.strip(" ") == "1":  # En caso que desee no filtrar
        return "1"
    if default and len(date) != 2:  # Si se ingresa la fecha mal al crear los
        #  eventos se devuelve 1 que indica que se le suma 1 hora a la fecha
        # inicial
        return "1"
    if len(date.split(" ")) != 2 and not filtro:
        print("Ingrese fecha en el formato pedido")
        return validar_fecha(default)
    if not filtro:
        fecha, tiempo = date.split(" ")[0].split("/"), date.split(" ")[1].split(
                        ":")  # Verifica formato
    else:
        fecha = date.strip(" ").split("/")
        tiempo = ["0", "0", "0"]
    if len(fecha) != 3 or len(tiempo) != 3:  # Verifica D/M/Y H/M/S
        if not filtro:
            print("Ingrese fecha en el formato pedido")
            return validar_fecha(default)
        else:
            if filtro and len(fecha) != 3:  # Verifica formato D/M/Y
                return ""
    if not 0 < len(fecha[0]) <= 2 or not 0 < len(fecha[1]) <= 2 or len(
            fecha[2]) != 4:  # Verifica que a lo mas existan dos caracteres
        # en la parte equivalente a dias y meses
        if not filtro:
            print("Ingrese fecha en el formato pedido")
            return validar_fecha(default)
        else:
            return ""
    if not 0 < len(tiempo[0]) <= 2 or not 0 < len(
            tiempo[1]) <= 2 or not 0 < len(tiempo[2]) <= 2 and not filtro:
        print("Ingrese fecha en el formato pedido")  # Se verifica formato
        # del tiempo H:M:S
        return validar_fecha(default)
    if (not fecha[0].isdigit()
            or not fecha[1].isdigit()
            or not fecha[2].isdigit()):  # Verifica que la fecha sean numeros
        if not filtro:
            print("Ingrese fecha en el formato pedido")
            return validar_fecha(default)
        else:
            return ""
    if (not tiempo[0].isdigit() or
            not tiempo[1].isdigit() or not tiempo[2].isdigit() and not filtro):
        print("Ingrese fecha en el formato pedido")
        return validar_fecha(default)
    if int(fecha[1]) not in mes_dia.keys():  # Se verifica que sea un mes valido
        if not filtro:
            print("El mes ingresado no existe")
            return validar_fecha(default)
        else:
            return ""
    if int(fecha[0]) not in list(range(1, mes_dia[int(fecha[1])] + 1)):
        if not filtro:
            print("El dia ingresado no existe")
            return validar_fecha(default)
        else:
            return ""
    if int(tiempo[0]) not in list(range(24)) or int(tiempo[1]) not in list(
            range(60)):
        print("Hora ingresada no existe, vuelva a intentarlo")
        return validar_fecha(default)

    if int(tiempo[2]) not in list(range(60)):
        print("Minutos ingresados no existen, vuelva a intentarlo")
        return validar_fecha(default)
    return date


def comprobar_fecha(fecha_act, hora_act, default=False):
    fecha = validar_fecha(default)
    if fecha == "1":
        print(
            "Error al ingresar fecha: Se le asignara 1 "
            "hora de duracion al evento")
        return 1
    fecha = fecha.split(" ")
    f_1 = fecha[0].split("/")
    f_2 = fecha[1].split(":")
    fecha_i = datetime.date(int(f_1[2]), int(f_1[1]), int(f_1[0]))
    if fecha_i < fecha_act:
        if int(f_2[0]) < hora_act.hour:
            print("Error al ingresar fecha,intente nuevamente")
            return comprobar_fecha(fecha_act, hora_act)
        elif int(f_2[0]) == hora_act.hour:
            if int(f_2[1]) < hora_act.minute:
                print("Error al ingresar fecha, intente nuevamente")
                return comprobar_fecha(fecha_act, hora_act)
            elif int(f_2[1]) == hora_act.minute:
                if int(f_2[2]) < hora_act.second:
                    print("Error al ingresar fecha, intente nuevamente")
                    return comprobar_fecha(fecha_act, hora_act)
    return " ".join(fecha)


def filtrar_eventos(
        eventos_user):  # Viene y se devuelve a mostrar calendario
    print(
        "A continuacion ingrese filtros,pulse 1 para desplegar todos los "
        "eventos, para cancelar pulse -1")
    print(
        "Si no desea filtrar por una caracteristica no "
        "complete nada en ese espacio")
    final = {}
    for i in eventos_user.keys():
        final[i] = eventos_user[i]
    print(
        "Ingrese filtro de fecha de inicio en formato DD/MM/YY\nSi esta "
        "no es valida no se tendra en cuenta para el filtro")
    # Filtro fecha de inicio -----------------------------------------------
    accion = validar_fecha(False, True)
    if accion == "1":
        return True
    elif accion == "-1":
        return False
    elif accion != "":
        final = filtrar_por_fecha(accion, final, True)
    print(
        "Ingrese filtro de fecha de termino en fomato DD/MM/YY\nSi esta no es "
        "valida no se tendra en cuenta para el filtro")
    # Filtro fecha de termino  ---------------------------------------------
    accion = validar_fecha(False, True)
    if accion != "" and accion != "1":
        final = filtrar_por_fecha(accion, final)
    print("Ingrese filtro por nombre, si deja el espacio en blanco no se "
          "aplicara este filtro")  #
    # Filtro por
    # nombre
    accion = input().strip(" ")
    if accion != "":
        final = filtrar_nombre(accion, final)
    print(
        "Ingrese filtro de etiquetas,si es mas de una separe por comas\nDeje "
        "el espacio en blanco para no apicar este filtro")
    # Filtro por etiquetas -----------------------------------------------------
    accion = input().strip(" ")
    if accion != "":
        final = filtrar_etiquetas(set(accion.split(",")), final)
    if final != {}:
        return final
    print(
        "No se ha podido encontrar lo que deseaba, "
        "por favor vuelva a intentarlo")
    return filtrar_eventos(eventos_user)


def converitr_fecha(x):
    fecha = [int(i) for i in x.split(" ")[0].split("/")]
    tiempo = [int(i) for i in x.split(" ")[1].split(":")]
    d = datetime.datetime(fecha[2], fecha[1], fecha[0], tiempo[0], tiempo[1],
                          tiempo[2])
    return d


def ordenar_eventos(eventos):
    l_llaves = list(eventos.keys())
    return sorted(l_llaves, key=lambda x: convertir_fechas(x[1]))


def filtrar_por_fecha(fecha, eventos, inicio=False):
    resultado = {}
    fecha = [int(h) for h in fecha.split("/")]
    for i in eventos.keys():
        if inicio:
            f_inicio = [int(j) for j in i[1].split(" ")[0].split("/")]
            if (datetime.date(f_inicio[2], f_inicio[1], f_inicio[0])
                    >= datetime.date(fecha[2], fecha[1], fecha[0])):
                resultado[i] = eventos[i]
        else:
            f_termino = [int(j) for j in i[2].split(" ")[0].split("/")]
            if (datetime.date(f_termino[2], f_termino[1], f_termino[0]) <=
                    datetime.date(fecha[2], fecha[1], fecha[0])):
                resultado[i] = eventos[i]
    return resultado


def filtrar_nombre(nombre, eventos):
    resultado = {}
    for i in eventos.keys():
        if nombre.lower() in i[0].lower():
            resultado[i] = eventos[i]
    return resultado


def filtrar_etiquetas(etiquetas, eventos):
    resultado = {}
    for i in eventos.keys():
        if etiquetas <= eventos[i].etiquetas:
            resultado[i] = eventos[i]
    return resultado


def mostrar_eventos(keys_eventos, eventos):  # Esta funcion se devuelve a
    # mostrar_calendario
    print(
        "Para seleccionar un evento pulse el numero correspondiente al evento")
    print("Para crear un evento pulse 0, para volver atras pulse otra tecla")
    c = 1
    mostrar = []
    print("  Nombre     |  Fecha Inicio    |    Fecha termino    |  Etiquetas")
    if len(eventos) == 0:
        print("No hay eventos para mostrar")
    for i in keys_eventos:
        print(str(c) + "-", eventos[i].nombre, "|", eventos[i].fecha_inicio,
              "|",  eventos[i].fecha_termino, "|", ",".join(eventos[
                                                                i].etiquetas))
        c += 1
        mostrar.append([i, eventos[i]])
    accion = input()
    if accion == "0":
        return -1, -1
    elif accion.isdigit():
        if 1 <= int(accion) <= len(eventos):
            return mostrar[int(accion) - 1]
    return -2, -2


def cargar_usuarios():
    usuarios_registrados = defaultdict(str)
    with open("datos/db_users.csv", encoding="utf-8") as archivo:
        lineas = archivo.readlines()
        for linea in lineas[1:]:
            datos_usuario = linea.strip().split(",")
            usuarios_registrados[datos_usuario[0]] = datos_usuario[1]
    return usuarios_registrados


def cargar_mensajes():
    mensajes_recibidos = defaultdict(deque)
    mail = namedtuple("mail", "de a asunto cuerpo clasificacion")
    with open("datos/db_emails.csv", encoding="utf-8") as archivo:
        lineas = archivo.readlines()
        for linea in lineas[1:]:
            datos_mail = linea.strip().split(",")
            if len(datos_mail) == 4:
                datos_mail.append("sin clasificacion")
            destinatarios = set(datos_mail[1].split(";"))
            recibido = mail(datos_mail[0], destinatarios, ",".join(datos_mail[
                                                          2:-2]),
                            datos_mail[-2], datos_mail[-1].split(";"))
            for i in destinatarios:
                if {i} <= set(list(mensajes_recibidos.keys())):
                    mensajes_recibidos[i].append(recibido)
                else:
                    mensajes_recibidos[i] = [recibido]
    return mensajes_recibidos


def cargar_eventos():
    eventos_invitados = defaultdict(tuple)
    d_eventos = namedtuple("d_eventos",
                           "creador nombre inicio fin "
                           "descripcion invitados etiquetas")
    with open("datos/db_events.csv", encoding="utf-8") as archivo:
        lineas = archivo.readlines()
        for linea in lineas[1:]:
            d_e = linea.strip().split(",")
            invitados = set(d_e[5].split(";"))
            etiquetas = set(d_e[6].split(";"))
            f_inicio = d_e[2].split(" ")[0].split("-")
            h_i = d_e[2].split(" ")[1].split(":")
            f_i = (
                f_inicio[2] + "/" + f_inicio[1] + "/" + f_inicio[0] + " " +
                h_i[0] + ":" + h_i[1] + ":" + h_i[2]
            )
            f_term = d_e[3].split(" ")[0].split("-")
            h_t = d_e[3].split(" ")[1].split(":")
            f_t = f_term[2] + "/" + f_term[1] + "/" + f_term[0] + " " + h_t[
                0] + ":" + h_t[1] + ":" + h_t[2]
            valor = d_eventos(d_e[0], d_e[1], f_i, f_t, d_e[4], invitados,
                              etiquetas)
            for i in invitados:
                if {i} <= set(eventos_invitados.keys()):
                    eventos_invitados[i].append(valor)
                else:
                    eventos_invitados[i] = [valor]
            if not {valor.creador} <= set(eventos_invitados.keys()):
                eventos_invitados[valor.creador] = [valor]  # En caso de que
                # el creador no este entre los invitados agrega su evento

    return eventos_invitados


def guardar_datos_user(datos_usuario):
    with open("datos/db_users.csv", "w", encoding="utf-8") as archivo:
        archivo.write("user,password\n")
        for i in datos_usuario.keys():
            datos = i + "," + datos_usuario[i].clave + "\n"
            archivo.write(datos)


def guardar_mails(datos_usuario):
    with open("datos/db_emails.csv", "w", encoding="utf-8") as archivo:
        archivo.write("from,to,title,body,clasification\n")
        guardados = set()
        for i in datos_usuario.keys():
            for j in datos_usuario[i].mensajes:
                para = ";".join(j.destinatarios)
                cuerpo = j.cuerpo
                clasif = ";".join(j.clasificacion)
                linea = (
                    j.de + "," + para + "," + j.asunto +
                    "," + cuerpo + "," + clasif + "\n"
                         )
                if not {linea} <= guardados:
                    archivo.write(linea)
                    guardados.add(linea)


def convertir_fechas(fecha):
    fecha_inicial = fecha.split(" ")
    fecha_2 = fecha_inicial[0].split("/")
    fecha_3 = fecha_inicial[1].split(":")
    tiempo_final = fecha_3[0] + ":" + fecha_3[1] + ":" + fecha_3[2]
    fecha_final = fecha_2[2] + "-" + fecha_2[1] + "-" + fecha_2[
        0] + " " + tiempo_final
    return fecha_final


def guardar_eventos(datos_usuario):
    with open("datos/db_events.csv", "w", encoding="utf-8") as archivo:
        archivo.write("owner,name,start,finish,description,invited,tags\n")
        guardados = set()
        for i in datos_usuario.keys():
            for j in datos_usuario[i].eventos.values():
                f_inicio = convertir_fechas(j.fecha_inicio)
                f_termino = convertir_fechas(j.fecha_termino)
                f_completa = f_inicio + "," + f_termino
                invitados = ";".join(j.invitados)
                etiquetas = ";".join(j.etiquetas)
                parte_final = j.descripcion + "," + invitados + "," + etiquetas
                linea = (j.creador + "," + j.nombre + "," + f_completa + ","
                                                                         "" +
                         parte_final + "\n")
                if not {linea} <= guardados:
                    archivo.write(linea)
                    guardados.add(linea)


def actualizar(datos):
    guardar_datos_user(datos)
    guardar_mails(datos)
    guardar_eventos(datos)
