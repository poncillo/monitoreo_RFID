# views/view_general.py
import tkinter as tk
from tkinter import ttk, messagebox

class GeneralView(tk.Frame):
    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador
        self.configure(bg="white")
        self.pack(fill=tk.BOTH, expand=True)
        self.crear_interfaz()

    def crear_interfaz(self):
        """Crea la interfaz principal del panel general"""
        main_frame = tk.Frame(self, bg="white", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text="Panel Usuario General", 
                font=("Arial", 18, "bold"), bg="white").pack(pady=(0, 20))

        # Funcionalidades de solo lectura
        ttk.Button(main_frame, text="Ver Rutas", 
                  command=self.ver_rutas, width=20).pack(pady=5)
        
        ttk.Button(main_frame, text="Ver Vehículos", 
                  command=self.ver_vehiculos, width=20).pack(pady=5)

        ttk.Button(main_frame, text="Cerrar Sesión", 
                  command=self.cerrar_sesion).pack(pady=20)

    def ver_rutas(self):
        messagebox.showinfo("Info", "Ver rutas - Por implementar")

    def ver_vehiculos(self):
        messagebox.showinfo("Info", "Ver vehículos - Por implementar")

    def cerrar_sesion(self):
        if self.controlador:
            self.controlador.cerrar_sesion()