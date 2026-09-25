from datetime import datetime

class Venta:
    def __init__(self, asientos):
        self.asientos = asientos
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def calcularTotal(self):
        return sum(asiento.precio for asiento in self.asientos)
    
    def cantidadBoletos(self):
        return len(self.asientos)
    
    def resumen(self):
        return {
            "cantidad": self.cantidadBoletos(),
            "total": self.calcularTotal(),
            "fecha": self.fecha
        }