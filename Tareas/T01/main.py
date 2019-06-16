from interaccion import menu_de_inicio
if __name__ == '__main__':
    try:
        while True:
            print("----------------- CRUNCHER FLIGHTS ------------------------")
            # rellenar esta parte con el llamado a sus funciones
            # sigue corriendo el uso restringido en toda situacion
            # de los for/while/etc dentro de este main a excepcion
            # del que se encuentra arriba, por lo que no se puede
            # agregar ninguno mas
            menu_de_inicio()

    # no es necesario que hagan una parte para salir del menu
    except KeyboardInterrupt():
        exit()
