import tkinter as tk
from tkinter import messagebox
from logica.usuarios import iniciar_sesion
from interfaz.menu_principal import abrir_menu_principal


class VentanaLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("GymTrack - Iniciar Sesión")
        self.root.geometry("400x340")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")

        self.crear_componentes()

    def crear_componentes(self):
        tk.Label(
            self.root,
            text="GYMTRACK",
            font=("Segoe UI", 22, "bold"),
            fg="#a6e3a1",
            bg="#1e1e2e"
        ).pack(pady=(25, 5))

        tk.Label(
            self.root,
            text="Control de Rutinas y Entrenamientos",
            font=("Segoe UI", 10),
            fg="#cdd6f4",
            bg="#1e1e2e"
        ).pack(pady=(0, 20))

        frame_form = tk.Frame(self.root, bg="#1e1e2e")
        frame_form.pack(padx=40, fill="x")

        tk.Label(
            frame_form,
            text="Correo electrónico:",
            font=("Segoe UI", 10),
            fg="#cdd6f4",
            bg="#1e1e2e",
            anchor="w"
        ).pack(fill="x")

        self.entry_correo = tk.Entry(frame_form, font=("Segoe UI", 11))
        self.entry_correo.pack(fill="x", pady=(4, 12), ipady=4)
        self.entry_correo.insert(0, "usuario1@gymtrack.com")

        tk.Label(
            frame_form,
            text="Contraseña:",
            font=("Segoe UI", 10),
            fg="#cdd6f4",
            bg="#1e1e2e",
            anchor="w"
        ).pack(fill="x")

        self.entry_password = tk.Entry(frame_form, font=("Segoe UI", 11), show="*")
        self.entry_password.pack(fill="x", pady=(4, 20), ipady=4)
        self.entry_password.insert(0, "hash_usuario1")

        self.btn_ingresar = tk.Button(
            frame_form,
            text="Iniciar Sesión",
            font=("Segoe UI", 11, "bold"),
            bg="#a6e3a1",
            fg="#11111b",
            cursor="hand2",
            relief="flat",
            command=self.validar_login
        )
        self.btn_ingresar.pack(fill="x", ipady=6)

        self.root.bind("<Return>", lambda event: self.validar_login())

    def validar_login(self):
        correo = self.entry_correo.get().strip()
        password = self.entry_password.get().strip()

        if not correo or not password:
            messagebox.showwarning("Campos vacíos", "Por favor ingresa tu correo y contraseña.")
            return

        try:
            usuario = iniciar_sesion(correo, password)
            if usuario:
                self.root.destroy()
                abrir_menu_principal(usuario)
            else:
                messagebox.showerror("Acceso denegado", "Correo o contraseña incorrectos.")
        except Exception as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a MySQL:\n{e}")