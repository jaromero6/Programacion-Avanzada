import random


def aplicar_cifrado_cesar(texto):
    texto_final = ""
    for letra in texto:
        formato_ascii = ord(letra) + 10
        notacion_binaria = bin(formato_ascii).replace("b", "")
        while len(notacion_binaria) < 8:  # Se comprueba que el binario sea de
            #  8 cifras
            notacion_binaria = "0" + notacion_binaria
        if len(notacion_binaria) > 8:
            notacion_binaria = notacion_binaria[1:]
        texto_final += notacion_binaria
    return texto_final


def generar_cadena_inicio():
    cadena_aletoria = ""
    clave = "2233"
    cadena_de_inicio = clave
    agregar = 1
    for i in range(10):
        numero_aleatorio = str(random.randint(0, 9))
        cadena_aletoria += numero_aleatorio
    while len(cadena_de_inicio) != 256:
        if agregar == 0:
            cadena_de_inicio += clave
            agregar = 1
        else:
            cadena_de_inicio += cadena_aletoria
            agregar = 0
    return cadena_de_inicio, cadena_aletoria


def aplicar_cambio_de_orden(cadena):
    cadena_numeros = list(range(0, 256))
    cadena_inicio = list(cadena)
    c = 0
    while c <= 255:
        indice_a_cambiar = c + int(cadena_inicio[c])
        if indice_a_cambiar > 255:
            indice_a_cambiar -= 256
        aux = str(cadena_numeros[c])
        #  Se realiza el intercambio
        cadena_numeros[c] = str(cadena_numeros[indice_a_cambiar])
        cadena_numeros[indice_a_cambiar] = aux
        c += 1
    final = []
    for i in cadena_numeros:  # Se pasa a binario
        num_bin = bin(int(i)).replace("b", "")
        #  Se comprueba que sea de largo 8
        while len(num_bin) < 8:
            num_bin = "0" + num_bin
        if len(num_bin) > 8:
            num_bin = num_bin[1:]
        final.append(num_bin)
    return "".join(final)  # Se retorna un string de largo 2048


def generar_mensaje_codificado(mensaje, cadena_numeros):
    #  Compara la cadena del asunto con la cadena obtenida al aplicar la
    # funcion cambio de orden
    c = 0
    mensaje_final = ""
    for i in mensaje:
        if i == cadena_numeros[c]:
            mensaje_final += "0"
        else:
            mensaje_final += "1"
        c += 1
    # retorna el mensaje codificado
    return mensaje_final


def encriptar(texto):  # Retorna el mensaje a enviar
    codificacion_m = aplicar_cifrado_cesar(texto)
    cadena_i, cadena_aleatoria = generar_cadena_inicio()
    codificado = generar_mensaje_codificado(codificacion_m,
                                            aplicar_cambio_de_orden(cadena_i))
    enviar = cadena_aleatoria + codificado
    return enviar


def recuperar_cadena_de_inicio(mensaje_encriptado):
    cadena_inicio = "2233" + mensaje_encriptado[0:10]
    c = 0
    while len(cadena_inicio) != 256:  # Se alterna clave - cadena aleatoria
        if c == 0:
            cadena_inicio += "2233"
            c = 1
        else:
            cadena_inicio += mensaje_encriptado[0:10]
            c = 0
    return cadena_inicio


def recuperar_cadena_de_numeros(mensaje_encriptado):
    #  Retorna el string de 2048 cifras que se uso para encriptar el mensaje
    cadena_de_inicio = recuperar_cadena_de_inicio(mensaje_encriptado)
    return aplicar_cambio_de_orden(cadena_de_inicio)


def recuperar_cadena_asunto(mensaje_encriptado, cadena):
    #  Dada la cadena de 2048 caracteres y el mensaje codificado retorna la
    # la cadena de asunto en binario
    cadena_asunto = ""
    c = 0
    for i in mensaje_encriptado[10:]:
        if i == "1":
            if cadena[c] == "0":
                cadena_asunto += "1"
            else:
                cadena_asunto += "0"
        else:
            cadena_asunto += cadena[c]
        c += 1
    return cadena_asunto


def quitar_cifrado_cesar(asunto_mensaje):
    #  Dada una cadena en binario, se fragementa en 8, se pasa a numero
    # entero cada secuencia,a ese numero se le resta 10 y se transforma de
    # ascci a caracter, con eso se recupera el mensaje original
    letras = []
    c = 8
    while c <= len(asunto_mensaje):
        caracter = asunto_mensaje[c-8:c]
        letras.append(caracter)
        c += 8
    asunto = ""
    for i in letras:
        formato_ascii = int(i, 2) - 10
        asunto += chr(formato_ascii)
    return asunto


def desencriptar(texto):
    cadena_numeros = recuperar_cadena_de_numeros(texto)
    cadena_asunto = recuperar_cadena_asunto(texto, cadena_numeros)
    texto_desencriptado = quitar_cifrado_cesar(cadena_asunto)
    return texto_desencriptado
