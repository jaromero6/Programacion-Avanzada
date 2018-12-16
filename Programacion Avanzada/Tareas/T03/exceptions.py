class ElectricalOverload(Exception):
    def __init__(self, name_function, overload):
        super().__init__(f"ElectricalOverload : La accion {name_function} "
                         f"sobrecarga "
                         f"la red a {overload}")


class ForbbidenAction(Exception):
    def __init__(self, name_function, explanation):
        super().__init__(f"ForbbidenAction: Accion {name_function} no es "
                         f"posible debido "
                         f"a {explanation}")


class InvalidQuery(Exception):
    def __init__(self, explanation):
        super().__init__(f"InvalidQuery: {explanation}")
