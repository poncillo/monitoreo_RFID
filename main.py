import tkinter as tk
from views.login import LoginViewCH
from views.view_admin import AdminView
from views.view_general import GeneralView
from views.view_chofer import ChoferView
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
            from views.view_admin import AdminView
            AdminView(self, self)
        elif self.usuario_actual.rol == 'chofer':
            from views.view_chofer import ChoferView
            ChoferView(self, self)
        else:  # general
            from views.view_general import GeneralView
            GeneralView(self, self)
            
    def cerrar_sesion(self):
        """Cierra la sesión y vuelve al login"""
        self.usuario_actual = None
        self.mostrar_login()

if __name__ == "__main__":
    app = Application()
    app.mainloop()