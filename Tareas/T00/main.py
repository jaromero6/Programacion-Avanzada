import interaccion as interact

if __name__ == "__main__":
    registro = interact.cargar_registro()
    usuario, accion = interact.menu_de_entrada(registro)
    interact.menu_de_correo(usuario, accion)
