import os


def buscar_archivo(nombre, cwd=os.getcwd()):
    for i in os.walk(cwd, topdown=True):
        for j in i:
            if nombre in j:
                return i[0] + "\\" + nombre


def leer_archivo(path):
    with open(path, "rb") as file:
        letras = file.read()
        total = []
        c = 0
        while c < len(letras):
            par_byte = letras[c:c+2]
            bin_1, bin_2 = bin(par_byte[0]).replace("b",""), bin(par_byte[
                                                                     1]).replace("b","")
            bin_1 = bin_1.zfill(7)
            bin_2 = bin_2.zfill(7)
            total.append(bin_1 + bin_2)
            c+=2
    return total


def decodificar(bits):
    par = [bits[0], bits[1], bits[3], bits[7]]
    ind = [0, 1, 2, 3]
    pal = []
    inicio  = 0
    for i in ind:
        a = bits[inicio : 2 ** i]
        pal.append(a)
        inicio = 2 ** i






def escribir_archivo(ruta, chunks):
    pass


# Aquí puedes crear todas las funciones extra que requieras.


if __name__ == "__main__":
    nombre_archivo_de_pista = "himno.shrek"
    ruta_archivo_de_pista = buscar_archivo(nombre_archivo_de_pista)

    chunks_corruptos_himno = leer_archivo(ruta_archivo_de_pista)

    chunks_himno = [decodificar(chunk) for chunk in chunks_corruptos_himno]

    nombre_ubicacion_himno = "himno.png"
    escribir_archivo(nombre_ubicacion_himno, chunks_himno)
