import tkinter as tk
from tkinter import ttk, messagebox
from logica.rutinas import listar_rutinas
from logica.ejercicios import listar_ejercicios
from logica.sesiones import guardar_sesion


class VentanaRegistrarSesion:
    def __init__(self, parent, usuario):
        self.ventana = tk.Toplevel(parent)
        self.usuario = usuario
        self.ventana.title("GymTrack - Registrar Entrenamiento")
        self.ventana.geometry("760x580")
        self.ventana.configure(bg="#1e1e2e")
        self.ventana.grab_set()

        self.ejercicios_agregados = []
        self.mapa_ejercicios = {}

        self.crear_componentes()
        self.cargar_catalogos()

    def crear_componentes(self):
        tk.Label(
            self.ventana,
            text="REGISTRAR SESIÓN DE ENTRENAMIENTO (MongoDB)",
            font=("Segoe UI", 15, "bold"),
            fg="#a6e3a1",
            bg="#1e1e2e"
        ).pack(pady=(15, 5))

        frame_rutina = tk.Frame(self.ventana, bg="#1e1e2e")
        frame_rutina.pack(padx=25, pady=8, fill="x")

        tk.Label(
            frame_rutina,
            text="Rutina realizada:",
            font=("Segoe UI", 10, "bold"),
            fg="#cdd6f4",
            bg="#1e1e2e"
        ).pack(side="left")

        self.combo_rutina = ttk.Combobox(frame_rutina, font=("Segoe UI", 10), width=35)
        self.combo_rutina.pack(side="left", padx=10)

        frame_agregar = tk.LabelFrame(
            self.ventana,
            text=" Agregar ejercicio realizado ",
            font=("Segoe UI", 10, "bold"),
            fg="#89b4fa",
            bg="#1e1e2e",
            padx=12,
            pady=10
        )
        frame_agregar.pack(padx=25, pady=8, fill="x")

        tk.Label(frame_agregar, text="Ejercicio:", fg="#cdd6f4", bg="#1e1e2e").grid(row=0, column=0, sticky="w")
        self.combo_ejercicio = ttk.Combobox(frame_agregar, state="readonly", width=24)
        self.combo_ejercicio.grid(row=1, column=0, padx=(0, 10), pady=4)

        tk.Label(frame_agregar, text="Peso (kg):", fg="#cdd6f4", bg="#1e1e2e").grid(row=0, column=1, sticky="w")
        self.entry_peso = tk.Entry(frame_agregar, width=10)
        self.entry_peso.insert(0, "0")
        self.entry_peso.grid(row=1, column=1, padx=(0, 10), pady=4)

        tk.Label(frame_agregar, text="Series:", fg="#cdd6f4", bg="#1e1e2e").grid(row=0, column=2, sticky="w")
        self.entry_series = tk.Entry(frame_agregar, width=10)
        self.entry_series.insert(0, "4")
        self.entry_series.grid(row=1, column=2, padx=(0, 10), pady=4)

        tk.Label(frame_agregar, text="Repeticiones:", fg="#cdd6f4", bg="#1e1e2e").grid(row=0, column=3, sticky="w")
        self.entry_reps = tk.Entry(frame_agregar, width=12)
        self.entry_reps.insert(0, "12")
        self.entry_reps.grid(row=1, column=3, padx=(0, 12), pady=4)

        tk.Button(
            frame_agregar,
            text="+ Añadir",
            font=("Segoe UI", 9, "bold"),
            bg="#89b4fa",
            fg="#11111b",
            cursor="hand2",
            relief="flat",
            command=self.agregar_ejercicio_lista
        ).grid(row=1, column=4, ipadx=10, ipady=2)

        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Treeview", background="#313244", foreground="#ffffff", fieldbackground="#313244", rowheight=25, font=("Segoe UI", 10))
        estilo.configure("Treeview.Heading", background="#181825", foreground="#a6e3a1", font=("Segoe UI", 10, "bold"))

        frame_tabla = tk.Frame(self.ventana, bg="#1e1e2e")
        frame_tabla.pack(padx=25, pady=8, fill="both", expand=True)

        cols = ("ejercicio", "peso", "series", "repeticiones")
        self.tabla = ttk.Treeview(frame_tabla, columns=cols, show="headings", height=6)
        self.tabla.heading("ejercicio", text="Ejercicio")
        self.tabla.heading("peso", text="Peso (kg)")
        self.tabla.heading("series", text="Series")
        self.tabla.heading("repeticiones", text="Repeticiones")

        self.tabla.column("ejercicio", width=280)
        self.tabla.column("peso", width=120, anchor="center")
        self.tabla.column("series", width=120, anchor="center")
        self.tabla.column("repeticiones", width=120, anchor="center")
        self.tabla.pack(fill="both", expand=True)

        frame_obs = tk.Frame(self.ventana, bg="#1e1e2e")
        frame_obs.pack(padx=25, pady=8, fill="x")

        tk.Label(
            frame_obs,
            text="Observaciones del entrenamiento:",
            font=("Segoe UI", 10, "bold"),
            fg="#cdd6f4",
            bg="#1e1e2e"
        ).pack(anchor="w")

        self.entry_obs = tk.Entry(frame_obs, font=("Segoe UI", 10))
        self.entry_obs.pack(fill="x", pady=(4, 0), ipady=4)

        frame_botones = tk.Frame(self.ventana, bg="#1e1e2e")
        frame_botones.pack(pady=15)

        tk.Button(
            frame_botones,
            text="Guardar Sesión en MongoDB",
            font=("Segoe UI", 10, "bold"),
            bg="#a6e3a1",
            fg="#11111b",
            cursor="hand2",
            relief="flat",
            command=self.guardar_en_mongo
        ).pack(side="left", padx=10, ipadx=15, ipady=6)

        tk.Button(
            frame_botones,
            text="Cancelar / Volver",
            font=("Segoe UI", 10, "bold"),
            bg="#f38ba8",
            fg="#11111b",
            cursor="hand2",
            relief="flat",
            command=self.ventana.destroy
        ).pack(side="left", padx=10, ipadx=15, ipady=6)

    def cargar_catalogos(self):
        try:
            rutinas = listar_rutinas()
            nombres_rutinas = [r["nombre"] for r in rutinas]
            self.combo_rutina["values"] = nombres_rutinas
            if nombres_rutinas:
                self.combo_rutina.current(0)

            ejercicios = listar_ejercicios()
            self.mapa_ejercicios = {nombre: id_ej for id_ej, nombre in ejercicios}
            nombres_ejercicios = list(self.mapa_ejercicios.keys())
            self.combo_ejercicio["values"] = nombres_ejercicios
            if nombres_ejercicios:
                self.combo_ejercicio.current(0)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los catálogos desde MySQL:\n{e}")

    def agregar_ejercicio_lista(self):
        nombre_ej = self.combo_ejercicio.get()
        if not nombre_ej:
            messagebox.showwarning("Atención", "Selecciona un ejercicio.")
            return

        try:
            peso = float(self.entry_peso.get().strip())
            series = int(self.entry_series.get().strip())
            repeticiones = int(self.entry_reps.get().strip())
            if series <= 0 or repeticiones <= 0 or peso < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Datos inválidos", "Verifica que peso, series y repeticiones sean números válidos.")
            return

        id_ej = self.mapa_ejercicios[nombre_ej]
        item_ejercicio = {
            "id_ejercicio": id_ej,
            "nombre": nombre_ej,
            "peso": peso,
            "series": series,
            "repeticiones": repeticiones
        }
        self.ejercicios_agregados.append(item_ejercicio)

        self.tabla.insert("", "end", values=(nombre_ej, f"{peso} kg", series, repeticiones))

    def guardar_en_mongo(self):
        rutina = self.combo_rutina.get().strip()
        observaciones = self.entry_obs.get().strip()

        if not rutina:
            messagebox.showwarning("Campo requerido", "Indica o selecciona el nombre de la rutina.")
            return

        if not self.ejercicios_agregados:
            messagebox.showwarning("Sin ejercicios", "Agrega al menos un ejercicio realizado antes de guardar.")
            return

        try:
            guardar_sesion(
                id_usuario=self.usuario["id_usuario"],
                rutina=rutina,
                ejercicios=self.ejercicios_agregados,
                observaciones=observaciones if observaciones else "Sin observaciones"
            )
            messagebox.showinfo("¡Éxito!", "Sesión de entrenamiento guardada correctamente en MongoDB.")
            self.ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error MongoDB", f"No se pudo guardar la sesión:\n{e}")