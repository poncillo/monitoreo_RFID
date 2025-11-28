import tkinter as tk
from tkinter import ttk, messagebox  # <--- AGREGA ESTA LÍNEA
from views.login import LoginViewCH
import os
import sys

def resource_path(relative_path):
    """Obtiene la ruta absoluta para recursos (imágenes, etc.)"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Transporte - Login")
        self.geometry("800x600")
        self.resizable(True, True)
        
        # Usuario actual
        self.usuario_actual = None
        
        # Mostrar vista de login
        self.mostrar_login()
        
    def mostrar_login(self):
        """Muestra la vista de login"""
        # Limpiar ventana si hay algo más
        for widget in self.winfo_children():
            widget.destroy()
            
        # Crear y mostrar login
        self.login_view = LoginViewCH(self, self)
        self.login_view.pack(fill=tk.BOTH, expand=True)
        
    def on_login_exitoso(self, usuario):
        """Callback cuando el login es exitoso"""
        self.usuario_actual = usuario
        self.mostrar_panel_principal()
        
    def mostrar_panel_principal(self):
        """Muestra el panel principal según el rol del usuario"""
        # Limpiar ventana
        for widget in self.winfo_children():
            widget.destroy()
            
        # Crear panel principal según rol
        if self.usuario_actual.rol == 'admin':
            self.mostrar_panel_admin()
        elif self.usuario_actual.rol == 'chofer':
            self.mostrar_panel_chofer()
        else:  # general
            self.mostrar_panel_general()
            
    def mostrar_panel_admin(self):
        """Panel para administradores"""
        tk.Label(self, text=f"Panel Admin - Bienvenido {self.usuario_actual.username}", 
                font=("Arial", 16, "bold")).pack(pady=20)
        
        # Aquí irían las funcionalidades específicas de admin
        ttk.Button(self, text="Gestionar Usuarios", command=self.gestionar_usuarios).pack(pady=5)
        ttk.Button(self, text="Gestionar Vehículos", command=self.gestionar_vehiculos).pack(pady=5)
        ttk.Button(self, text="Ver Reportes", command=self.ver_reportes).pack(pady=5)
        ttk.Button(self, text="Cerrar Sesión", command=self.cerrar_sesion).pack(pady=20)
        
    def mostrar_panel_chofer(self):
        """Panel para choferes"""
        tk.Label(self, text=f"Panel Chofer - Bienvenido {self.usuario_actual.username}", 
                font=("Arial", 16, "bold")).pack(pady=20)
        
        # Funcionalidades para choferes
        ttk.Button(self, text="Mis Rutas", command=self.mis_rutas).pack(pady=5)
        ttk.Button(self, text="Reportar Ubicación", command=self.reportar_ubicacion).pack(pady=5)
        ttk.Button(self, text="Cerrar Sesión", command=self.cerrar_sesion).pack(pady=20)
        
    def mostrar_panel_general(self):
        """Panel para usuarios generales"""
        tk.Label(self, text=f"Panel General - Bienvenido {self.usuario_actual.username}", 
                font=("Arial", 16, "bold")).pack(pady=20)
        
        # Funcionalidades de solo lectura
        ttk.Button(self, text="Ver Rutas", command=self.ver_rutas).pack(pady=5)
        ttk.Button(self, text="Ver Vehículos", command=self.ver_vehiculos).pack(pady=5)
        ttk.Button(self, text="Cerrar Sesión", command=self.cerrar_sesion).pack(pady=20)
        
    def cerrar_sesion(self):
        """Cierra la sesión y vuelve al login"""
        self.usuario_actual = None
        self.mostrar_login()
        
    # Métodos placeholder para las funcionalidades
    def gestionar_usuarios(self):
        messagebox.showinfo("Info", "Gestión de usuarios - Por implementar")
        
    def gestionar_vehiculos(self):
        messagebox.showinfo("Info", "Gestión de vehículos - Por implementar")
        
    def ver_reportes(self):
        messagebox.showinfo("Info", "Reportes - Por implementar")
        
    def mis_rutas(self):
        messagebox.showinfo("Info", "Mis rutas - Por implementar")
        
    def reportar_ubicacion(self):
        messagebox.showinfo("Info", "Reportar ubicación - Por implementar")
        
    def ver_rutas(self):
        messagebox.showinfo("Info", "Ver rutas - Por implementar")
        
    def ver_vehiculos(self):
        messagebox.showinfo("Info", "Ver vehículos - Por implementar")

if __name__ == "__main__":
    app = Application()
    app.mainloop()