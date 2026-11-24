import tkinter as tk
from tkinter import ttk, messagebox
from logica.sesiones import listar_sesiones, eliminar_sesion


class VentanaHistorialSesiones:
    def __init__(self, parent, usuario):
        self.ventana = tk.Toplevel(parent)
        self.usuario = usuario
        self.ventana.title("GymTrack - Historial de Sesiones")
        self.ventana.geometry("780x550")
        self.ventana.configure(bg="#1e1e2e")
        self.ventana.grab_set()

        self.sesiones_cache = {}

        self.crear_componentes()
        self.cargar_sesiones()

    def crear_componentes(self):
        tk.Label(
            self.ventana,
            text="HISTORIAL DE SESIONES DE ENTRENAMIENTO (MongoDB)",
            font=("Segoe UI", 15, "bold"),
            fg="#cba6f7",
            bg="#1e1e2e"
        ).pack(pady=(18, 4))

        tk.Label(
            self.ventana,
            text="Selecciona una sesión para ver el detalle de ejercicios o eliminarla:",
            font=("Segoe UI", 10),
            fg="#cdd6f4",
            bg="#1e1e2e"
        ).pack(pady=(0, 12))

        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Treeview", background="#313244", foreground="#ffffff", fieldbackground="#313244", rowheight=26, font=("Segoe UI", 10))
        estilo.configure("Treeview.Heading", background="#181825", foreground="#cba6f7", font=("Segoe UI", 10, "bold"))

        frame_tabla = tk.Frame(self.ventana, bg="#1e1e2e")
        frame_tabla.pack(padx=25, fill="x")

        cols = ("id", "fecha", "rutina", "observaciones")
        self.tabla = ttk.Treeview(frame_tabla, columns=cols, show="headings", height=7)
        self.tabla.heading("id", text="ID Mongo")
        self.tabla.heading("fecha", text="Fecha")
        self.tabla.heading("rutina", text="Rutina")
        self.tabla.heading("observaciones", text="Observaciones")

        self.tabla.column("id", width=165)
        self.tabla.column("fecha", width=100, anchor="center")
        self.tabla.column("rutina", width=170)
        self.tabla.column("observaciones", width=280)
        self.tabla.pack(fill="x")

        self.tabla.bind("<<TreeviewSelect>>", self.mostrar_detalle)

        tk.Label(
            self.ventana,
            text="Detalle de ejercicios de la sesión seleccionada:",
            font=("Segoe UI", 10, "bold"),
            fg="#a6e3a1",
            bg="#1e1e2e"
        ).pack(pady=(15, 5))

        self.texto_detalle = tk.Text(
            self.ventana,
            height=8,
            font=("Consolas", 10),
            bg="#313244",
            fg="#ffffff",
            relief="flat",
            padx=10,
            pady=8
        )
        self.texto_detalle.pack(padx=25, fill="both", expand=True)
        self.texto_detalle.config(state="disabled")

        frame_botones = tk.Frame(self.ventana, bg="#1e1e2e")
        frame_botones.pack(pady=15)

        tk.Button(
            frame_botones,
            text="Eliminar Sesión Seleccionada",
            font=("Segoe UI", 10, "bold"),
            bg="#fab387",
            fg="#11111b",
            cursor="hand2",
            relief="flat",
            command=self.borrar_seleccionada
        ).pack(side="left", padx=10, ipadx=15, ipady=5)

        tk.Button(
            frame_botones,
            text="Volver al Menú",
            font=("Segoe UI", 10, "bold"),
            bg="#f38ba8",
            fg="#11111b",
            cursor="hand2",
            relief="flat",
            command=self.ventana.destroy
        ).pack(side="left", padx=10, ipadx=15, ipady=5)

    def cargar_sesiones(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        self.sesiones_cache.clear()

        try:
            sesiones = listar_sesiones(self.usuario["id_usuario"])
            for s in sesiones:
                id_str = str(s["_id"])
                self.sesiones_cache[id_str] = s
                self.tabla.insert(
                    "",
                    "end",
                    values=(id_str, s.get("fecha", ""), s.get("rutina", ""), s.get("observaciones", ""))
                )
        except Exception as e:
            messagebox.showerror("Error MongoDB", f"No se pudieron cargar las sesiones:\n{e}")

    def mostrar_detalle(self, event):
        seleccion = self.tabla.selection()
        if not seleccion:
            return

        id_str = self.tabla.item(seleccion[0], "values")[0]
        sesion = self.sesiones_cache.get(id_str)
        if not sesion:
            return

        lineas = [f"Rutina: {sesion.get('rutina', '')} | Fecha: {sesion.get('fecha', '')}"]
        lineas.append("-" * 60)

        for ej in sesion.get("ejercicios", []):
            nombre = ej.get("nombre", "Ejercicio")
            series = ej.get("series", "")
            if isinstance(series, list):
                detalle_series = ", ".join([f"{st.get('peso', 0)}kg x {st.get('repeticiones', 0)} reps" for st in series])
                lineas.append(f"• {nombre}: {detalle_series}")
            else:
                peso = ej.get("peso", 0)
                reps = ej.get("repeticiones", 0)
                lineas.append(f"• {nombre}: {series} series x {reps} repeticiones (Peso: {peso} kg)")

        self.texto_detalle.config(state="normal")
        self.texto_detalle.delete("1.0", tk.END)
        self.texto_detalle.insert(tk.END, "\n".join(lineas))
        self.texto_detalle.config(state="disabled")

    def borrar_seleccionada(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona una sesión de la tabla para eliminarla.")
            return

        id_str = self.tabla.item(seleccion[0], "values")[0]
        confirmar = messagebox.askyesno("Confirmar eliminación", "¿Seguro que deseas eliminar esta sesión de MongoDB?")
        if not confirmar:
            return

        try:
            eliminar_sesion(id_str)
            self.texto_detalle.config(state="normal")
            self.texto_detalle.delete("1.0", tk.END)
            self.texto_detalle.config(state="disabled")
            self.cargar_sesiones()
            messagebox.showinfo("Eliminada", "Sesión eliminada correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la sesión:\n{e}")