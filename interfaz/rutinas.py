import tkinter as tk
from tkinter import ttk, messagebox
from logica.rutinas import listar_rutinas, obtener_ejercicios_de_rutina


class VentanaRutinas:
    def __init__(self, parent):
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("GymTrack - Rutinas Disponibles")
        self.ventana.geometry("760x540")
        self.ventana.configure(bg="#1e1e2e")
        self.ventana.grab_set()

        self.crear_componentes()
        self.cargar_rutinas()

    def crear_componentes(self):
        tk.Label(
            self.ventana,
            text="RUTINAS DISPONIBLES (MySQL)",
            font=("Segoe UI", 16, "bold"),
            fg="#f9e2af",
            bg="#1e1e2e"
        ).pack(pady=(18, 4))

        tk.Label(
            self.ventana,
            text="Haz clic sobre una rutina para ver sus ejercicios asignados:",
            font=("Segoe UI", 10),
            fg="#cdd6f4",
            bg="#1e1e2e"
        ).pack(pady=(0, 10))

        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Treeview", background="#313244", foreground="#ffffff", fieldbackground="#313244", rowheight=26, font=("Segoe UI", 10))
        estilo.configure("Treeview.Heading", background="#181825", foreground="#f9e2af", font=("Segoe UI", 10, "bold"))

        frame_rutinas = tk.Frame(self.ventana, bg="#1e1e2e")
        frame_rutinas.pack(padx=25, fill="x")

        cols_rutinas = ("id", "nombre", "descripcion", "origen")
        self.tabla_rutinas = ttk.Treeview(frame_rutinas, columns=cols_rutinas, show="headings", height=5)
        self.tabla_rutinas.heading("id", text="ID")
        self.tabla_rutinas.heading("nombre", text="Nombre de Rutina")
        self.tabla_rutinas.heading("descripcion", text="Descripción")
        self.tabla_rutinas.heading("origen", text="Tipo")

        self.tabla_rutinas.column("id", width=45, anchor="center")
        self.tabla_rutinas.column("nombre", width=180)
        self.tabla_rutinas.column("descripcion", width=340)
        self.tabla_rutinas.column("origen", width=120, anchor="center")
        self.tabla_rutinas.pack(fill="x")

        self.tabla_rutinas.bind("<<TreeviewSelect>>", self.al_seleccionar_rutina)

        tk.Label(
            self.ventana,
            text="Ejercicios de la rutina seleccionada:",
            font=("Segoe UI", 11, "bold"),
            fg="#a6e3a1",
            bg="#1e1e2e"
        ).pack(pady=(18, 8))

        frame_detalle = tk.Frame(self.ventana, bg="#1e1e2e")
        frame_detalle.pack(padx=25, fill="both", expand=True)

        cols_detalle = ("ejercicio", "series", "repeticiones")
        self.tabla_detalle = ttk.Treeview(frame_detalle, columns=cols_detalle, show="headings", height=6)
        self.tabla_detalle.heading("ejercicio", text="Ejercicio")
        self.tabla_detalle.heading("series", text="Series")
        self.tabla_detalle.heading("repeticiones", text="Repeticiones")

        self.tabla_detalle.column("ejercicio", width=350)
        self.tabla_detalle.column("series", width=150, anchor="center")
        self.tabla_detalle.column("repeticiones", width=150, anchor="center")
        self.tabla_detalle.pack(fill="both", expand=True)

        tk.Button(
            self.ventana,
            text="Volver al Menú",
            font=("Segoe UI", 10, "bold"),
            bg="#f38ba8",
            fg="#11111b",
            cursor="hand2",
            relief="flat",
            command=self.ventana.destroy
        ).pack(pady=15, ipadx=20, ipady=5)

    def cargar_rutinas(self):
        try:
            for item in self.tabla_rutinas.get_children():
                self.tabla_rutinas.delete(item)

            rutinas = listar_rutinas()
            for r in rutinas:
                self.tabla_rutinas.insert(
                    "",
                    "end",
                    values=(r["id_rutina"], r["nombre"], r["descripcion"], r["origen"])
                )
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las rutinas:\n{e}")

    def al_seleccionar_rutina(self, event):
        seleccion = self.tabla_rutinas.selection()
        if not seleccion:
            return

        valores = self.tabla_rutinas.item(seleccion[0], "values")
        id_rutina = valores[0]

        for item in self.tabla_detalle.get_children():
            self.tabla_detalle.delete(item)

        try:
            ejercicios = obtener_ejercicios_de_rutina(id_rutina)
            for ej in ejercicios:
                self.tabla_detalle.insert(
                    "",
                    "end",
                    values=(ej["ejercicio"], ej["series"], ej["repeticiones"])
                )
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los ejercicios de la rutina:\n{e}")