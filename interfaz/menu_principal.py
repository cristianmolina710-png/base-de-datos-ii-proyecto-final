import tkinter as tk
from interfaz.ejercicios import VentanaEjercicios
from interfaz.rutinas import VentanaRutinas
from interfaz.registrar_sesion import VentanaRegistrarSesion
from interfaz.historial_sesiones import VentanaHistorialSesiones


class VentanaMenuPrincipal:
    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario
        self.root.title("GymTrack - Panel Principal")
        self.root.geometry("680x520")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        self.crear_componentes()

    def crear_componentes(self):
        header = tk.Frame(self.root, bg="#181825", height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="GYMTRACK",
            font=("Segoe UI", 18, "bold"),
            fg="#a6e3a1",
            bg="#181825"
        ).pack(side="left", padx=25)

        info_usuario = f"{self.usuario['nombre']} ({self.usuario['rol']})"
        tk.Label(
            header,
            text=info_usuario,
            font=("Segoe UI", 10, "bold"),
            fg="#cdd6f4",
            bg="#181825"
        ).pack(side="right", padx=25)

        tk.Label(
            self.root,
            text=f"¡Bienvenido, {self.usuario['nombre']}!",
            font=("Segoe UI", 16, "bold"),
            fg="#ffffff",
            bg="#1e1e2e"
        ).pack(pady=(25, 5))

        tk.Label(
            self.root,
            text="Selecciona el módulo con el que deseas trabajar hoy:",
            font=("Segoe UI", 10),
            fg="#bac2de",
            bg="#1e1e2e"
        ).pack(pady=(0, 20))

        contenedor_botones = tk.Frame(self.root, bg="#1e1e2e")
        contenedor_botones.pack(padx=60, fill="both", expand=True)

        botones = [
            ("Catálogo de Ejercicios (MySQL)", "#89b4fa", self.abrir_ejercicios),
            ("Rutinas Disponibles (MySQL)", "#f9e2af", self.abrir_rutinas),
            ("Registrar Entrenamiento (MongoDB)", "#a6e3a1", self.abrir_registrar_sesion),
            ("Historial de Sesiones (MongoDB)", "#cba6f7", self.abrir_historial_sesiones),
        ]

        for texto, color, comando in botones:
            tk.Button(
                contenedor_botones,
                text=texto,
                font=("Segoe UI", 11, "bold"),
                bg=color,
                fg="#11111b",
                cursor="hand2",
                relief="flat",
                command=comando
            ).pack(fill="x", pady=8, ipady=10)

        tk.Button(
            self.root,
            text="Cerrar Sesión",
            font=("Segoe UI", 10, "bold"),
            bg="#f38ba8",
            fg="#11111b",
            cursor="hand2",
            relief="flat",
            command=self.cerrar_sesion
        ).pack(pady=(10, 25), ipadx=20, ipady=5)

    def abrir_ejercicios(self):
        VentanaEjercicios(self.root)

    def abrir_rutinas(self):
        VentanaRutinas(self.root)

    def abrir_registrar_sesion(self):
        VentanaRegistrarSesion(self.root, self.usuario)

    def abrir_historial_sesiones(self):
        VentanaHistorialSesiones(self.root, self.usuario)

    def cerrar_sesion(self):
        from interfaz.login import VentanaLogin
        self.root.destroy()
        nuevo_root = tk.Tk()
        VentanaLogin(nuevo_root)
        nuevo_root.mainloop()


def abrir_menu_principal(usuario):
    root = tk.Tk()
    VentanaMenuPrincipal(root, usuario)
    root.mainloop()