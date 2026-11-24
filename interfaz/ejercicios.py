import tkinter as tk
from tkinter import ttk, messagebox
from logica.ejercicios import listar_ejercicios_completos


class VentanaEjercicios:
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("GymTrack - Catálogo de Ejercicios")
        self.ventana.geometry("760x440")
        self.ventana.configure(bg="#1e1e2e")
        self.ventana.grab_set()

        self.crear_componentes()
        self.cargar_datos()

    def crear_componentes(self):
        tk.Label(
            self.ventana,
            text="CATÁLOGO DE EJERCICIOS (MySQL)",
            font=("Segoe UI", 16, "bold"),
            fg="#89b4fa",
            bg="#1e1e2e"
        ).pack(pady=(20, 5))

        tk.Label(
            self.ventana,
            text="Consulta los ejercicios registrados con su tipo, equipo y grupos musculares.",
            font=("Segoe UI", 10),
            fg="#cdd6f4",
            bg="#1e1e2e"
        ).pack(pady=(0, 15))

        frame_tabla = tk.Frame(self.ventana, bg="#1e1e2e")
        frame_tabla.pack(padx=25, fill="both", expand=True)

        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Treeview", background="#313244", foreground="#ffffff", fieldbackground="#313244", rowheight=28, font=("Segoe UI", 10))
        estilo.configure("Treeview.Heading", background="#181825", foreground="#89b4fa", font=("Segoe UI", 10, "bold"))

        columnas = ("id", "ejercicio", "tipo", "equipo", "grupos")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

        self.tabla.heading("id", text="ID")
        self.tabla.heading("ejercicio", text="Ejercicio")
        self.tabla.heading("tipo", text="Tipo")
        self.tabla.heading("equipo", text="Equipo")
        self.tabla.heading("grupos", text="Grupos Musculares")

        self.tabla.column("id", width=45, anchor="center")
        self.tabla.column("ejercicio", width=160)
        self.tabla.column("tipo", width=120, anchor="center")
        self.tabla.column("equipo", width=150, anchor="center")
        self.tabla.column("grupos", width=220)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Button(
            self.ventana,
            text="Volver al Menú",
            font=("Segoe UI", 10, "bold"),
            bg="#f38ba8",
            fg="#11111b",
            cursor="hand2",
            relief="flat",
            command=self.ventana.destroy
        ).pack(pady=18, ipadx=20, ipady=5)

    def cargar_datos(self):
        try:
            for item in self.tabla.get_children():
                self.tabla.delete(item)

            ejercicios = listar_ejercicios_completos()
            for ej in ejercicios:
                self.tabla.insert(
                    "",
                    "end",
                    values=(ej["id_ejercicio"], ej["ejercicio"], ej["tipo"], ej["equipo"], ej["grupos_musculares"])
                )
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los ejercicios:\n{e}")