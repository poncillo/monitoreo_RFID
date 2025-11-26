import tkinter as tk
from tkinter import ttk, messagebox
from models.database import Database
from models.vehiculo import Vehiculo

class AdminView(tk.Frame):
    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador
        self.configure(bg="white")
        self.pack(fill=tk.BOTH, expand=True)
        self.crear_interfaz()

    def crear_interfaz(self):
        """Crea la interfaz principal del panel admin"""
        # Frame principal
        main_frame = tk.Frame(self, bg="white", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        tk.Label(main_frame, text="Panel de Administración", font=("Arial", 18, "bold"), bg="white").pack(pady=(0, 30))

        # Botones principales
        frame_botones = tk.Frame(main_frame, bg="white")
        frame_botones.pack(fill=tk.X, pady=10)
        # Frame contenedor para centrar los botones
        frame_contenedor = tk.Frame(main_frame, bg="white")
        frame_contenedor.pack(expand=True)  # Esto centra vertical y horizontalmente

        ttk.Button(frame_contenedor, text="👥 Gestionar Usuarios", command=self.gestionar_usuarios, width=20).pack(pady=10)
        
        ttk.Button(frame_contenedor, text="🚗 Gestionar Vehículos", command=self.gestionar_vehiculos, width=20).pack(pady=10)

        ttk.Button(frame_contenedor, text="🚗 Gestionar Rutas", command=self.gestionar_rutas, width=20).pack(pady=10)
        
        ttk.Button(frame_contenedor, text="📊 Ver Reportes", command=self.ver_reportes, width=20).pack(pady=10)

        # Botón cerrar sesión
        ttk.Button(frame_contenedor, text="Cerrar Sesión", command=self.cerrar_sesion, style="Danger.TButton").pack(pady=20)

    def gestionar_usuarios(self):
        """Abre la ventana de gestión de usuarios"""
        ventana_usuarios = tk.Toplevel(self)
        ventana_usuarios.title("Gestión de Usuarios")
        ventana_usuarios.geometry("800x500")
        ventana_usuarios.configure(bg="white")
        ventana_usuarios.grab_set()

        # Título
        tk.Label(ventana_usuarios, text="Gestión de Usuarios", 
                font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        # Treeview para mostrar usuarios
        frame_tabla = tk.Frame(ventana_usuarios, bg="white")
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("ID", "Usuario", "Rol", "Licencia", "Teléfono", "Estado")
        tree = ttk.Treeview(frame_tabla, columns=columns, show="headings", height=15)
        
        # Configurar columnas
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        tree.column("ID", width=50)
        tree.column("Usuario", width=120)
        tree.column("Licencia", width=100)
        tree.column("Teléfono", width=100)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Cargar datos
        self.cargar_usuarios(tree)

        # Frame de botones de acción
        frame_acciones = tk.Frame(ventana_usuarios, bg="white", pady=10)
        frame_acciones.pack(fill=tk.X)

        ttk.Button(frame_acciones, text="Editar Usuario", 
                  command=lambda: self.editar_usuario(tree)).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_acciones, text="Actualizar Lista", 
                  command=lambda: self.cargar_usuarios(tree)).pack(side=tk.LEFT, padx=5)

    def cargar_usuarios(self, tree):
        """Carga los usuarios en el treeview"""
        # Limpiar treeview
        for item in tree.get_children():
            tree.delete(item)
        
        usuarios = Database.obtener_usuarios()
        for usuario in usuarios:
            tree.insert("", tk.END, values=(
                usuario['id'],
                usuario['username'],
                usuario['rol'],
                usuario['licencia'] or "N/A",
                usuario['telefono'],
                usuario['estado']
            ))

    def editar_usuario(self, tree):
        """Abre ventana para editar usuario seleccionado"""
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un usuario para editar.")
            return

        item = tree.item(seleccion[0])
        usuario_id = item['values'][0]
        usuario_username = item['values'][1]

        ventana_editar = tk.Toplevel(self)
        ventana_editar.title(f"Editar Usuario: {usuario_username}")
        ventana_editar.geometry("400x300")
        ventana_editar.configure(bg="white")
        ventana_editar.grab_set()

        # Frame principal
        frame = tk.Frame(ventana_editar, bg="white", padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text=f"Editando: {usuario_username}", 
                font=("Arial", 14, "bold"), bg="white").pack(pady=(0, 20))

        # Cambiar contraseña
        tk.Label(frame, text="Nueva Contraseña:", bg="white").pack(anchor="w", pady=(10,0))
        entry_nueva_pass = ttk.Entry(frame, show="*")
        entry_nueva_pass.pack(fill=tk.X, pady=5)

        # Cambiar teléfono
        tk.Label(frame, text="Nuevo Teléfono:", bg="white").pack(anchor="w", pady=(10,0))
        entry_telefono = ttk.Entry(frame)
        entry_telefono.pack(fill=tk.X, pady=5)

        # Cambiar estado
        tk.Label(frame, text="Estado:", bg="white").pack(anchor="w", pady=(10,0))
        var_estado = tk.StringVar(value="activo")
        frame_estado = tk.Frame(frame, bg="white")
        frame_estado.pack(fill=tk.X, pady=5)
        tk.Radiobutton(frame_estado, text="Activo", variable=var_estado, 
                      value="activo", bg="white").pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(frame_estado, text="Inactivo", variable=var_estado, 
                      value="inactivo", bg="white").pack(side=tk.LEFT, padx=10)

        # Botones de acción
        frame_botones = tk.Frame(frame, bg="white", pady=20)
        frame_botones.pack(fill=tk.X, side=tk.BOTTOM)

        ttk.Button(frame_botones, text="Cambiar Contraseña",
                  command=lambda: self.cambiar_password(usuario_id, entry_nueva_pass.get(), ventana_editar)).pack(side=tk.LEFT, padx=5)

        ttk.Button(frame_botones, text="Cambiar Teléfono",
                  command=lambda: self.cambiar_telefono(usuario_id, entry_telefono.get(), ventana_editar)).pack(side=tk.LEFT, padx=5)

        ttk.Button(frame_botones, text="Cambiar Estado",
                  command=lambda: self.cambiar_estado(usuario_id, var_estado.get(), ventana_editar)).pack(side=tk.LEFT, padx=5)

        ttk.Button(frame_botones, text="Eliminar Usuario", style="Danger.TButton",
                  command=lambda: self.eliminar_usuario(usuario_id, ventana_editar)).pack(side=tk.RIGHT, padx=5)

    def cambiar_password(self, user_id, nueva_password, ventana):
        if not nueva_password:
            messagebox.showwarning("Advertencia", "Ingrese una nueva contraseña.")
            return
        
        if Database.actualizar_usuario(user_id, 'password_hash', nueva_password):
            messagebox.showinfo("Éxito", "Contraseña actualizada correctamente.")
            ventana.destroy()
        else:
            messagebox.showerror("Error", "No se pudo actualizar la contraseña.")

    def cambiar_telefono(self, user_id, nuevo_telefono, ventana):
        if not nuevo_telefono:
            messagebox.showwarning("Advertencia", "Ingrese un nuevo teléfono.")
            return
        
        if Database.actualizar_usuario(user_id, 'telefono', nuevo_telefono):
            messagebox.showinfo("Éxito", "Teléfono actualizado correctamente.")
            ventana.destroy()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el teléfono.")

    def cambiar_estado(self, user_id, nuevo_estado, ventana):
        if Database.actualizar_usuario(user_id, 'estado', nuevo_estado):
            messagebox.showinfo("Éxito", f"Estado cambiado a {nuevo_estado}.")
            ventana.destroy()
        else:
            messagebox.showerror("Error", "No se pudo cambiar el estado.")

    def eliminar_usuario(self, user_id, ventana):
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este usuario? Esta acción no se puede deshacer."):
            if Database.eliminar_usuario(user_id):
                messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
                ventana.destroy()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el usuario.")

    def gestionar_vehiculos(self):
        """Abre la ventana de gestión de vehículos"""
        ventana_vehiculos = tk.Toplevel(self)
        ventana_vehiculos.title("Gestión de Vehículos")
        ventana_vehiculos.geometry("900x600")
        ventana_vehiculos.configure(bg="white")
        ventana_vehiculos.grab_set()

        # Frame principal
        main_frame = tk.Frame(ventana_vehiculos, bg="white", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        tk.Label(main_frame, text="Gestión de Vehículos", 
                font=("Arial", 16, "bold"), bg="white").pack(pady=(0, 10))

        # Botón registrar nuevo vehículo
        ttk.Button(main_frame, text="➕ Registrar Nuevo Vehículo", 
                  command=self.registrar_vehiculo).pack(anchor="w", pady=(0, 10))

        # Treeview para mostrar vehículos
        frame_tabla = tk.Frame(main_frame, bg="white")
        frame_tabla.pack(fill=tk.BOTH, expand=True)

        columns = ("ID", "Placa", "Modelo", "Capacidad", "Estado", "Chofer")
        tree = ttk.Treeview(frame_tabla, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        tree.column("ID", width=50)
        tree.column("Placa", width=100)
        tree.column("Modelo", width=150)
        tree.column("Capacidad", width=80)
        tree.column("Estado", width=100)
        tree.column("Chofer", width=120)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Cargar datos
        self.cargar_vehiculos(tree)

        # Botones de acción
        frame_acciones = tk.Frame(main_frame, bg="white", pady=10)
        frame_acciones.pack(fill=tk.X)

        ttk.Button(frame_acciones, text="Eliminar Vehículo", 
          command=lambda: self.eliminar_vehiculo(tree)).pack(side=tk.LEFT, padx=5)

        ttk.Button(frame_acciones, text="Actualizar Lista", 
                command=lambda: self.cargar_vehiculos(tree)).pack(side=tk.LEFT, padx=5)

    def cargar_vehiculos(self, tree):
        """Carga los vehículos en el treeview"""
        for item in tree.get_children():
            tree.delete(item)
        
        vehiculos = Vehiculo.obtener_todos()
        for vehiculo in vehiculos:
            tree.insert("", tk.END, values=(
                vehiculo['id'],
                vehiculo['placa'],
                vehiculo['modelo'],
                f"{vehiculo['capacidad_cilindros']} cilindros",
                vehiculo['estado'],
                vehiculo['chofer_username'] or "Sin asignar"
            ))

    def registrar_vehiculo(self):
        """Abre ventana para registrar nuevo vehículo"""
        ventana_registro = tk.Toplevel(self)
        ventana_registro.title("Registrar Nuevo Vehículo")
        ventana_registro.geometry("400x500")
        ventana_registro.configure(bg="white")
        ventana_registro.grab_set()

        # Frame principal
        frame = tk.Frame(ventana_registro, bg="white", padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Registrar Nuevo Vehículo", 
                font=("Arial", 14, "bold"), bg="white").pack(pady=(0, 20))

        # Placa
        tk.Label(frame, text="Placa:", bg="white").pack(anchor="w", pady=(10,0))
        entry_placa = ttk.Entry(frame)
        entry_placa.pack(fill=tk.X, pady=5)

        # Modelo (dropdown)
        tk.Label(frame, text="Modelo:", bg="white").pack(anchor="w", pady=(10,0))
        modelos = [
            'np 300 2018', 'np 300 2020', 'np 300 2024',
            'chevrolet s10 2018', 'chevrolet s10 2020', 
            'chevrolet s10 2022', 'chevrolet s10 2024',
            'Ram 4000/3500'
        ]
        combo_modelo = ttk.Combobox(frame, values=modelos, state="readonly")
        combo_modelo.pack(fill=tk.X, pady=5)
        combo_modelo.set(modelos[0])

        # Capacidad (dropdown)
        tk.Label(frame, text="Capacidad de Cilindros:", bg="white").pack(anchor="w", pady=(10,0))
        capacidades = ['15', '20', '35']
        combo_capacidad = ttk.Combobox(frame, values=capacidades, state="readonly")
        combo_capacidad.pack(fill=tk.X, pady=5)
        combo_capacidad.set(capacidades[0])

        # Estado (dropdown)
        tk.Label(frame, text="Estado:", bg="white").pack(anchor="w", pady=(10,0))
        estados = ['disponible', 'mantenimiento', 'ocupado']
        combo_estado = ttk.Combobox(frame, values=estados, state="readonly")
        combo_estado.pack(fill=tk.X, pady=5)
        combo_estado.set('disponible')

        # Chofer (dropdown)
        tk.Label(frame, text="Asignar Chofer (Opcional):", bg="white").pack(anchor="w", pady=(10,0))
        choferes = Vehiculo.obtener_choferes_disponibles()
        chofer_options = ["Sin asignar"] + [f"{ch['username']} ({ch['licencia']})" for ch in choferes]
        combo_chofer = ttk.Combobox(frame, values=chofer_options, state="readonly")
        combo_chofer.pack(fill=tk.X, pady=5)
        combo_chofer.set("Sin asignar")

        # Botones
        frame_botones = tk.Frame(frame, bg="white", pady=20)
        frame_botones.pack(fill=tk.X, side=tk.BOTTOM)

        ttk.Button(frame_botones, text="Registrar", 
                  command=lambda: self.guardar_vehiculo(
                      entry_placa.get(),
                      combo_modelo.get(),
                      combo_capacidad.get(),
                      combo_estado.get(),
                      combo_chofer.get(),
                      choferes,
                      ventana_registro
                  )).pack(side=tk.LEFT, padx=5)

        ttk.Button(frame_botones, text="Cancelar", 
                  command=ventana_registro.destroy).pack(side=tk.RIGHT, padx=5)
    
    def eliminar_vehiculo(self, tree):
        """Elimina el vehículo seleccionado"""
        from models.vehiculo import Vehiculo
        
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un vehículo para eliminar.")
            return

        item = tree.item(seleccion[0])
        vehiculo_id = item['values'][0]
        placa = item['values'][1]
        modelo = item['values'][2]

        if messagebox.askyesno("Confirmar Eliminación", 
                            f"¿Está seguro de eliminar el vehículo:\n{placa} - {modelo}?"):
            print(f">> Intentando eliminar vehículo: {placa} (ID: {vehiculo_id})")
            if Vehiculo.eliminar_vehiculo(vehiculo_id):
                messagebox.showinfo("Éxito", "Vehículo eliminado correctamente.")
                self.cargar_vehiculos(tree)
            else:
                messagebox.showerror("Error", "No se pudo eliminar el vehículo.")

    def guardar_vehiculo(self, placa, modelo, capacidad, estado, chofer_seleccionado, choferes_lista, ventana):
        """Guarda el nuevo vehículo en la base de datos"""
        if not placa:
            messagebox.showwarning("Advertencia", "La placa es obligatoria.")
            return

        # Determinar chofer_id
        chofer_id = None
        if chofer_seleccionado != "Sin asignar":
            # Extraer el ID del chofer seleccionado
            chofer_username = chofer_seleccionado.split(' ')[0]
            for chofer in choferes_lista:
                if chofer['username'] == chofer_username:
                    chofer_id = chofer['id']
                    break

        if Vehiculo.crear_vehiculo(placa, modelo, int(capacidad), estado, chofer_id):
            messagebox.showinfo("Éxito", "Vehículo registrado correctamente.")
            ventana.destroy()
        else:
            messagebox.showerror("Error", "No se pudo registrar el vehículo. Verifique que la placa no esté duplicada.")

    def gestionar_rutas(self):
        """Abre la ventana de gestión de rutas"""
        from models.ruta import Ruta
        
        ventana_rutas = tk.Toplevel(self)
        ventana_rutas.title("Gestión de Rutas")
        ventana_rutas.geometry("1000x600")
        ventana_rutas.configure(bg="white")
        ventana_rutas.grab_set()

        # Frame principal
        main_frame = tk.Frame(ventana_rutas, bg="white", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        tk.Label(main_frame, text="Gestión de Rutas", 
                font=("Arial", 16, "bold"), bg="white").pack(pady=(0, 10))

        # Botón registrar nueva ruta
        ttk.Button(main_frame, text="➕ Registrar Nueva Ruta", 
                command=self.registrar_ruta).pack(anchor="w", pady=(0, 10))

        # Treeview para mostrar rutas
        frame_tabla = tk.Frame(main_frame, bg="white")
        frame_tabla.pack(fill=tk.BOTH, expand=True)

        columns = ("ID", "Chofer", "Vehículo", "Origen", "Destino", "Distancia", "Tiempo", "Estado")
        tree = ttk.Treeview(frame_tabla, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        tree.column("ID", width=50)
        tree.column("Chofer", width=120)
        tree.column("Vehículo", width=100)
        tree.column("Origen", width=120)
        tree.column("Destino", width=120)
        tree.column("Distancia", width=80)
        tree.column("Tiempo", width=80)
        tree.column("Estado", width=100)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Cargar datos
        self.cargar_rutas(tree)

        # Botones de acción
        frame_acciones = tk.Frame(main_frame, bg="white", pady=10)
        frame_acciones.pack(fill=tk.X)

        ttk.Button(frame_acciones, text="Eliminar Ruta", 
                command=lambda: self.eliminar_ruta(tree)).pack(side=tk.LEFT, padx=5)

        ttk.Button(frame_acciones, text="Actualizar Lista", 
                command=lambda: self.cargar_rutas(tree)).pack(side=tk.LEFT, padx=5)

    def cargar_rutas(self, tree):
        """Carga las rutas en el treeview"""
        from models.ruta import Ruta
        
        for item in tree.get_children():
            tree.delete(item)
        
        rutas = Ruta.obtener_todas()
        print(f">> Cargando {len(rutas)} rutas en la tabla")
        
        for ruta in rutas:
            # Convertir minutos a horas para mostrar
            tiempo_horas = f"{ruta['tiempo_estimado_min'] // 60}h"
            
            tree.insert("", tk.END, values=(
                ruta['id'],
                ruta['chofer_username'] or "N/A",
                ruta['vehiculo_placa'] or "N/A",
                ruta['origen'],
                ruta['destino'],
                f"{ruta['distancia_km']} km",
                tiempo_horas,
                ruta['estado']
            ))

    def eliminar_ruta(self, tree):
        """Elimina la ruta seleccionada"""
        from models.ruta import Ruta
        
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una ruta para eliminar.")
            return

        item = tree.item(seleccion[0])
        ruta_id = item['values'][0]
        origen = item['values'][3]
        destino = item['values'][4]

        if messagebox.askyesno("Confirmar Eliminación", 
                            f"¿Está seguro de eliminar la ruta:\n{origen} → {destino}?"):
            if Ruta.eliminar_ruta(ruta_id):
                messagebox.showinfo("Éxito", "Ruta eliminada correctamente.")
                self.cargar_rutas(tree)
            else:
                messagebox.showerror("Error", "No se pudo eliminar la ruta.")

    def registrar_ruta(self):
        """Abre ventana para registrar nueva ruta"""
        from models.ruta import Ruta
        
        ventana_registro = tk.Toplevel(self)
        ventana_registro.title("Registrar Nueva Ruta")
        ventana_registro.geometry("500x600")
        ventana_registro.configure(bg="white")
        ventana_registro.grab_set()

        # Frame principal
        frame = tk.Frame(ventana_registro, bg="white", padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Registrar Nueva Ruta", 
                font=("Arial", 14, "bold"), bg="white").pack(pady=(0, 20))

        # Chofer (dropdown)
        tk.Label(frame, text="Chofer Asignado:", bg="white").pack(anchor="w", pady=(10,0))
        choferes = Ruta.obtener_choferes_con_vehiculos()
        chofer_options = [f"{ch['username']} ({ch['licencia']})" for ch in choferes]
        
        if not chofer_options:
            messagebox.showwarning("Advertencia", "No hay choferes con vehículos asignados disponibles.")
            ventana_registro.destroy()
            return
        
        var_chofer = tk.StringVar()
        combo_chofer = ttk.Combobox(frame, values=chofer_options, state="readonly", textvariable=var_chofer)
        combo_chofer.pack(fill=tk.X, pady=5)
        combo_chofer.set(chofer_options[0])
        
        # Vehículo (se actualiza automáticamente al seleccionar chofer)
        tk.Label(frame, text="Vehículo Asignado:", bg="white").pack(anchor="w", pady=(10,0))
        label_vehiculo = tk.Label(frame, text="Seleccione un chofer", bg="white", fg="blue")
        label_vehiculo.pack(fill=tk.X, pady=5)

        # Variables para almacenar IDs
        self.chofer_id_seleccionado = None
        self.vehiculo_id_seleccionado = None

        def actualizar_vehiculo(*args):
            chofer_seleccionado = var_chofer.get()
            if chofer_seleccionado:
                chofer_username = chofer_seleccionado.split(' ')[0]
                for chofer in choferes:
                    if chofer['username'] == chofer_username:
                        vehiculo_info = f"{chofer['placa']} - {chofer['modelo']}"
                        label_vehiculo.config(text=vehiculo_info)
                        self.chofer_id_seleccionado = chofer['id']
                        self.vehiculo_id_seleccionado = chofer['vehiculo_id']
                        print(f">> Vehículo actualizado: {vehiculo_info}")
                        print(f">> Chofer ID: {self.chofer_id_seleccionado}, Vehículo ID: {self.vehiculo_id_seleccionado}")
                        break

        var_chofer.trace('w', actualizar_vehiculo)
        actualizar_vehiculo()  # Llamar inicialmente

        # Origen
        tk.Label(frame, text="Origen:", bg="white").pack(anchor="w", pady=(10,0))
        entry_origen = ttk.Entry(frame)
        entry_origen.pack(fill=tk.X, pady=5)

        # Destino
        tk.Label(frame, text="Destino:", bg="white").pack(anchor="w", pady=(10,0))
        entry_destino = ttk.Entry(frame)
        entry_destino.pack(fill=tk.X, pady=5)

        # Distancia
        tk.Label(frame, text="Distancia (km):", bg="white").pack(anchor="w", pady=(10,0))
        entry_distancia = ttk.Entry(frame)
        entry_distancia.pack(fill=tk.X, pady=5)

        # Tiempo estimado (dropdown)
        tk.Label(frame, text="Tiempo Estimado (horas):", bg="white").pack(anchor="w", pady=(10,0))
        tiempos = ['2', '4', '8', '10']
        combo_tiempo = ttk.Combobox(frame, values=tiempos, state="readonly")
        combo_tiempo.pack(fill=tk.X, pady=5)
        combo_tiempo.set(tiempos[0])

        # Estado (dropdown)
        tk.Label(frame, text="Estado:", bg="white").pack(anchor="w", pady=(10,0))
        estados = ['programada', 'en_camino', 'completada', 'cancelada']
        combo_estado = ttk.Combobox(frame, values=estados, state="readonly")
        combo_estado.pack(fill=tk.X, pady=5)
        combo_estado.set('programada')

        # Botones
        frame_botones = tk.Frame(frame, bg="white", pady=20)
        frame_botones.pack(fill=tk.X, side=tk.BOTTOM)

        ttk.Button(frame_botones, text="Registrar Ruta", 
                command=lambda: self.guardar_ruta(
                    self.chofer_id_seleccionado,
                    self.vehiculo_id_seleccionado,
                    entry_origen.get(),
                    entry_destino.get(),
                    entry_distancia.get(),
                    combo_tiempo.get(),
                    combo_estado.get(),
                    ventana_registro
                )).pack(side=tk.LEFT, padx=5)

        ttk.Button(frame_botones, text="Cancelar", 
                command=ventana_registro.destroy).pack(side=tk.RIGHT, padx=5)

    def guardar_ruta(self, chofer_id, vehiculo_id, origen, destino, distancia, tiempo_horas, estado, ventana):
        """Guarda la nueva ruta en la base de datos"""
        from models.ruta import Ruta
        
        # Validaciones
        if not origen or not destino:
            messagebox.showwarning("Advertencia", "Origen y destino son obligatorios.")
            return

        if not distancia or not distancia.isdigit():
            messagebox.showwarning("Advertencia", "La distancia debe ser un número válido.")
            return

        if not chofer_id or not vehiculo_id:
            messagebox.showwarning("Advertencia", "Debe seleccionar un chofer con vehículo asignado.")
            return

        # Convertir tiempo de horas a minutos
        tiempo_minutos = int(tiempo_horas) * 60

        print(f">> Guardando ruta: {origen} -> {destino}")
        print(f">> Detalles: {distancia}km, {tiempo_horas}h, estado: {estado}")

        if Ruta.crear_ruta(chofer_id, vehiculo_id, origen, destino, float(distancia), tiempo_minutos, estado):
            messagebox.showinfo("Éxito", "Ruta registrada correctamente.")
            ventana.destroy()
        else:
            messagebox.showerror("Error", "No se pudo registrar la ruta.")

    def ver_reportes(self):
        """Placeholder para reportes"""
        messagebox.showinfo("Reportes", "Módulo de reportes - Por implementar")

    def cerrar_sesion(self):
        """Cierra la sesión del administrador"""
        if self.controlador:
            self.controlador.cerrar_sesion()