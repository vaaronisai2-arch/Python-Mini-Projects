import sqlite3

class BaseDatos:
    def __init__(self, nombre="avion.db"):
        self.nombre = nombre
        self.conectar()
        self.crearTablas()
        self.crearAsientos()
        
    def conectar(self):
        self.conexion = sqlite3.connect(self.nombre)
        self.conexion.row_factory = sqlite3.Row
    
    def crearTablas(self):
        cursor = self.conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS asientos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asiento TEXT UNIQUE NOT NULL,
                fila TEXT NOT NULL,
                columna INTEGER NOT NULL,
                clase TEXT NOT NULL,
                tipoAsiento TEXT NOT NULL,
                precio REAL NOT NULL,
                estado TEXT NOT NULL)''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventas(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asiento TEXT NOT NULL,
                precio REAL NOT NULL,
                fecha TEXT NOT NULL)''')
        
        self.conexion.commit()
        
    def crearAsientos(self):
        cursor = self.conexion.cursor()
        cursor.execute("Select COUNT(*) FROM asientos")
        cantidad = cursor.fetchone()[0]
        
        if cantidad > 0:
            return
        
        filas = "ABCDEFGHIJKLMNO"
        
        for fila in filas:
            for columna in range (1, 7):
                numero = f"{fila}{columna}"
                
                if fila in "ABC":
                    clase = "Primera Clase"
                elif fila in "DEFGHIJK":
                    clase = "Clase Media"
                else:
                    clase = "Clase Comercial"
                
                tipo = "Ventanilla" if columna in (1, 6) else "Normal"
                
                precioBase = {
                    "Primera Clase": 1100.00,
                    "Clase Media": 1050.00,
                    "Clase Comercial": 1000.00
                }[clase]
                
                precio = precioBase * 1.15 if tipo == "Ventanilla" else precioBase
                
                cursor.execute('''
                    INSERT INTO asientos
                    (asiento, fila, columna, clase, tipoAsiento, precio, estado)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''', (numero, fila, columna, clase, tipo, precio, "Disponible"))
                
        self.conexion.commit()
        
    def obtenerAsientos(self):
        cursor = self.conexion.cursor()
        cursor.execute("SELECT * FROM asientos ORDER BY id")
        return cursor.fetchall()
    
    def actualizarEstado(self, numero, estado):
        cursor = self.conexion.cursor()
        cursor.execute('''
            UPDATE asientos
            SET estado = ?
            WHERE asiento = ?''',
            (estado, numero))
        self.conexion.commit()
        
    def registrarVenta(self, venta):
        cursor = self.conexion.cursor()

        try:
            for asiento in venta.asientos:

                cursor.execute('''
                    UPDATE asientos
                    SET estado = "Ocupado"
                    WHERE asiento = ?
                    AND estado = "Disponible"
                ''', (asiento.numero,))

                if cursor.rowcount != 1:
                    raise ValueError(
                        f"El asiento {asiento.numero} ya está ocupado"
                    )

                cursor.execute('''
                    INSERT INTO ventas
                    (asiento, precio, fecha)
                    VALUES (?, ?, ?)
                ''', (
                    asiento.numero,
                    asiento.precio,
                    venta.fecha
                ))

            self.conexion.commit()

        except Exception:
            self.conexion.rollback()
            raise
        
    def obtenerResumen(self):
        cursor = self.conexion.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM asientos WHERE estado = 'Ocupado'")
        vendidos = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM asientos WHERE estado = 'Disponible'")
        disponibles = cursor.fetchone()[0]
        
        cursor.execute("SELECT COALESCE(SUM(precio), 0) FROM ventas")
        recaudado = cursor.fetchone()[0]
        
        return vendidos, disponibles, recaudado
    
    def cerrar(self):
        self.conexion.close()