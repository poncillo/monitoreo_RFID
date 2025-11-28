# views/view_chofer.py
import tkinter as tk
from tkinter import ttk, messagebox

class ChoferView(tk.Frame):
    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador
        self.configure(bg="white")
        self.pack(fill=tk.BOTH, expand=True)
        self.crear_interfaz()

    def crear_interfaz(self):
        """Crea la interfaz principal del panel chofer"""
        main_frame = tk.Frame(self, bg="white", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text="Panel Chofer", 
                font=("Arial", 18, "bold"), bg="white").pack(pady=(0, 20))

        # Funcionalidades para choferes
        ttk.Button(main_frame, text="Mis Rutas", 
                  command=self.mis_rutas, width=20).pack(pady=5)
        
        ttk.Button(main_frame, text="Reportar Ubicación", 
                  command=self.reportar_ubicacion, width=20).pack(pady=5)

        ttk.Button(main_frame, text="Cerrar Sesión", 
                  command=self.cerrar_sesion).pack(pady=20)

    def mis_rutas(self):
        messagebox.showinfo("Info", "Mis rutas - Por implementar")

    def reportar_ubicacion(self):
        messagebox.showinfo("Info", "Reportar ubicación - Por implementar")

    def cerrar_sesion(self):
        if self.controlador:
            self.controlador.cerrar_sesion()