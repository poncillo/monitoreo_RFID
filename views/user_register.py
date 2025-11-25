import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from models.usuario import Usuario
from db_connection import create_connection

class RegistroUsuarioView:
    def __init__(self, parent):
        self.parent = parent
        self.ventana_reg = None
        self.frame_licencia = None

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
        self.ventana_reg.geometry("450x500")
        self.ventana_reg.configure(bg="white")
        self.ventana_reg.grab_set() 

        # Contenedor Principal
        frame = tk.Frame(self.ventana_reg, bg="white", padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Nuevo Registro", font=("Arial", 14, "bold"), bg="white").pack(pady=(0, 15))

        tk.Label(frame, text="Seleccione el Rol:", bg="white", font=("Arial", 10, "bold")).pack(anchor="w", pady=5)
        
        self.var_rol = tk.StringVar(value="chofer")
        frame_roles = tk.Frame(frame, bg="white")
        frame_roles.pack(fill=tk.X, pady=5)
        
        opciones = [("Chofer", "chofer"), ("General", "general"), ("Admin", "admin")]
        for texto, valor in opciones:
            tk.Radiobutton(frame_roles, text=texto, variable=self.var_rol, value=valor, 
                           bg="white", activebackground="white", 
                           command=self.actualizar_formulario).pack(side=tk.LEFT, padx=10)

        tk.Label(frame, text="Código de Usuario:", bg="white").pack(anchor="w", pady=(15,0))
        self.entry_username = ttk.Entry(frame, state="readonly", foreground="blue", font=("Arial", 10, "bold"))
        self.entry_username.pack(fill=tk.X, pady=5)
        
        self.actualizar_codigo_usuario()

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

        # Actualizar formulario después de crear todos los componentes
        self.actualizar_formulario()

    def generar_codigo_usuario_emp(self):
        """
        Genera código de usuario en formato EMP-PG## 
        Busca el siguiente número disponible que no esté en uso
        """
        conn = create_connection()
        if not conn:
            return "EMP-PG01"  # Fallback

        try:
            cursor = conn.cursor()
            
            # Buscar todos los códigos existentes que sigan el patrón EMP-PG##
            cursor.execute("SELECT username FROM users WHERE username LIKE 'EMP-PG%'")
            resultados = cursor.fetchall()
            
            # Extraer números existentes
            numeros_existentes = []
            for resultado in resultados:
                try:
                    # Extraer el número del código (ej: "EMP-PG01" -> 1)
                    numero = int(resultado[0].replace("EMP-PG", ""))
                    numeros_existentes.append(numero)
                except ValueError:
                    continue
            
            # Encontrar el siguiente número disponible
            siguiente_numero = 1
            while siguiente_numero in numeros_existentes:
                siguiente_numero += 1
            
            # Formatear como EMP-PG01, EMP-PG02, etc.
            codigo = f"EMP-PG{siguiente_numero:02d}"
            
            cursor.close()
            conn.close()
            return codigo
            
        except Exception as e:
            print(f"Error al generar código de usuario: {e}")
            if conn.is_connected():
                conn.close()
            return "EMP-PG01"

    def actualizar_codigo_usuario(self):
        """Actualiza el campo de username con el código generado"""
        codigo = self.generar_codigo_usuario_emp()
        print(f">> Código de usuario generado: {codigo}")
        self.entry_username.config(state="normal")
        self.entry_username.delete(0, tk.END)
        self.entry_username.insert(0, codigo)
        self.entry_username.config(state="readonly")

    def actualizar_formulario(self):
        """Muestra u oculta el campo licencia según el rol."""
        rol = self.var_rol.get()
        print(f">> Rol seleccionado: {rol}")

        if hasattr(self, 'frame_licencia') and self.frame_licencia is not None:
            if rol == 'chofer':
                # Mostrar licencia solo para chofer
                self.frame_licencia.pack(fill=tk.X, pady=5)
            else:
                # Ocultar para otros roles
                self.frame_licencia.pack_forget()

    def guardar_usuario(self):
        # Obtener el código de usuario del campo (que es de solo lectura)
        username = self.entry_username.get()aaa
        password = self.entry_nuevo_pass.get()
        rol = self.var_rol.get()
        telefono = self.entry_telefono.get()
        
        # Solo capturamos licencia si es chofer
        licencia = self.entry_licencia.get() if rol == 'chofer' else None

        # Validaciones
        if not password:
            messagebox.showwarning("Faltan datos", "La contraseña es obligatoria.", parent=self.ventana_reg)
            self.entry_nuevo_pass.focus()
            return

        if not telefono:
            messagebox.showwarning("Faltan datos", "El teléfono es obligatorio.", parent=self.ventana_reg)
            self.entry_telefono.focus()
            return

        if rol == 'chofer' and not licencia:
            messagebox.showwarning("Faltan datos", "Para un chofer, la licencia es obligatoria.", parent=self.ventana_reg)
            self.entry_licencia.focus()
            return

        print(f">> Intentando registrar: {username} | Rol: {rol}")
        
        if Usuario.crear_usuario(username, password, rol, telefono, licencia):
            print(">> Registro exitoso en BD.")
            # Mostrar confirmación con el código
            messagebox.showinfo("Éxito", 
                               f"Usuario registrado correctamente.\n\n"
                               f"Código: {username}\n"
                               f"Rol: {rol}\n\n"
                               f"Este código se usará para iniciar sesión.", 
                               parent=self.ventana_reg)
            self.ventana_reg.destroy()
        else:
            print(">> Error al insertar en BD.")
            messagebox.showerror("Error", 
                                "No se pudo registrar el usuario.\n"
                                "Puede que el código ya esté en uso.\n"
                                "Intente registrar nuevamente.", 
                                parent=self.ventana_reg)
            # Regenerar código en caso de error
            self.actualizar_codigo_usuario()