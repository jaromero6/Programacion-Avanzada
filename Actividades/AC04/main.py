from functools import reduce


class Aventurero:
    def __init__(self, nombre, vida, ataque, velocidad):
        self.nombre = nombre
        self.vida = vida
        self.ataque = ataque
        self.velocidad = velocidad

    def __str__(self):
        return "Nombre:" + self.nombre + ", Poder: " + str(self.poder())

    def __lt__(self, other):
        return self.poder() < other.poder()

    def __eq__(self, other):
        return self.poder() == other.poder()

    def __gt__(self, other):
        return self.poder() > other.poder()

    def grito_de_guerra(self):
        print(self.nombre, ":", "¡Gloria al gran Tini!")

    @property
    def poder(self):
        return self.vida + self.ataque + self.velocidad


class Guerrero(Aventurero):
    def __init__(self, nombre, vida, ataque, velocidad, defensa):
        super().__init__(nombre, vida, ataque, velocidad)
        self.defensa = defensa

    @property
    def poder(self):
        return 0.8 * self.vida + 2.2 * self.ataque + 1.5 * self.defensa + \
               1.4 * self.velocidad


class Mago(Aventurero):
    def __init__(self, nombre, vida, ataque, velocidad, magia):
        super().__init__(nombre, vida, ataque, velocidad)
        self.magia = magia

    @property
    def poder(self):
        return self.vida + 0.1 * self.ataque + 2.5 * self.magia + \
               1.4 * self.velocidad


class Monstruo:
    def __init__(self, nombre, vida, poder, jefe):
        self.nombre = nombre
        self.vida = vida
        self.jefe = jefe
        if jefe:
            self.poder_ = 3 * poder
        else:
            self.poder_ = poder

    def __str__(self):
        return self.nombre, self.poder_

    def __lt__(self, other):
        return self.poder() < other.poder()

    def __eq__(self, other):
        return self.poder() == other.poder()

    def __gt__(self, other):
        return self.poder() > other.poder()

    def poder(self):
        return self.poder_


class Clan:
    def __init__(self, nombre):
        self.nombre = nombre
        self.miembros = []
        self.rango = None

    def __str__(self):
        return self.nombre, self.poder, self.rango, len(self.miembros)

    def __add__(self, other):
        if isinstance(other, Clan):
            nuevo_clan = Clan(self.nombre + other.nombre)
            nuevo_clan.miembros = self.miembros + other.miembros
            nuevo_clan.rango_()
            return nuevo_clan

    def agregar(self, miembro):
        if isinstance(miembro, Aventurero):
            self.miembros.append(miembro)
            self.rango_()

    def rango_(self):
        if len(self.miembros) <= 2:
            self.rango = "Bronce"
        elif len(self.miembros) <= 5:
            self.rango = "Plata"
        else:
            self.rango = "Oro"

    def __lt__(self, other):
        return self.poder() < other.poder()

    def __eq__(self, other):
        return self.poder() == other.poder()

    def __gt__(self, other):
        return self.poder() > other.poder()

    def remover(self, other):
        if other in self.miembros:
            self.miembros.pop(self.miembros.index(other))

    @property
    def poder(self):
        if self.rango == "Bronce":
            ponderador = 0.5
        elif self.rango == "Plata":
            ponderador = 0.75
        else:
            ponderador = 1.2
        if len(self.miembros) > 1:
            return reduce(lambda x, y: ponderador * (x.poder() + y.poder()),
                          self.miembros)
        return self.miembros[0].poder * ponderador


class Mazmorra(Clan):
    def __init__(self, nombre):
        super().__init__(nombre)

    def __add__(self, other):
        if isinstance(other, Mazmorra):
            nuevo_clan = Mazmorra(self.nombre + other.nombre)
            nuevo_clan.miembros = self.miembros + other.miembros
            nuevo_clan.rango_()
            return nuevo_clan

    def agregar(self, miembro):
        if isinstance(miembro, Monstruo):
            super().miembros.append(miembro)
            super().rango_()
