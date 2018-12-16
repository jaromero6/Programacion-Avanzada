class Entidad:
    def __init__(self, rango, items):
        self.rango = rango
        self.items = items
        self.subordinados = []
        self.rangos_subordinables = set()
        self.afinidad_superiores = 0

    def obtener_jerarquia(self,entidad):
        rangos = ["general", "teniente", "mayor", "capitan", "soldado"]
        if self.rango != "soldado":
            entidad.rangos_subordinables.add(rangos[rangos.index(self.rango) + 1])
        for i in self.subordinados:
            i.obtener_jerarquia(self)

    def agregar_entidad(self, entidad, afinidad=0):
        # Caso base: Se debe agregar
        self.obtener_jerarquia(self)
        if entidad.rango not in self.rangos_subordinables:
            entidad.afinidad_superiores = afinidad
            self.subordinados.append(entidad)
            return True
        # Si no se busca el mejor
        mayor = 0
        mejor = None
        for i in self.subordinados:
            if entidad.rango in i.rangos_subordinables:
                if len(i.items & self.items) >= mayor:
                    mayor = len(i.items & self.items)
                    mejor = i
        if mejor is not None:
            return mejor.agregar_entidad(entidad,mayor)

    def obtener_poder(self,poder=0):
        poder += self.afinidad_superiores
        for i in self.subordinados:
            i.obtener_poder(poder)
        return poder


def cargar_datos(nombre):
    lista = []
    with open(nombre) as archivo:
        archivo.readline()
        [lista.append(i.strip().split(",")) for i in archivo]
    return lista

def armar_ejercito(lista):
    ent = Entidad(lista[0][0],set(lista[0][1:]))
    ent.obtener_jerarquia(ent)
    for i in lista:
        ent.agregar_entidad(Entidad(i[0],set(i[1:])))
    return ent

ej_1 = armar_ejercito(cargar_datos("ejercito_1.csv"))
for i in ej_1.subordinados:
    print(i.rango)
ej_2 = armar_ejercito(cargar_datos("ejercito_2.csv"))
ej_3 = armar_ejercito(cargar_datos("ejercito_3.csv"))
ej_4 = armar_ejercito(cargar_datos("ejercito_4.csv"))
print(ej_1.obtener_poder())
print(ej_2.obtener_poder())
print(ej_3.obtener_poder())
print(ej_4.obtener_poder())




    