# views/view_chofer.py
import tkinter as tk
from tkinter import ttk, messagebox
from models.vehiculo import Vehiculo
from models.ruta import Ruta
from db_connection import create_connection

class ChoferView(tk.Frame):
    def __init__(self, parent, controlador=None):
        super().__init__(parent)
        self.controlador = controlador
        self.usuario_actual = controlador.usuario_actual if controlador else None
        self.configure(bg="white")
        self.pack(fill=tk.BOTH, expand=True)
        self.crear_interfaz()

    def crear_interfaz(self):
        """Crea la interfaz principal del panel chofer"""
        main_frame = tk.Frame(self, bg="white", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text=f"Panel Chofer - {self.usuario_actual.username if self.usuario_actual else 'Usuario'}", 
                font=("Arial", 18, "bold"), bg="white").pack(pady=(0, 30))

        # Frame contenedor para centrar los botones
        frame_contenedor = tk.Frame(main_frame, bg="white")
        frame_contenedor.pack(expand=True)

        ttk.Button(frame_contenedor, text="🚗 Mis Vehículos", 
                  command=self.visualizar_mis_vehiculos, width=20).pack(pady=10)
        
        ttk.Button(frame_contenedor, text="🗺️ Mis Rutas", 
                  command=self.visualizar_mis_rutas, width=20).pack(pady=10)

        ttk.Button(frame_contenedor, text="Cerrar Sesión", 
                  command=self.cerrar_sesion).pack(pady=20)

    def visualizar_mis_vehiculos(self):
        """Muestra los vehículos asignados al chofer actual"""
        if not self.usuario_actual:
            messagebox.showerror("Error", "No se pudo identificar al usuario actual.")
            return

        ventana_vehiculos = tk.Toplevel(self)
        ventana_vehiculos.title("Mis Vehículos")
        ventana_vehiculos.geometry("700x400")
        ventana_vehiculos.configure(bg="white")
        ventana_vehiculos.grab_set()

        # Título
        tk.Label(ventana_vehiculos, text="Mis Vehículos Asignados", 
                font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        # Treeview para mostrar vehículos
        frame_tabla = tk.Frame(ventana_vehiculos, bg="white")
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("Placa", "Modelo", "Capacidad", "Estado")
        tree = ttk.Treeview(frame_tabla, columns=columns, show="headings", height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Cargar datos
        self.cargar_mis_vehiculos(tree)

        # Botón actualizar
        ttk.Button(ventana_vehiculos, text="Actualizar", 
                  command=lambda: self.cargar_mis_vehiculos(tree)).pack(pady=10)

    def cargar_mis_vehiculos(self, tree):
        """Carga los vehículos del chofer actual"""
        for item in tree.get_children():
            tree.delete(item)
        
        vehiculos = self.obtener_vehiculos_chofer()
        print(f">> Cargando {len(vehiculos)} vehículos para el chofer {self.usuario_actual.username}")
        
        for vehiculo in vehiculos:
            tree.insert("", tk.END, values=(
                vehiculo['placa'],
                vehiculo['modelo'],
                f"{vehiculo['capacidad_cilindros']} cilindros",
                vehiculo['estado']
            ))

    def obtener_vehiculos_chofer(self):
        """Obtiene los vehículos asignados al chofer actual"""
        conn = create_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT placa, modelo, capacidad_cilindros, estado 
                FROM vehiculos 
                WHERE chofer_id = %s
            """
            cursor.execute(query, (self.usuario_actual.id,))
            vehiculos = cursor.fetchall()
            cursor.close()
            conn.close()
            return vehiculos
        except Exception as e:
            print(f"Error al obtener vehículos del chofer: {e}")
            if conn.is_connected():
                conn.close()
            return []

    def visualizar_mis_rutas(self):
        """Muestra las rutas asignadas al chofer actual"""
        if not self.usuario_actual:
            messagebox.showerror("Error", "No se pudo identificar al usuario actual.")
            return

        ventana_rutas = tk.Toplevel(self)
        ventana_rutas.title("Mis Rutas")
        ventana_rutas.geometry("900x500")
        ventana_rutas.configure(bg="white")
        ventana_rutas.grab_set()

        # Título
        tk.Label(ventana_rutas, text="Mis Rutas Asignadas", 
                font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        # Treeview para mostrar rutas
        frame_tabla = tk.Frame(ventana_rutas, bg="white")
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("ID", "Vehículo", "Origen", "Destino", "Distancia", "Tiempo", "Estado")
        tree = ttk.Treeview(frame_tabla, columns=columns, show="headings", height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        tree.column("ID", width=50)
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
        self.cargar_mis_rutas(tree)

        # Frame de botones
        frame_botones = tk.Frame(ventana_rutas, bg="white", pady=10)
        frame_botones.pack(fill=tk.X)

        ttk.Button(frame_botones, text="🔄 Cambiar Estado a 'En Camino'", 
                  command=lambda: self.cambiar_estado_ruta(tree, 'en_camino')).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_botones, text="✅ Cambiar Estado a 'Completada'", 
                  command=lambda: self.cambiar_estado_ruta(tree, 'completada')).pack(side=tk.LEFT, padx=5)

        ttk.Button(frame_botones, text="Actualizar", 
                  command=lambda: self.cargar_mis_rutas(tree)).pack(side=tk.LEFT, padx=5)

    def cargar_mis_rutas(self, tree):
        """Carga las rutas del chofer actual"""
        for item in tree.get_children():
            tree.delete(item)
        
        rutas = self.obtener_rutas_chofer()
        print(f">> Cargando {len(rutas)} rutas para el chofer {self.usuario_actual.username}")
        
        for ruta in rutas:
            # Convertir minutos a horas para mostrar
            tiempo_horas = f"{ruta['tiempo_estimado_min'] // 60}h"
            
            tree.insert("", tk.END, values=(
                ruta['id'],
                ruta['vehiculo_placa'],
                ruta['origen'],
                ruta['destino'],
                f"{ruta['distancia_km']} km",
                tiempo_horas,
                ruta['estado']
            ))

    def obtener_rutas_chofer(self):
        """Obtiene las rutas asignadas al chofer actual"""
        conn = create_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT r.*, v.placa as vehiculo_placa
                FROM rutas r 
                JOIN vehiculos v ON r.vehiculo_id = v.id
                WHERE r.chofer_id = %s
            """
            cursor.execute(query, (self.usuario_actual.id,))
            rutas = cursor.fetchall()
            cursor.close()
            conn.close()
            return rutas
        except Exception as e:
            print(f"Error al obtener rutas del chofer: {e}")
            if conn.is_connected():
                conn.close()
            return []

    def cambiar_estado_ruta(self, tree, nuevo_estado):
        """Cambia el estado de la ruta seleccionada"""
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione una ruta para cambiar su estado.")
            return

        item = tree.item(seleccion[0])
        ruta_id = item['values'][0]
        estado_actual = item['values'][6]
        origen = item['values'][2]
        destino = item['values'][3]

        # Validar transición de estado
        if estado_actual == 'completada':
            messagebox.showwarning("Advertencia", "No se puede modificar una ruta completada.")
            return

        if estado_actual == nuevo_estado:
            messagebox.showwarning("Advertencia", f"La ruta ya está en estado '{nuevo_estado}'.")
            return

        if messagebox.askyesno("Confirmar Cambio", 
                              f"¿Cambiar estado de la ruta {origen} → {destino} a '{nuevo_estado}'?"):
            if self.actualizar_estado_ruta(ruta_id, nuevo_estado):
                messagebox.showinfo("Éxito", f"Estado de la ruta cambiado a '{nuevo_estado}'.")
                print(f">> Ruta {ruta_id} cambiada a estado: {nuevo_estado}")
                self.cargar_mis_rutas(tree)
            else:
                messagebox.showerror("Error", "No se pudo cambiar el estado de la ruta.")

    def actualizar_estado_ruta(self, ruta_id, nuevo_estado):
        """Actualiza el estado de una ruta en la base de datos"""
        conn = create_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            query = "UPDATE rutas SET estado = %s WHERE id = %s"
            cursor.execute(query, (nuevo_estado, ruta_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al actualizar estado de ruta: {e}")
            if conn.is_connected():
                conn.close()
            return False

    def cerrar_sesion(self):
        """Cierra la sesión del chofer"""
        if self.controlador:
            self.controlador.cerrar_sesion()