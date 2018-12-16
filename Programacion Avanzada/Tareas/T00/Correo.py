import eventos as events
import funciones_tarea as func
import encriptacion as encript


class Correo:
    def __init__(self, nombre, proveedor, clave, mensajes, eventos):
        self.nombre = nombre
        self.proveedor = proveedor
        self.clave = clave
        self.mensajes = mensajes
        self.eventos = eventos

    def enviar_correo(self,
                      registro):  # Viene y vuelve a bandeja de entrada
        print(
            "Ingrese la direccion de correo electronico, si es mas de uno "
            "separelos por coma")
        mensaje = Mensaje(self.nombre, "", "",
                          "", ["sin clasificación"])
        destinatario = input().split(",")
        existe_uno = False
        dest_finales = []
        while not existe_uno:  # Verifica si al menos uno de los destinatarios
            # existe
            for i in destinatario:
                if func.existe(i.strip(" "), registro):
                    existe_uno = True
                    dest_finales.append(i.strip(" "))  # Se agregan solo los
                    # que
                    # existan
            if not existe_uno:
                print("Error, ningun destinatario es valido, ingrese "
                      "nuevamente")
                destinatario = input().split(",")
        print("Escribe el asunto del mensaje, no se permite el uso de comas")
        asunto = input()
        while len(asunto) > 50 or "," in asunto:
            if len(asunto) > 50:
                print("El asunto no puede exceder los 50 caracteres")
            if "," in asunto:
                print("El asunto no puede llevar comas")
            asunto = input()
        if asunto.strip(" ") == "":
            print("El asunto esta en blanco, se dejara como Sin asunto")
            asunto = "Sin asunto"
        print("Redacte el cuerpo del mensaje")
        cuerpo = input()
        while len(cuerpo) > 256:
            print(
                "El cuerpo no puede superar los 256 caracteres, "
                "vuelva a intentarlo")
            cuerpo = input()
        print(
            "Coloque etiquetas, deje en blanco si no desea poner etiquetas,"
            " se es mas de una separela por comas ")
        mensaje.poner_etiquetas()
        mensaje.destinatarios = dest_finales
        mensaje.asunto = asunto
        mensaje.cuerpo = encript.encriptar(cuerpo)
        todo_bien = "Se ha enviado todo correctamente"
        if dest_finales != destinatario:  # A algunos destinatarios no les llego
            todo_bien = (
                "Se ha enviado correctamente, aunque algunos "
                "destinatarios no existian")
        for i in dest_finales:  # Se manda el mensaje a cada usuario
            registro[i].mensajes.appendleft(mensaje)
        # La funcion informa si todos los usuarios existian o no
        return todo_bien

    def mostrar_bandeja_de_entrada(self,
                                   registro):  # Viene y vuelve a
        # interaccion.menu_de_correo
        print(
            "0- para enviar mensaje\nPara leer  un mensaje pulse el numero "
            "correspondiente al mensaje")
        print("Pulse otra tecla para volver atras")
        c = 1
        print("  Clasificaciones     |    Asunto")
        for i in self.mensajes:
            print(str(c), "-", ",".join(i.clasificacion), "|", i.asunto)
            c += 1
        if len(self.mensajes) == 0:
            print("No tiene mensajes")
        accion = input()
        if accion == "0":
            print(self.enviar_correo(registro))  # Va a enviar_corre
            print("Pulse una tecla para volver a la bandeja de entrada")
            input()
            self.mostrar_bandeja_de_entrada(registro)
        elif accion.isdigit():
            if 0 < int(accion) <= len(self.mensajes):
                print("De:", self.mensajes[int(accion) - 1].de)
                print("Para:",
                      ",".join(self.mensajes[int(accion) - 1].destinatarios))
                print("Asunto:", self.mensajes[int(accion) - 1].asunto)
                print(self.mensajes[int(accion) - 1].desplegar_texto())
                print("Para volver a la bandeja de entrada pulse una tecla")
                input()
                self.mostrar_bandeja_de_entrada(registro)
        return accion

    def mostrar_calendario(self,
                           registro):  # Viene y vuelve a
        # interaccion.menu_de_correo
        accion = func.filtrar_eventos(
            self.eventos)  # Se va a funciones.filtrar_eventos
        opcion = 0
        while accion and opcion == 0:
            if type(accion) == bool:
                if accion:
                    accion = self.eventos
            llave, respuesta = func.mostrar_eventos(
                func.ordenar_eventos(accion), accion)  # Se va a
            # funciones.mostrar_eventos
            if type(respuesta) != int:
                opcion = respuesta.mostrar_evento(
                    self.nombre + "@" + self.proveedor, registro)
                if opcion == 1:
                    for i in registro.values():
                        if llave in i.eventos.keys():
                            del i.eventos[llave]
                            print("Evento borrado exitosamente, pulse una "
                                  "tecla para continuar")
                            input()
                    return self.mostrar_calendario(
                        registro)  # Se vuelve a filtrar eventos
            else:
                if respuesta == -1:
                    self.crear_evento(registro)
                else:  # Viene de escoger eventos, vuelve a seleccionar
                    # bandeja o calendario
                    return 0

    def crear_evento(self, registro):
        creador_evento = self.nombre + "@" + self.proveedor
        invitados = set()
        invitados.add("sin invitados")
        invitados.add(self.nombre + "@" + self.proveedor)
        etiquetas = set()
        etiquetas.add("sin etiquetas")
        nuevo_evento = events.Evento(creador_evento, "", "sin descripcion",
                                     invitados, etiquetas, "", "")
        nuevo_evento.cambiar_nombre(registro, True)
        nuevo_evento.editar_descricpcion(registro, True)
        nuevo_evento.invitar(registro, True)
        nuevo_evento.cambiar_etiquetas(registro, True)
        nuevo_evento.editar_fecha(registro, True)
        llave = (
            nuevo_evento.nombre, nuevo_evento.fecha_inicio,
            nuevo_evento.fecha_termino
        )
        if llave in self.eventos.keys():
            print("Error el evento ya existe, no se ha podido crear")
        else:
            self.eventos[llave] = nuevo_evento
            for i in nuevo_evento.invitados:
                if i != "sin invitados":
                    registro[i].eventos[llave] = nuevo_evento
        print("Pulse una tecla para continuar")
        input()
        return 0


class Mensaje:
    def __init__(self, de, destinatarios, asunto, cuerpo, clasificacion):
        self.de = de
        self.destinatarios = destinatarios
        self.asunto = asunto
        self.cuerpo = cuerpo
        self.clasificacion = set(clasificacion)

    def desplegar_texto(self):
        return encript.desencriptar(self.cuerpo)

    def poner_etiquetas(self):
        lista_etiquetas = ["Destacado", "Importante", "Publicidad",
                           "Newsletter"]
        print("Para poner etiquetas a su mensaje, seleccione el numero "
              "asociado a esta, si desea mas de una separe los numeros por "
              "coma")
        c = 1
        for i in lista_etiquetas:
            print(c, "-", i)
            c += 1
        n_etiquetas = input().strip().split(",")
        for i in n_etiquetas:
            if i.isdigit():
                if 0 < int(i) <= len(lista_etiquetas):
                    self.clasificacion.add(lista_etiquetas[int(i) - 1])
        if len(self.clasificacion) >= 2 and "sin clasificación":
            self.clasificacion.remove("sin clasificación")
