class Asiento:
    PRECIOS = {
        "Primera Clase": 1100.00,
        "Clase Media": 1050.00,
        "Clase Comercial": 1000.00
    }

    def __init__(
        self,
        numero,
        fila,
        columna,
        clase,
        tipoAsiento="Normal",
        precio=None,
        estado="Disponible"
    ):
        self.numero = numero
        self.fila = fila
        self.columna = columna
        self.clase = clase
        self.tipoAsiento = tipoAsiento
        self.estado = estado

        if precio is None:
            self.precio = self.calcularPrecio()
        else:
            self.precio = float(precio)

    def esVentanilla(self):
        return self.columna in (1, 6)

    def calcularPrecio(self):
        precioBase = self.PRECIOS[self.clase]

        if self.esVentanilla():
            return precioBase * 1.15

        return precioBase

    def seleccionar(self):
        if self.estado == "Disponible":
            self.estado = "Seleccionado"
            return True

        return False

    def liberar(self):
        if self.estado == "Seleccionado":
            self.estado = "Disponible"
            return True

        return False

    def ocupar(self):
        if self.estado == "Seleccionado":
            self.estado = "Ocupado"
            return True

        return False

    def informacion(self):
        precioBase = self.PRECIOS[self.clase]
        recargo = 15 if self.esVentanilla() else 0

        return {
            "asiento": self.numero,
            "clase": self.clase,
            "tipo": self.tipoAsiento,
            "precioBase": precioBase,
            "recargo": recargo,
            "precio": self.precio,
            "estado": self.estado
        }