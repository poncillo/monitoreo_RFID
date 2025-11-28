import re
import tkinter as tk
from tkinter import ttk, messagebox

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
        self.style.configure("Danger.TButton", foreground="white", background="#dc3545", font=("Arial", 10))
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
        frame.configure(width=350, height=380)  # Aumentamos la altura para acomodar el logo

        # Cargar y mostrar el logotipo
        try:
            # Usar resource_path para obtener la ruta correcta del logo
            from main import resource_path
            logo_path = resource_path('images/demo_logo.png')
            
            # MÉTODO 1: Usando tk.PhotoImage con subsample (más simple)
            self.logo_image = tk.PhotoImage(file=logo_path)
            self.logo_image = self.logo_image.subsample(2, 2)  # Reducir a la mitad
            
            # Mostrar el logo
            logo_label = tk.Label(frame, image=self.logo_image, bg="white")
            logo_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
            
        except Exception as e:
            print(f"Error al cargar el logo: {e}")

        # Título (ahora en la fila 1)
        tk.Label(frame, text="Inicio de Sesión", font=("Arial", 16, "bold"), bg="white").grid(row=1, column=0, columnspan=2, pady=10)

        # Campos de entrada (actualizar números de fila)
        self.crear_campo_email(frame, 2)  # Cambiado de 1 a 2
        self.crear_campo_password(frame, 4)  # Cambiado de 3 a 4

        # Botón para Iniciar Sesión (actualizar fila)
        ttk.Button(frame, text="Iniciar Sesión", command=self.iniciar_sesion).grid(row=6, column=0, columnspan=2, pady=(15, 5), sticky="ew")

        # Botón para Salir (actualizar fila)
        ttk.Button(frame,text="Salir",command=self.exit,).grid(row=7, column=0, columnspan=2, pady=(0, 10), sticky="ew")

    def exit(self):
        if messagebox.askyesno("Salir", "¿Está seguro que desea cerrar la aplicación?"):
            if self.controlador:
                self.controlador.destroy()
            else:
                self.master.destroy()

    def crear_campo_email(self, padre, fila):
        """Crea el campo de entrada para el email."""
        # CORREGIDO: Usar el parámetro 'fila' en lugar de números fijos
        tk.Label(padre, text="Email:", bg="white", font=("Arial", 10)).grid(row=fila, column=0, sticky="w", pady=5)
        self.email_entry = ttk.Entry(padre, width=30, font=("Arial", 10), style="TEntry")
        self.email_entry.grid(row=fila+1, column=0, columnspan=2, pady=5, sticky="ew")
        self.email_entry.bind("<KeyRelease>", self.validar_email_en_tiempo_real)

    def crear_campo_password(self, padre, fila):
        """Crea el campo de entrada para la contraseña."""
        # CORREGIDO: Usar el parámetro 'fila' en lugar de números fijos
        tk.Label(padre, text="Contraseña:", bg="white", font=("Arial", 10)).grid(row=fila, column=0, sticky="w", pady=5)
        self.password_entry = ttk.Entry(padre, show="*", width=30, font=("Arial", 10), style="TEntry")
        self.password_entry.grid(row=fila+1, column=0, columnspan=2, pady=5, sticky="ew")

    def validar_email(self, email):
        return re.match(r'^[\w\.+-]+@[\w\.-]+\.[\w-]+$', email) is not None

    def validar_email_en_tiempo_real(self, event):
        email = self.email_entry.get()
        if email:
            if self.validar_email(email):
                self.email_entry.config(style="TEntry")
            else:
                self.email_entry.config(style="Error.TEntry")
        else:
            self.email_entry.config(style="TEntry")

    def mostrar_error(self, mensaje, widget):
        widget.config(style="Error.TEntry")
        messagebox.showerror("Error", mensaje)

    def iniciar_sesion(self):
        """Verifica los datos de login y cambia a la vista de historial de movimientos."""
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        if not email:
            self.mostrar_error("El email es obligatorio", self.email_entry)
            return
        if not password:
            self.mostrar_error("La contraseña es obligatoria", self.password_entry)
            return
        if not self.validar_email(email):
            self.mostrar_error("Formato de email inválido", self.email_entry)
            return

        try:
            user = auth.sign_in_with_email_and_password(email, password)
            self.email_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.controlador.login(user['idToken'])
        except Exception as e:
            self.manejar_error_login(str(e))

    def manejar_error_login(self, error_msg):
        """Maneja los errores de autenticación de Firebase."""
        if "INVALID_PASSWORD" in error_msg:
            self.mostrar_error("Contraseña incorrecta", self.password_entry)
            self.password_entry.delete(0, tk.END)
        elif "EMAIL_NOT_FOUND" in error_msg:
            self.mostrar_error("Email no registrado", self.email_entry)
        elif "TOO_MANY_ATTEMPTS" in error_msg:
            messagebox.showerror("Bloqueo temporal", "Demasiados intentos fallidos. Intente nuevamente más tarde.")
        else:
            messagebox.showerror("Error", f"Error de autenticación: {error_msg}")