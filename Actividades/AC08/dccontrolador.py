from collections import Counter, namedtuple

###############################################################################
"""
Excepciones Personalizadas
Acá crea tus excepciones personalizadas
"""

###############################################################################
class RepeatedError(Exception):
    def __init__(self, elemento):
        super().__init__(f"{elemento} ya esta siendo utilizado")

class InconsistencyError(Exception):
    def __init__(self, carros):
        super().__init__("carros de compra de distintos supermercados")

class Producto:
    def __init__(self, nombre, precio_base, descuento=0):
        if 0 <= 100 * descuento <= 50:
            raise ValueError("descuento no está entre 0% y 50%")
        self.nombre = nombre
        self.precio_base_ = precio_base
        self.descuento_ = descuento

    @property
    def precio_base(self):
        return self.precio_base_

    @precio_base.setter
    def precio_base(self, valor):
        if valor < 0:
            raise ValueError("precio base menor que 0")
        self.precio_base = valor

    @property
    def descuento(self):
        return self.descuento_

    @descuento.setter
    def descuento(self, valor):
        if 0 <= 100 * valor <= 50:
            raise ValueError("descuento no está entre 0% y 50%")
        self.descuento = valor

    @property
    def precio(self):
        return self.precio_base * (1 - self.descuento)

    def __str__(self):
        porcentaje_descuento = self.descuento * 100
        return f'{self.nombre}: '\
                f'${self.precio_base} ({porcentaje_descuento}% dscto.)'

    def __repr__(self):
        return f'<Producto {self}>'


class Supermercado:
    CARCTERES_INVALIDOS = '-&%#@*()'

    def __init__(self, nombre):
        self.nombre = nombre
        self.catalogo = {}

    @property
    def productos(self):
        return self.catalogo.values()

    def agregar_producto(self, codigo, producto):
        prohibidos = "-&%#@*()"
        for i in prohibidos:
            if i in codigo:
                raise ValueError("codigo posee caracteres invalidos: {",i, "}")
        if codigo in self.catalogo:
            raise RepeatedError(codigo)

        self.catalogo[codigo] = producto

    def __getitem__(self, key):
        if not self.__contains__(key):
            raise KeyError("el producto no existe en el supermercado")
        return self.catalogo[key]

    def __contains__(self, producto):
        return producto in self.catalogo

    def __iter__(self):
        yield from self.catalogo.values()


class PedidoOnline:
    def __init__(self, supermercado, orden=None):
        self.supermercado = supermercado

        # orden puede ser un arreglo de elementos:
        # ['a', 'a', 'b', 'c', 'a', 'b'] => {'a': 3, 'b': 2, 'c': 1}
        # o un dict con los conteos
        # {'a': 3, 'b': 2, 'c': 1} => {'a': 3, 'b': 2, 'c': 1}
        self.orden = Counter(orden)

    def añadir_producto(self, producto, cantidad=1):
        if cantidad < 0:
            raise ValueError("cantidad menor que 0")
        self.orden[producto] += cantidad

    @property
    def productos(self):
        return self.orden.keys()

    @property
    def total(self):
        return sum(producto.precio * cantidad for producto, cantidad in self)

    def comprar(self, dinero):
        if dinero < self.total:
            print('Falta dinero, la compra no fue exitosa.')
            return

        print(f'Compra exitosa! (El Dr. H^4 aplaude silenciosamente).')
        self.orden.clear()
        return dinero - self.total  # vuelto

    def __add__(self, other):
        if self.supermercado != other.supermercado:
            raise InconsistencyError
        nueva_orden = self.orden + other.orden

        return PedidoOnline(self.supermercado, nueva_orden)

    def __iter__(self):
        yield from self.orden.items()

    def __contains__(self, producto):
        return producto in self.orden
