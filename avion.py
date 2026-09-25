from funciones import Asiento
from venta import Venta


class Avion:
    TOTAL_ASIENTOS = 90

    def __init__(self, dataBase):
        self.dataBase = dataBase
        self.asientos = {}
        self.cargarAsientos()

    def cargarAsientos(self):
        self.asientos.clear()

        for fila in self.dataBase.obtenerAsientos():
            asiento = Asiento(
                numero=fila["asiento"],
                fila=fila["fila"],
                columna=fila["columna"],
                clase=fila["clase"],
                tipoAsiento=fila["tipoAsiento"],
                precio=fila["precio"],
                estado=fila["estado"]
            )

            self.asientos[asiento.numero] = asiento

    def buscarAsiento(self, numero):
        return self.asientos.get(numero)

    def seleccionarAsiento(self, numero):
        asiento = self.buscarAsiento(numero)

        if asiento is None:
            return False

        if asiento.estado == "Ocupado":
            return False

        if asiento.estado == "Disponible":
            return asiento.seleccionar()

        if asiento.estado == "Seleccionado":
            return asiento.liberar()

        return False

    def obtenerSeleccionados(self):
        return [
            asiento
            for asiento in self.asientos.values()
            if asiento.estado == "Seleccionado"
        ]

    def cancelarSeleccion(self):
        for asiento in self.obtenerSeleccionados():
            asiento.liberar()

    def confirmarVenta(self):
        seleccionados = self.obtenerSeleccionados()

        if not seleccionados:
            raise ValueError("No hay asientos seleccionados")

        venta = Venta(seleccionados)

        self.dataBase.registrarVenta(venta)

        for asiento in seleccionados:
            asiento.ocupar()

        return venta

    def obtenerResumen(self):
        return self.dataBase.obtenerResumen()

    def todosOcupados(self):
        vendidos, _, _ = self.obtenerResumen()
        return vendidos == self.TOTAL_ASIENTOS