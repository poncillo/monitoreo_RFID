import re
import tkinter as tk
from tkinter import ttk, messagebox
from models.usuario import Usuario  # Importamos nuestro modelo Usuario

class LoginViewCH(tk.Frame):
    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador
        self.configure(bg="white")
        self.style = ttk.Style()
        self.estilos_personalizados()
        self.interface_conf()
        
    def estilos_personalizados(self):
        """Configura estilos personalizados para los campos de entrada en caso de error."""
        self.style.configure("Error.TEntry", foreground="red", bordercolor="#dc3545", fieldbackground="#ffe6e6")
        self.style.map("Error.TEntry", bordercolor=[("focus", "#dc3545"), ("!focus", "#dc3545")], foreground=[("focus", "black")])
        
        # Estilo para el botón de Salir (opcional)
        self.style.configure("Danger.TButton", foreground="black", background="#dc3545", font=("Arial", 10))
        self.style.map("Danger.TButton", background=[("active", "#c82333")])

    def interface_conf(self):
        """Configura la interfaz gráfica."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Contenedor principal
        frame_contenedor = tk.Frame(self, bg="white")
        frame_contenedor.grid(row=0, column=0, sticky="nsew")
        frame_contenedor.grid_columnconfigure(0, weight=1)
        frame_contenedor.grid_rowconfigure(0, weight=1)

        # Marco interno con tamaño fijo
        frame = tk.Frame(frame_contenedor, bg="white", padx=20, pady=20)
        frame.grid(row=0, column=0, sticky="")
        frame.configure(width=550, height=700)

        # Cargar y mostrar el logotipo
        try:
            # Usar resource_path para obtener la ruta correcta del logo
            from main import resource_path
            logo_path = resource_path('images/demo_logo.png')
            
            self.logo_image = tk.PhotoImage(file=logo_path)
            self.logo_image = self.logo_image.subsample(2, 2)  # Reducir a la mitad
            
            # Mostrar el logo
            logo_label = tk.Label(frame, image=self.logo_image, bg="white")
            logo_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
            
        except Exception as e:
            print(f"Error al cargar el logo: {e}")

        # Título
        tk.Label(frame, text="Sistema de Monitoreo de Cilindros RFID", font=("Arial", 16, "bold"), bg="white").grid(row=1, column=0, columnspan=2, pady=10)

        # Campos de entrada - CAMBIO IMPORTANTE: Usamos username en lugar de email
        self.crear_campo_usuario(frame, 2)
        self.crear_campo_password(frame, 4)

        # Botón para Iniciar Sesión
        ttk.Button(frame, text="Iniciar Sesión", command=self.iniciar_sesion).grid(row=6, column=0, columnspan=2, pady=(15, 5), sticky="ew")
        # Botón de Creación de usuario
        ttk.Button(frame, text="Registrar Nuevo Usuario", command=self).grid(row=8, column=0, columnspan=2, pady=(0, 10), sticky="ew")
        # Botón para Salir
        ttk.Button(frame, text="Salir", command=self.exit, style="Danger.TButton").grid(row=8, column=0, columnspan=2, pady=(0, 10), sticky="ew")

    def exit(self):
        if messagebox.askyesno("Salir", "¿Está seguro que desea cerrar la aplicación?"):
            if self.controlador:
                self.controlador.destroy()
            else:
                self.master.destroy()

    def crear_campo_usuario(self, padre, fila):
        """Crea el campo de entrada para el usuario (NO email)."""
        tk.Label(padre, text="Usuario:", bg="white", font=("Arial", 10)).grid(row=fila, column=0, sticky="w", pady=5)
        self.usuario_entry = ttk.Entry(padre, width=30, font=("Arial", 10), style="TEntry")
        self.usuario_entry.grid(row=fila+1, column=0, columnspan=2, pady=5, sticky="ew")
        self.usuario_entry.bind("<KeyRelease>", self.validar_usuario_en_tiempo_real)
        self.usuario_entry.bind("<Return>", lambda e: self.iniciar_sesion())  # Enter para login

    def crear_campo_password(self, padre, fila):
        """Crea el campo de entrada para la contraseña."""
        tk.Label(padre, text="Contraseña:", bg="white", font=("Arial", 10)).grid(row=fila, column=0, sticky="w", pady=5)
        self.password_entry = ttk.Entry(padre, show="*", width=30, font=("Arial", 10), style="TEntry")
        self.password_entry.grid(row=fila+1, column=0, columnspan=2, pady=5, sticky="ew")
        self.password_entry.bind("<Return>", lambda e: self.iniciar_sesion())  # Enter para login

    def validar_usuario(self, usuario):
        """Valida que el usuario no esté vacío y tenga formato básico."""
        return len(usuario.strip()) >= 3  # Mínimo 3 caracteres

    def validar_usuario_en_tiempo_real(self, event):
        """Validación en tiempo real del campo usuario."""
        usuario = self.usuario_entry.get()
        if usuario:
            if self.validar_usuario(usuario):
                self.usuario_entry.config(style="TEntry")
            else:
                self.usuario_entry.config(style="Error.TEntry")
        else:
            self.usuario_entry.config(style="TEntry")

    def mostrar_error(self, mensaje, widget=None):
        """Muestra mensaje de error y resalta campo si se especifica."""
        if widget:
            widget.config(style="Error.TEntry")
        messagebox.showerror("Error de Autenticación", mensaje)

    def iniciar_sesion(self):
        """Verifica los datos de login contra nuestra base de datos MySQL."""
        username = self.usuario_entry.get().strip()
        password = self.password_entry.get()
        
        # Validaciones básicas
        if not username:
            self.mostrar_error("El usuario es obligatorio", self.usuario_entry)
            self.usuario_entry.focus()
            return
            
        if not password:
            self.mostrar_error("La contraseña es obligatoria", self.password_entry)
            self.password_entry.focus()
            return
            
        if not self.validar_usuario(username):
            self.mostrar_error("Usuario debe tener al menos 3 caracteres", self.usuario_entry)
            self.usuario_entry.focus()
            return

        try:
            # AUTENTICACIÓN CON NUESTRO SISTEMA - CAMBIO PRINCIPAL
            usuario = Usuario.autenticar(username, password)
            
            if usuario:
                # Login exitoso - limpiar campos
                self.usuario_entry.delete(0, tk.END)
                self.password_entry.delete(0, tk.END)
                
                # Notificar al controlador del login exitoso
                if self.controlador:
                    self.controlador.on_login_exitoso(usuario)
                else:
                    messagebox.showinfo("Éxito", f"Bienvenido {usuario.username} ({usuario.rol})")
                    
            else:
                self.mostrar_error("Usuario o contraseña incorrectos")
                self.password_entry.delete(0, tk.END)
                self.usuario_entry.focus()
                
        except Exception as e:
            self.mostrar_error(f"Error de conexión: {str(e)}")
            print(f"Error en login: {e}")

    def limpiar_campos(self):
        """Limpia todos los campos del formulario."""
        self.usuario_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.usuario_entry.config(style="TEntry")