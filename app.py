import customtkinter as ctk
from tkinter import messagebox

from dataBase import BaseDatos
from avion import Avion


class App(ctk.CTk):
    COLOR_DISPONIBLE = "#2E8B57"
    COLOR_OCUPADO = "#B22222"
    COLOR_SELECCIONADO = "#1E90FF"

    def __init__(self):
        super().__init__()

        self.title("Venta de Boletos de Avion")
        self.geometry("1180x850")
        self.minsize(1000, 750)

        ctk.set_appearance_mode("dark")

        self.baseDatos = BaseDatos()
        self.avion = Avion(self.baseDatos)

        self.botones = {}
        self.crearInterfaz()
        self.actualizarInterfaz()

        self.protocol("WM_DELETE_WINDOW", self.cerrar)

    def crearInterfaz(self):
        encabezado = ctk.CTkFrame(self)
        encabezado.pack(fill="x", padx=20, pady=(20, 10))

        titulo = ctk.CTkLabel(
            encabezado,
            text="SISTEMA DE VENTA DE BOLETOS",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        titulo.pack(pady=(15, 5))

        subtitulo = ctk.CTkLabel(
            encabezado,
            text="Selecciona uno o varios asientos disponibles",
        )
        subtitulo.pack(pady=(0, 15))

        clases = ctk.CTkFrame(self)
        clases.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(
            clases,
            text="PRIMERA: $1100 | MEDIA: $1050 | COMERCIAL: $1000 | "
                 "VENTANILLA: +15%",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=10)

        mapa = ctk.CTkFrame(self)
        mapa.pack(fill="both", expand=True, padx=20, pady=10)

        ctk.CTkLabel(
            mapa,
            text="MAPA DEL AVIÓN",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(10, 5))

        self.contenedorAsientos = ctk.CTkFrame(mapa)
        self.contenedorAsientos.pack(expand=True, pady=10)

        self.crearMapaAsientos()

        inferior = ctk.CTkFrame(self)
        inferior.pack(fill="x", padx=20, pady=(0, 20))

        self.info_asiento = ctk.CTkLabel(
            inferior,
            text="Selecciona un asiento para ver su información.",
            justify="left",
            anchor="w"
        )
        self.info_asiento.pack(side="left", padx=15, pady=12)

        panelDerecho = ctk.CTkFrame(
            inferior,
            fg_color="transparent"
        )
        panelDerecho.pack(side="right", padx=15, pady=10)

        self.resumen = ctk.CTkLabel(
            panelDerecho,
            text="",
            justify="left"
        )
        self.resumen.pack(pady=(0, 8))

        self.confirmarBtn = ctk.CTkButton(
            panelDerecho,
            text="Confirmar selección",
            command=self.confirmarCompra,
            height=40,
            font=ctk.CTkFont(size=15, weight="bold")
        )
        self.confirmarBtn.pack()

        leyenda = ctk.CTkFrame(self)
        leyenda.pack(fill="x", padx=20, pady=(0, 20))

        ctk.CTkLabel(
            leyenda,
            text="🟢 Disponible    🔴 Ocupado    🔵 Seleccionado    "
                 "│    1 2 3   PASILLO   4 5 6"
        ).pack(pady=8)

    def crearMapaAsientos(self):
        filas = "ABCDEFGHIJKLMNO"

        ctk.CTkLabel(
            self.contenedorAsientos,
            text="FILA",
            width=55
        ).grid(row=0, column=0, padx=5, pady=5)

        for columna in range(1, 7):
            grid_col = columna if columna <= 3 else columna + 1

            ctk.CTkLabel(
                self.contenedorAsientos,
                text=str(columna),
                width=65
            ).grid(
                row=0,
                column=grid_col,
                padx=4,
                pady=5
            )

        for indiceFila, letra in enumerate(filas, start=1):

            if letra == "D":
                indiceFila += 1

            elif letra == "L":
                indiceFila += 2

            ctk.CTkLabel(
                self.contenedorAsientos,
                text=letra,
                width=55
            ).grid(
                row=indiceFila,
                column=0,
                padx=5,
                pady=3
            )

            for columna in range(1, 7):

                grid_col = columna if columna <= 3 else columna + 1
                numero = f"{letra}{columna}"

                boton = ctk.CTkButton(
                    self.contenedorAsientos,
                    text=numero,
                    width=65,
                    height=35,
                    command=lambda n=numero: self.clickAsiento(n)
                )

                boton.grid(
                    row=indiceFila,
                    column=grid_col,
                    padx=(4, 14 if columna == 3 else 4),
                    pady=3
                )

                self.botones[numero] = boton

    def clickAsiento(self, numero):
        asiento = self.avion.buscarAsiento(numero)

        if asiento is None:
            return

        if asiento.estado == "Ocupado":
            self.mostrarInformacion(numero)

            messagebox.showinfo(
                "Asiento ocupado",
                f"El asiento {numero} ya está ocupado."
            )

            return

        self.avion.seleccionarAsiento(numero)

        self.mostrarInformacion(numero)
        self.actualizarInterfaz()

    def mostrarInformacion(self, numero):
        asiento = self.avion.buscarAsiento(numero)

        if asiento is None:
            return

        datos = asiento.informacion()

        if datos["estado"] == "Ocupado":

            texto = (
                f"Asiento: {datos['asiento']}\n"
                f"Clase: {datos['clase']}\n"
                f"Tipo: {datos['tipo']}\n"
                f"Precio: ${datos['precio']:,.2f}\n"
                f"Estado: {datos['estado']}"
            )

        else:

            texto = (
                f"Asiento: {datos['asiento']}\n"
                f"Clase: {datos['clase']}\n"
                f"Tipo: {datos['tipo']}\n"
                f"Precio base: ${datos['precioBase']:,.2f}\n"
                f"Recargo ventanilla: {datos['recargo']}%\n"
                f"Precio final: ${datos['precio']:,.2f}\n"
                f"Estado: {datos['estado']}"
            )

        self.info_asiento.configure(text=texto)

    def actualizarInterfaz(self):

        for numero, boton in self.botones.items():

            asiento = self.avion.buscarAsiento(numero)

            if asiento is None:
                continue

            if asiento.estado == "Disponible":

                boton.configure(
                    fg_color=self.COLOR_DISPONIBLE,
                    hover_color="#3AA76D",
                    state="normal"
                )

            elif asiento.estado == "Ocupado":

                boton.configure(
                    fg_color=self.COLOR_OCUPADO,
                    hover_color=self.COLOR_OCUPADO,
                    state="disabled"
                )

            elif asiento.estado == "Seleccionado":

                boton.configure(
                    fg_color=self.COLOR_SELECCIONADO,
                    hover_color="#4BA3FF",
                    state="normal"
                )

        vendidos, disponibles, recaudado = self.avion.obtenerResumen()

        seleccionados = self.avion.obtenerSeleccionados()

        totalSeleccion = sum(
            a.precio for a in seleccionados
        )

        texto = (
            f"Boletos vendidos: {vendidos}\n"
            f"Boletos faltantes: {disponibles}\n"
            f"Dinero recaudado: ${recaudado:,.2f}\n"
            f"Selección actual: {len(seleccionados)}\n"
            f"Total selección: ${totalSeleccion:,.2f}"
        )

        self.resumen.configure(text=texto)

        if self.avion.todosOcupados():

            self.confirmarBtn.configure(
                state="disabled",
                text="Avión completo"
            )

        else:

            self.confirmarBtn.configure(
                state="normal",
                text="Confirmar selección"
            )

    def confirmarCompra(self):

        seleccionados = self.avion.obtenerSeleccionados()

        if not seleccionados:

            messagebox.showwarning(
                "Sin selección",
                "Debes seleccionar al menos un asiento."
            )

            return

        detalles = "\n".join(
            f"{a.numero} - {a.clase} - {a.tipoAsiento} "
            f"- ${a.precio:,.2f}"
            for a in seleccionados
        )

        total = sum(
            a.precio for a in seleccionados
        )

        mensaje = (
            "ASIENTOS SELECCIONADOS:\n\n"
            f"{detalles}\n\n"
            f"TOTAL: ${total:,.2f}\n\n"
            "¿Deseas confirmar la compra?"
        )

        confirmar = messagebox.askyesno(
            "Confirmar compra",
            mensaje
        )

        if not confirmar:
            return

        try:

            venta = self.avion.confirmarVenta()

            messagebox.showinfo(
                "Compra realizada",
                f"Compra confirmada correctamente.\n\n"
                f"Boletos vendidos en esta compra: "
                f"{venta.cantidadBoletos()}\n"
                f"Total: ${venta.calcularTotal():,.2f}"
            )

            self.actualizarInterfaz()

        except ValueError as error:

            messagebox.showerror(
                "Error en la compra",
                str(error)
            )

            self.avion.cargarAsientos()
            self.actualizarInterfaz()

    def cerrar(self):
        self.baseDatos.cerrar()
        self.destroy()