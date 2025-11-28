# views/user_register.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from models.usuario import Usuario

class RegistroUsuarioView:
    def __init__(self, parent):
        self.parent = parent
        self.ventana_reg = None

    def iniciar(self):
        """Paso 1: Pedir código de super usuario."""
        codigo = simpledialog.askstring("Seguridad", "Ingrese código de Super Usuario:", parent=self.parent, show="*")
        
        if codigo == "123456":
            print(">> ACCESO CONCEDIDO: Código de Super Usuario correcto.")
            self.mostrar_ventana_registro()
        elif codigo is None:
            print(">> CANCELADO: El usuario canceló la entrada del código.")
        else:
            print(">> ACCESO DENEGADO: Código incorrecto.")
            messagebox.showerror("Error de Seguridad", "Código de autorización inválido.", parent=self.parent)

    def mostrar_ventana_registro(self):
        """Paso 2: Mostrar formulario de registro con estilo blanco."""
        self.ventana_reg = tk.Toplevel(self.parent)
        self.ventana_reg.title("Registrar Nuevo Usuario")
        self.ventana_reg.geometry("450x550")
        self.ventana_reg.configure(bg="white")
        self.ventana_reg.grab_set() 

        # Contenedor Principal
        frame = tk.Frame(self.ventana_reg, bg="white", padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        # --- Título ---
        tk.Label(frame, text="Nuevo Registro", font=("Arial", 14, "bold"), bg="white").pack(pady=(0, 15))

        # --- Selección de Rol ---
        tk.Label(frame, text="Seleccione el Rol:", bg="white", font=("Arial", 10, "bold")).pack(anchor="w", pady=5)
        
        self.var_rol = tk.StringVar(value="chofer")
        frame_roles = tk.Frame(frame, bg="white")
        frame_roles.pack(fill=tk.X, pady=5)
        
        opciones = [("Chofer", "chofer"), ("General", "general"), ("Admin", "admin")]
        for texto, valor in opciones:
            tk.Radiobutton(frame_roles, text=texto, variable=self.var_rol, value=valor, 
                           bg="white", activebackground="white", 
                           command=self.actualizar_formulario).pack(side=tk.LEFT, padx=10)

        # --- Usuario (Automático) ---
        tk.Label(frame, text="ID de Usuario (Automático):", bg="white").pack(anchor="w", pady=(15,0))
        self.entry_nuevo_user = ttk.Entry(frame, state="readonly")
        self.entry_nuevo_user.pack(fill=tk.X, pady=5)
        
        self.generar_codigo_usuario()

        # --- Contraseña ---
        tk.Label(frame, text="Contraseña:", bg="white").pack(anchor="w", pady=(10,0))
        self.entry_nuevo_pass = ttk.Entry(frame, show="*")
        self.entry_nuevo_pass.pack(fill=tk.X, pady=5)

        # --- Teléfono ---
        tk.Label(frame, text="Teléfono:", bg="white").pack(anchor="w", pady=(10,0))
        self.entry_telefono = ttk.Entry(frame)
        self.entry_telefono.pack(fill=tk.X, pady=5)

        # --- Frame para Licencia (Dinámico) ---
        self.frame_licencia = tk.Frame(frame, bg="white")
        tk.Label(self.frame_licencia, text="No. de Licencia:", bg="white").pack(anchor="w", pady=(10,0))
        self.entry_licencia = ttk.Entry(self.frame_licencia)
        self.entry_licencia.pack(fill=tk.X, pady=5)

        # --- Botones de Acción ---
        frame_btns = tk.Frame(frame, bg="white", pady=20)
        frame_btns.pack(fill=tk.X, side=tk.BOTTOM)
        
        ttk.Button(frame_btns, text="Registrar", command=self.guardar_usuario).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        ttk.Button(frame_btns, text="Cancelar", command=self.ventana_reg.destroy).pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=5)

        self.actualizar_formulario()

    def generar_codigo_usuario(self):
        nuevo_codigo = Usuario.generar_siguiente_codigo_usuario()
        print(f">> Generando nuevo ID sugerido: {nuevo_codigo}")
        self.entry_nuevo_user.config(state="normal")
        self.entry_nuevo_user.delete(0, tk.END)
        self.entry_nuevo_user.insert(0, nuevo_codigo)
        self.entry_nuevo_user.config(state="readonly")

    def actualizar_formulario(self):
        """Muestra u oculta el campo licencia según el rol."""
        rol = self.var_rol.get()
        print(f">> Rol seleccionado: {rol}")

        # AHORA SÍ: Solo Chofer lleva licencia. General y Admin NO.
        if rol == 'chofer':
            self.frame_licencia.pack(fill=tk.X, pady=5)
        else:
            self.frame_licencia.pack_forget()

    def guardar_usuario(self):
        username = self.entry_nuevo_user.get()
        password = self.entry_nuevo_pass.get()
        rol = self.var_rol.get()
        telefono = self.entry_telefono.get()
        
        # Solo capturamos licencia si es chofer
        licencia = self.entry_licencia.get() if rol == 'chofer' else None

        if not password or not telefono:
            messagebox.showwarning("Faltan datos", "La contraseña y el teléfono son obligatorios.", parent=self.ventana_reg)
            return

        if rol == 'chofer' and not licencia:
            messagebox.showwarning("Faltan datos", "Para un chofer, la licencia es obligatoria.", parent=self.ventana_reg)
            return

        print(f">> Intentando registrar: {username} | Rol: {rol}")
        
        if Usuario.crear_usuario(username, password, rol, telefono, licencia):
            print(">> Registro exitoso en BD.")
            messagebox.showinfo("Éxito", f"Usuario {username} registrado correctamente.", parent=self.ventana_reg)
            self.ventana_reg.destroy()
        else:
            print(">> Error al insertar en BD.")
            messagebox.showerror("Error", "No se pudo registrar el usuario.\nVerifique la conexión o si el usuario ya existe.", parent=self.ventana_reg)