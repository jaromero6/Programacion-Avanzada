import datetime
import funciones_tarea as func


class Evento:
    def __init__(self, creador, nombre, descripcion, invitados, etiquetas,
                 fecha_termino, fecha_inicio):
        self.creador = creador
        self.nombre = nombre
        self.descripcion = descripcion
        self.invitados = invitados
        self.etiquetas = etiquetas
        self.fecha_termino = fecha_termino
        self.fecha_inicio = fecha_inicio

    def __eq__(self, other):
        id_evento = self.nombre + self.fecha_inicio + self.fecha_termino
        id_other = other.nombre + other.fecha_inicio + self.fecha_termino
        return id_evento == id_other

    def mostrar_evento(self, user, registro):  # Se devuelve a
        # mostrar_calendario
        print("Creador:", self.creador)
        print("Nombre", self.nombre)
        print("Fecha Inicio:", self.fecha_inicio, "Fecha termino:",
              self.fecha_termino)
        no_mostrar = {"sin invitados", self.creador}
        mostrar = self.invitados - no_mostrar
        if len(mostrar) == 0:
            mostrar.add("sin invitados")
        print("Invitados:", ",".join(mostrar))
        print("Descripcion:\n" + str(self.descripcion))
        if self.creador == user:
            print("Seleccione una accion para el evento")
            print("1- Cambiar nombre")
            print("2- Invitar")
            print("3- Eliminar invitados")
            print("4- Cambiar descripcion")
            print("5- Cambiar fecha")
            print("6- Cambiar etiquetas")
            print("7- Eliminar evento")
            print("Otra tecla para volver atras")
            accion = input()
            if accion == "1":
                self.cambiar_nombre(registro)
            elif accion == "2":
                self.invitar(registro)
            elif accion == "3":
                self.eliminar_invitados(registro)
            elif accion == "4":
                self.editar_descricpcion(registro)
            elif accion == "5":
                self.editar_fecha(registro)
            elif accion == "6":
                self.cambiar_etiquetas(registro)
            elif accion == "7":
                accion = self.eliminar_evento(registro)
                if accion == 1:
                    return 1
        else:
            print("No tiene acciones disponibles, pulse una tecla "
                  "para volver atras")
            input()
        return 0

    def cambiar_nombre(self, registro, creacion=False):  # Viene de
        # mostrar_evento o de correo.crear_evento
        print("Ingrese el nuevo nombre")
        nombre = input()
        while len(nombre) <= 6 or len(nombre) >= 50 or "," in nombre:
            if "," not in nombre:
                print("El nombre debe tener mas de 6 caracteres y menos de 50")
            else:
                print("El nombre no puede llevar ,")
            nombre = input()
        for i in registro.values():
            #  Se comprueba que no exista un evento con el mismo nombre y fecha
            if (
                            (self.nombre, self.fecha_inicio,
                             self.fecha_termino) in
                            i.eventos.keys() and (nombre, self.fecha_inicio,
                                                  self.fecha_termino) in
                            i.eventos.keys()
            ):
                print("Error, ya existe un evento con ese nombre y tiene la "
                      "misma fecha de inicio y de termino, pulse una tecla "
                      "para continuar")
                input()
                return self.mostrar_evento(self.creador, registro)
        for i in registro.values():  # Una vez comprobado que es factible
            # hacer el cambio este se realiza
            if (
                        (self.nombre, self.fecha_inicio, self.fecha_termino)
                    in i.eventos.keys()):
                n_evento = Evento(self.creador, nombre,
                                  self.descripcion, self.invitados,
                                  self.etiquetas, self.fecha_termino,
                                  self.fecha_inicio)
                del i.eventos[self.nombre, self.fecha_inicio,
                              self.fecha_termino]
                i.eventos[nombre, self.fecha_inicio, self.fecha_termino] = \
                    n_evento
        self.nombre = nombre
        if not creacion:
            print("Listo")
            return self.mostrar_evento(self.creador, registro)

    def invitar(self, registro, creacion=False):  # viene de mostrar_evento o
        #  de correo.crear_evento
        print("Ingrese el nombre del usuario que desea invitar, separe por "
              "comas si es mas de 1, "
              "pulse 1 para cancelar: ")
        invitado = input()
        if invitado == "1" and not creacion:
            return self.mostrar_evento(self.creador, registro)
        elif invitado == "1" and creacion:
            return 0
        invitado = invitado.split(",")
        existen = False
        invitados_final = []
        while not existen:
            for i in invitado:
                if i != self.creador:
                    if func.existe(i.strip(" "), registro):  # Verifica que al
                        # menos uno exista y sea distinto del creador
                        invitados_final.append(i.strip(" "))
                        existen = True
            if not existen:
                print("Ninguno de los invitados ingresados existe, vuelva a "
                      "intentarlo, pulse 1 para cancelar"
                      )
                invitado = input()
                if invitado == "1" and not creacion:
                    return self.mostrar_evento(self.creador, registro)
                elif invitado == "1" and creacion:
                    return 0
                invitado = invitado.split(",")
                invitados_final = []
                existen = False
        # A este punto solo se llega si se va a agregar un invitado, por lo
        # que se retira el sin invitados
        if "sin invitados" in self.invitados:
            self.invitados.remove("sin invitados")
        for i in invitados_final:
            self.invitados.add(i)

        if not creacion:
            for i in registro.values():  # Se modifica el evento en cada uno de
                #  los registros de usuarios relacionados con este
                if ((self.nombre, self.fecha_inicio, self.fecha_termino) in
                        i.eventos.keys()):
                    n_evento = Evento(self.creador, self.nombre,
                                      self.descripcion, self.invitados,
                                      self.etiquetas, self.fecha_termino,
                                      self.fecha_inicio)
                    del i.eventos[self.nombre, self.fecha_inicio,
                                  self.fecha_termino]  # Se borra el actual
                    i.eventos[self.nombre, self.fecha_inicio,
                              self.fecha_termino] = n_evento
            print("Listo")
            return self.mostrar_evento(self.creador, registro)

    def eliminar_invitados(self, registro):  # Viene de mostrar_evento
        if len(self.invitados) > 0:
            print("Seleccione a quien quiere eliminar, "
                  "para cancelar pulse otra tecla")
            posibles_eliminados = []
            c = 1
            for i in self.invitados:
                if i != self.creador:
                    print(str(c) + "-", i)
                    c += 1
                    posibles_eliminados.append(i)
            eliminar = input()
            if eliminar.isdigit():
                if 1 <= int(eliminar) <= len(self.invitados):
                    self.invitados.remove(posibles_eliminados[int(eliminar)
                                                              - 1])
                    del registro[
                        posibles_eliminados[int(eliminar) - 1]
                    ].eventos[self.nombre, self.fecha_inicio,
                              self.fecha_termino]
                    for i in registro.values():  # Se modifica el evento en
                        # cada uno delos registros de usuarios relacionados
                        # con este
                        if ((self.nombre, self.fecha_inicio,
                             self.fecha_termino) in
                                i.eventos.keys()):
                            n_evento = Evento(self.creador, self.nombre,
                                              self.descripcion, self.invitados,
                                              self.etiquetas,
                                              self.fecha_termino,
                                              self.fecha_inicio)
                            del i.eventos[self.nombre, self.fecha_inicio,
                                          self.fecha_termino]  # Se borra
                            # el actual
                            i.eventos[self.nombre, self.fecha_inicio,
                                      self.fecha_termino] = n_evento
                    print("Usuario borrado")
        else:
            print("No tienes invitados")
        print("Pulse una tecla para continuar")
        input()
        return self.mostrar_evento(self.creador, registro)

    def editar_descricpcion(self, registro, creacion=False):  # Viene de
        # mostrat_evento o de correo.crear_evento
        print("Ingresa una nueva descripcion, esta no puede llevar comas")
        nueva_descripicion = input()
        while "," in nueva_descripicion:
            print("No puede llevar comas la descripcion")
            nueva_descripicion = input()
        if nueva_descripicion.strip(" ") == "":
            self.descripicion = "'sin descripcion'"
        else:
            self.descripcion = nueva_descripicion
        if not creacion:
            for i in registro.values():  # Se modifica el evento en cada uno de
                #  los registros de usuarios relacionados con este
                if ((self.nombre, self.fecha_inicio, self.fecha_termino) in
                        i.eventos.keys()):
                    n_evento = Evento(self.creador, self.nombre,
                                      self.descripcion, self.invitados,
                                      self.etiquetas, self.fecha_termino,
                                      self.fecha_inicio)
                    i.eventos[self.nombre, self.fecha_inicio,
                              self.fecha_termino] = n_evento  # Se
                    # actualiza

            print("Listo")
            return self.mostrar_evento(self.creador, registro)

    def editar_fecha(self, registro,
                     creacion=False):  # Viene de
        # mostrat_evento o de correo.crear_evento
        print("Ingrese fecha de inicio")
        f_inicio = func.comprobar_fecha(datetime.date.today(),
                                        datetime.datetime.now())
        hora, minuto, segundo = f_inicio.split(" ")[1].split(":")
        dia, mes, anio = f_inicio.split(" ")[0].split("/")
        print("Ingrese fecha de termino")
        f_1 = datetime.date(int(anio), int(mes), int(dia))
        f_2 = datetime.datetime(int(anio), int(mes), int(dia), int(hora),
                                int(minuto), int(segundo))
        f_termino = func.comprobar_fecha(f_1, f_2, True)
        if f_termino == 1:
            f_termino = (dia + "/" + mes + "/" + anio + " " +
                         str(int(
                             hora) + 1) + ":" + minuto + ":" +
                         segundo
                         )
        if not creacion:
            for i in registro.values():  # Se verifica que el evento no
                # exista en todos los usuarios
                if (self.nombre, f_inicio, f_termino) in i.eventos.keys():
                    print("Error, ya existe un evento con el mismo nombre y "
                          "las mismas fechas, no se ha podido modificar las "
                          "fechas. Pulse una tecla para continuar")
                    input()
                    return self.mostrar_evento(self.creador, registro)
            for i in registro.values():
                if ((self.nombre, self.fecha_inicio, self.fecha_termino) in
                        i.eventos.keys()):
                    n_evento = Evento(self.creador, self.nombre,
                                      self.descripcion, self.invitados,
                                      self.etiquetas, f_termino,
                                      f_inicio)
                    del i.eventos[self.nombre, self.fecha_inicio,
                                  self.fecha_termino]  # Se borra el actual
                    i.eventos[self.nombre, f_inicio,
                              f_termino] = n_evento
            print("Se ha cambiado la fecha de forma exitosa")
            self.fecha_inicio = f_inicio
            self.fecha_termino = f_termino
            return self.mostrar_evento(self.creador, registro)
        else:
            self.fecha_inicio = f_inicio
            self.fecha_termino = f_termino

    def cambiar_etiquetas(self, registro, creacion=False):  # Viene de
        # mostrat_evento o de correo.crear_evento
        if not creacion:
            print("Escriba las etquetas que quiere separadas por coma")
        else:
            print("Ingrese alguna etiqueta para su evento")
        n_etiquetas = input().split(",")
        for i in n_etiquetas:
            if i.strip(" ") != "":
                self.etiquetas.add(i.strip(" "))
        if "sin etiquetas" in self.etiquetas:
            self.etiquetas.remove("sin etiquetas")
        if not creacion:
            for i in registro.values():  # Se modifica el evento en cada uno de
                #  los registros de usuarios relacionados con este
                if ((self.nombre, self.fecha_inicio, self.fecha_termino) in
                        i.eventos.keys()):
                    n_evento = Evento(self.creador, self.nombre,
                                      self.descripcion, self.invitados,
                                      self.etiquetas, self.fecha_termino,
                                      self.fecha_inicio)
                    i.eventos[self.nombre, self.fecha_inicio,
                              self.fecha_termino] = n_evento  # Se
                    # actualiza el actual
            print("Listo")
            return self.mostrar_evento(self.creador, registro)

    def eliminar_evento(self, registro):  # Viene de mostrat_evento
        print("Pulse 1 para confirmar que desea eliminar este evento")
        accion = input()
        if accion == "1":
            return 1
        return self.mostrar_evento(self.creador, registro)
