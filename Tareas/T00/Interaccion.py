import sys
import correo as correo
import funciones_tarea as func
import eventos as event
from collections import deque


def cargar_registro():  # Carga los datos
    usuarios = func.cargar_usuarios()
    mails = func.cargar_mensajes()
    eventos = func.cargar_eventos()
    registro = {}
    for user in usuarios.keys():
        mensajes_usuario = deque()
        for i in mails[user]:
            m = correo.Mensaje(i.de, i.a, i.asunto, i.cuerpo, i.clasificacion)
            mensajes_usuario.append(m)
        eventos_user = {}
        for i in eventos[user]:
            e = event.Evento(i.creador, i.nombre, i.descripcion, i.invitados,
                             i.etiquetas, i.fin, i.inicio)
            eventos_user[i.nombre, i.inicio, i.fin] = e
        d_mail = user.split("@")
        registro_usuario = correo.Correo(d_mail[0], d_mail[1], usuarios[user],
                                         mensajes_usuario, eventos_user)
        registro[user] = registro_usuario
    return registro


def verificar_input(palabra, comprobante, igualdad=False):
    if palabra == "1" and not igualdad:
        return "1"
    if not igualdad:  # Verifica si palabra esta en comprobante
        while palabra not in comprobante:
            print(
                "Correo no existente: Ingrese su correo correctamente, "
                "si desea "
                "volver "
                "atras "
                "pulse 1")
            palabra = input()
            if palabra == "1":
                return "1"
    else:  # Comprueba si palabra es igual al comprobante
        while palabra != comprobante:
            print("Clave incorrecta, vuelve a intentarlo, si desea cancelar "
                  "pulse 1")
            palabra = input()
            if palabra == "1":
                return "1"
    return palabra


def comprobar_input_de_correo():
    direccion_correo = input()
    if direccion_correo != "1":
        if direccion_correo.count("@") == 1:
            partes_correo = direccion_correo.split("@")  # Ver supuesto 1
            if len(partes_correo[0]) >= 1 and (
                    ";" not in partes_correo[0]) and len(partes_correo[1]) >= 3:
                if "," not in partes_correo[0]:
                    if partes_correo[1].count(".") == 1:
                        proveedor = partes_correo[1].split(".")
                        if len(proveedor[0]) >= 1 and len(
                                proveedor[1]) >= 1:
                            return direccion_correo
        print("Direccion de correo no valida, ingrese nuevamente")
        return comprobar_input_de_correo()
    else:
        print("Accion cancelada")
        return "cancela"


def ingresar_al_correo(registro_usuarios):
    print(
        "Ingrese su direccion de correo electronico, para"
        " volver atras pulse 1: ")
    ingresar_usuario = verificar_input(input().strip(" "),
                                       registro_usuarios.keys())
    if ingresar_usuario == "1":
        return menu_de_entrada(registro_usuarios)
    else:
        print("Ingrese su clave")
        if verificar_input(input(), registro_usuarios[ingresar_usuario].clave,
                           True) != "1":
            return registro_usuarios[ingresar_usuario], mostrar_opciones()
        else:
            return menu_de_entrada(registro_usuarios)


def mostrar_opciones():
    print("Seleccione una accion")
    print("1- Ver bandeja de entrada")
    print("2- Ver calendario")
    print("- Pulse cualquier otra tecla para salir")
    return input()


def menu_de_entrada(
        registro_usuarios):  # Es el menu principal, solo desde
    #  aqui se puede finalizar el programa
    print("----------------------------------------------------------------")
    print("Bienvenido, por favor inicie sesion o registrese")
    print(
        "1- Iniciar sesion\n2- Registrarse\nPara salir pulsa "
        "cualquier otra tecla")
    opcion = input("Escoja una opcion: ")
    if opcion == "1":
        user, action = ingresar_al_correo(registro_usuarios)
        if action == "1" or action == "2":
            menu_de_correo(user, action, registro_usuarios)
            return menu_de_entrada(registro_usuarios)
        else:
            return menu_de_entrada(registro_usuarios)
    elif opcion == "2":
        registrarse(registro_usuarios)
    print("Saliendo del sistema ...")
    func.actualizar(registro_usuarios)
    print("Nos vemos")
    sys.exit()


def menu_de_correo(usuario_ingresado, accion_usuario,
                   registro_users):  # Viene y vuelve a menu de entrada
    if accion_usuario == "1":
        print("-------------------------------------------------------")
        usuario_ingresado.mostrar_bandeja_de_entrada(
            registro_users)  # Va a modulo correo
        print("Para ir a la bandeja de entrada pulse 1")
        print("Para mostrar el calendario pulse 2")
        print("Para salir y cerrar sesion pulse cualquier otra tecla")
        menu_de_correo(usuario_ingresado, input(),
                       registro_users)  # Va a modulo correo
    elif accion_usuario == "2":
        print("-----------------------------------------------------------")
        usuario_ingresado.mostrar_calendario(registro_users)
        print("Para ir a la bandeja de entrada pulse 1")
        print("Para mostrar el calendario pulse 2")
        print("Para salir y cerrar sesion pulse cualquier otra tecla")
        menu_de_correo(usuario_ingresado, input(), registro_users)
    else:
        return 0


def registrarse(registro_usuario):  # Vuelve a menu de entrada
    print("Ingrese su correo incluyendo su proveedor, ejemplo: example@uc.cl")
    print("Para cancelar pulse 1")
    usuario_registrar = comprobar_input_de_correo().strip(" ")
    if usuario_registrar == "cancela":
        return menu_de_entrada(registro_usuario)
    while usuario_registrar in registro_usuario.keys():
        print("El correo ya existe, ingrese nuevamente")
        usuario_registrar = comprobar_input_de_correo()
        if usuario_registrar == "cancela":
            return menu_de_entrada(registro_usuario)
    clave_1 = True
    clave_2 = False
    while clave_1 != clave_2:
        print(
            "Ingrese una clave, debe tener al menos 6 caracteres "
            "ni , o ;.Para cancelar pulse 1")
        clave_1 = input()
        if clave_1 == "1":
            print("Operacion cancelada")
            return menu_de_entrada(registro_usuario)
        if len(clave_1) < 6 or "," in clave_1 or ";" in clave_1:
            continue
        print("Confirme su clave")
        clave_2 = input()
        if clave_1 != clave_2:
            print(
                "Error, las claves no son inguales,"
                " por favor vuelva a intentarlo")
    direccion = usuario_registrar.split("@")
    nuevo_usuario = correo.Correo(direccion[0], direccion[1], clave_1, deque(),
                                  {})
    registro_usuario[usuario_registrar] = nuevo_usuario
    print("Bien, para confirmar que el registro ha sido existoso inicie sesion")
    return menu_de_entrada(registro_usuario)
