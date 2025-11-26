import tkinter as tk
from tkinter import ttk, messagebox
from models.database import Database
from models.vehiculo import Vehiculo
from models.ruta import Ruta
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
from datetime import datetime

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
                font=("Arial", 18, "bold"), bg="white").pack(pady=(0, 30))

        # Frame contenedor para centrar los botones y acomodarse sin darle geometría completamente específica
        frame_contenedor = tk.Frame(main_frame, bg="white")
        frame_contenedor.pack(expand=True)

        ttk.Button(frame_contenedor, text="👥 Visualizar Usuarios", 
                  command=self.visualizar_usuarios, width=20).pack(pady=10)
        
        ttk.Button(frame_contenedor, text="🚗 Visualizar Vehículos", 
                  command=self.visualizar_vehiculos, width=20).pack(pady=10)
        
        ttk.Button(frame_contenedor, text="🗺️ Visualizar Rutas", 
                  command=self.visualizar_rutas, width=20).pack(pady=10)

        ttk.Button(frame_contenedor, text="⛽ Gestionar Cilindros", 
                  command=self.gestionar_cilindros, width=20).pack(pady=10)

        ttk.Button(frame_contenedor, text="Cerrar Sesión", 
                  command=self.cerrar_sesion).pack(pady=20)

    def visualizar_usuarios(self):
        """Muestra ventana para visualizar usuarios"""
        ventana_usuarios = tk.Toplevel(self)
        ventana_usuarios.title("Visualización de Usuarios")
        ventana_usuarios.geometry("800x500")
        ventana_usuarios.configure(bg="white")
        ventana_usuarios.grab_set()

        # Título
        tk.Label(ventana_usuarios, text="Usuarios del Sistema", 
                font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        # Treeview para mostrar usuarios
        frame_tabla = tk.Frame(ventana_usuarios, bg="white")
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("Usuario", "Rol", "Teléfono", "Estado")
        tree = ttk.Treeview(frame_tabla, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Cargar datos
        self.cargar_usuarios_general(tree)

        # Botones de exportación
        frame_acciones = tk.Frame(ventana_usuarios, bg="white", pady=10)
        frame_acciones.pack(fill=tk.X)

        ttk.Button(frame_acciones, text="📊 Exportar a Excel", 
                  command=lambda: self.exportar_usuarios_excel()).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_acciones, text="📄 Exportar a PDF", 
                  command=lambda: self.exportar_usuarios_pdf()).pack(side=tk.LEFT, padx=5)

        ttk.Button(frame_acciones, text="Actualizar", 
                  command=lambda: self.cargar_usuarios_general(tree)).pack(side=tk.LEFT, padx=5)

    def cargar_usuarios_general(self, tree):
        """Carga los usuarios en el treeview (sin contraseñas)"""
        for item in tree.get_children():
            tree.delete(item)
        
        usuarios = Database.obtener_usuarios()
        print(f">> Cargando {len(usuarios)} usuarios para visualización general")
        
        for usuario in usuarios:
            tree.insert("", tk.END, values=(
                usuario['username'],
                usuario['rol'],
                usuario['telefono'],
                usuario['estado']
            ))

    def visualizar_vehiculos(self):
        """Muestra ventana para visualizar vehículos"""
        ventana_vehiculos = tk.Toplevel(self)
        ventana_vehiculos.title("Visualización de Vehículos")
        ventana_vehiculos.geometry("900x500")
        ventana_vehiculos.configure(bg="white")
        ventana_vehiculos.grab_set()

        # Título
        tk.Label(ventana_vehiculos, text="Vehículos del Sistema", 
                font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        # Treeview para mostrar vehículos
        frame_tabla = tk.Frame(ventana_vehiculos, bg="white")
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("Placa", "Modelo", "Capacidad", "Estado", "Chofer")
        tree = ttk.Treeview(frame_tabla, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Cargar datos
        self.cargar_vehiculos_general(tree)

        frame_acciones = tk.Frame(ventana_vehiculos, bg="white", pady=10)
        frame_acciones.pack(fill=tk.X)

        ttk.Button(frame_acciones, text="📊 Exportar a Excel", 
                  command=lambda: self.exportar_vehiculos_excel()).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_acciones, text="📄 Exportar a PDF", 
                  command=lambda: self.exportar_vehiculos_pdf()).pack(side=tk.LEFT, padx=5)

        ttk.Button(frame_acciones, text="Actualizar", 
                  command=lambda: self.cargar_vehiculos_general(tree)).pack(side=tk.LEFT, padx=5)

    def cargar_vehiculos_general(self, tree):
        """Carga los vehículos en el treeview"""
        for item in tree.get_children():
            tree.delete(item)
        
        vehiculos = Vehiculo.obtener_todos()
        print(f">> Cargando {len(vehiculos)} vehículos para visualización general")
        
        for vehiculo in vehiculos:
            tree.insert("", tk.END, values=(
                vehiculo['placa'],
                vehiculo['modelo'],
                f"{vehiculo['capacidad_cilindros']} cilindros",
                vehiculo['estado'],
                vehiculo['chofer_username'] or "Sin asignar"
            ))

    def visualizar_rutas(self):
        """Muestra ventana para visualizar rutas"""
        ventana_rutas = tk.Toplevel(self)
        ventana_rutas.title("Visualización de Rutas")
        ventana_rutas.geometry("1000x500")
        ventana_rutas.configure(bg="white")
        ventana_rutas.grab_set()

        # Título
        tk.Label(ventana_rutas, text="Rutas del Sistema", 
                font=("Arial", 16, "bold"), bg="white").pack(pady=10)

        # Treeview para mostrar rutas
        frame_tabla = tk.Frame(ventana_rutas, bg="white")
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

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
        self.cargar_rutas_general(tree)

        frame_acciones = tk.Frame(ventana_rutas, bg="white", pady=10)
        frame_acciones.pack(fill=tk.X)

        ttk.Button(frame_acciones, text="📊 Exportar a Excel", 
                  command=lambda: self.exportar_rutas_excel()).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_acciones, text="📄 Exportar a PDF", 
                  command=lambda: self.exportar_rutas_pdf()).pack(side=tk.LEFT, padx=5)

        ttk.Button(frame_acciones, text="Actualizar", 
                  command=lambda: self.cargar_rutas_general(tree)).pack(side=tk.LEFT, padx=5)

    def cargar_rutas_general(self, tree):
        """Carga las rutas en el treeview"""
        from models.ruta import Ruta
        
        for item in tree.get_children():
            tree.delete(item)
        
        rutas = Ruta.obtener_todas()
        print(f">> Cargando {len(rutas)} rutas para visualización general")
        
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

    # Métodos de exportación a Excel
    def exportar_usuarios_excel(self):
        """Exporta usuarios a Excel"""
        try:
            from tkinter import filedialog
            
            usuarios = Database.obtener_usuarios()
            df = pd.DataFrame([(u['username'], u['rol'], u['telefono'], u['estado']) 
                            for u in usuarios],
                            columns=['Usuario', 'Rol', 'Teléfono', 'Estado'])
            
            # Cuadro de diálogo para elegir ubicación
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Guardar reporte de usuarios como..."
            )
            
            if filename:  # Si el usuario no cancela
                df.to_excel(filename, index=False)
                messagebox.showinfo("Éxito", f"Usuarios exportados a {filename}")
                print(f">> Usuarios exportados a Excel: {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {str(e)}")
            print(f">> Error exportando usuarios a Excel: {e}")

    def exportar_vehiculos_excel(self):
        """Exporta vehículos a Excel"""
        try:
            from tkinter import filedialog
            
            vehiculos = Vehiculo.obtener_todos()
            df = pd.DataFrame([(v['placa'], v['modelo'], v['capacidad_cilindros'], 
                            v['estado'], v['chofer_username'] or "Sin asignar") 
                            for v in vehiculos],
                            columns=['Placa', 'Modelo', 'Capacidad', 'Estado', 'Chofer'])
            
            # Cuadro de diálogo para elegir ubicación
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Guardar reporte de vehículos como..."
            )
            
            if filename:  # Si el usuario no cancela
                df.to_excel(filename, index=False)
                messagebox.showinfo("Éxito", f"Vehículos exportados a {filename}")
                print(f">> Vehículos exportados a Excel: {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {str(e)}")
            print(f">> Error exportando vehículos a Excel: {e}")

    def exportar_rutas_excel(self):
        """Exporta rutas a Excel"""
        try:
            from tkinter import filedialog
            from models.ruta import Ruta
            
            rutas = Ruta.obtener_todas()
            df = pd.DataFrame([(r['id'], r['chofer_username'] or "N/A", 
                            r['vehiculo_placa'] or "N/A", r['origen'], 
                            r['destino'], r['distancia_km'], 
                            r['tiempo_estimado_min'] // 60, r['estado']) 
                            for r in rutas],
                            columns=['ID', 'Chofer', 'Vehículo', 'Origen', 'Destino', 
                                'Distancia_km', 'Tiempo_horas', 'Estado'])
            
            # Cuadro de diálogo para elegir ubicación
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Guardar reporte de rutas como..."
            )
            
            if filename:  # Si el usuario no cancela
                df.to_excel(filename, index=False)
                messagebox.showinfo("Éxito", f"Rutas exportadas a {filename}")
                print(f">> Rutas exportadas a Excel: {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {str(e)}")
            print(f">> Error exportando rutas a Excel: {e}")

    # Métodos de exportación a PDF
    def exportar_usuarios_pdf(self):
        """Exporta usuarios a PDF"""
        try:
            from tkinter import filedialog
            
            usuarios = Database.obtener_usuarios()
            
            # Cuadro de diálogo para elegir ubicación
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                title="Guardar reporte de usuarios como..."
            )
            
            if not filename:  # Si el usuario cancela
                return
                
            c = canvas.Canvas(filename, pagesize=letter)
            c.setFont("Helvetica", 12)
            c.drawString(100, 750, "Reporte de Usuarios")
            c.drawString(100, 730, f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            y = 700
            for usuario in usuarios:
                if y < 100:
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y = 750
                
                texto = f"Usuario: {usuario['username']} | Rol: {usuario['rol']} | Tel: {usuario['telefono']} | Estado: {usuario['estado']}"
                c.drawString(50, y, texto)
                y -= 20
            
            c.save()
            messagebox.showinfo("Éxito", f"Usuarios exportados a {filename}")
            print(f">> Usuarios exportados a PDF: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {str(e)}")
            print(f">> Error exportando usuarios a PDF: {e}")

    def exportar_vehiculos_pdf(self):
        """Exporta vehículos a PDF"""
        try:
            from tkinter import filedialog
            
            vehiculos = Vehiculo.obtener_todos()
            
            # Cuadro de diálogo para elegir ubicación
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                title="Guardar reporte de vehículos como..."
            )
            
            if not filename:  # Si el usuario cancela
                return
                
            c = canvas.Canvas(filename, pagesize=letter)
            c.setFont("Helvetica", 12)
            c.drawString(100, 750, "Reporte de Vehículos")
            c.drawString(100, 730, f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            y = 700
            for vehiculo in vehiculos:
                if y < 100:
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y = 750
                
                texto = f"Placa: {vehiculo['placa']} | Modelo: {vehiculo['modelo']} | Capacidad: {vehiculo['capacidad_cilindros']} | Estado: {vehiculo['estado']}"
                c.drawString(50, y, texto)
                y -= 20
            
            c.save()
            messagebox.showinfo("Éxito", f"Vehículos exportados a {filename}")
            print(f">> Vehículos exportados a PDF: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {str(e)}")
            print(f">> Error exportando vehículos a PDF: {e}")

    def exportar_rutas_pdf(self):
        """Exporta rutas a PDF"""
        try:
            from tkinter import filedialog
            from models.ruta import Ruta
            
            rutas = Ruta.obtener_todas()
            
            # Cuadro de diálogo para elegir ubicación
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                title="Guardar reporte de rutas como..."
            )
            
            if not filename:  # Si el usuario cancela
                return
                
            c = canvas.Canvas(filename, pagesize=letter)
            c.setFont("Helvetica", 12)
            c.drawString(100, 750, "Reporte de Rutas")
            c.drawString(100, 730, f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            y = 700
            for ruta in rutas:
                if y < 100:
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y = 750
                
                texto = f"Ruta {ruta['id']}: {ruta['origen']} → {ruta['destino']} | Chofer: {ruta['chofer_username']} | Estado: {ruta['estado']}"
                c.drawString(50, y, texto)
                y -= 20
            
            c.save()
            messagebox.showinfo("Éxito", f"Rutas exportadas a {filename}")
            print(f">> Rutas exportadas a PDF: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {str(e)}")
            print(f">> Error exportando rutas a PDF: {e}")

    # ========== MÉTODOS PARA GESTIÓN DE CILINDROS ==========
    
    def gestionar_cilindros(self):
        """Abre la ventana de gestión de cilindros"""
        from models.cilindro import Cilindro
        
        ventana_cilindros = tk.Toplevel(self)
        ventana_cilindros.title("Gestión de Cilindros")
        ventana_cilindros.geometry("1000x600")
        ventana_cilindros.configure(bg="white")
        ventana_cilindros.grab_set()

        # Frame principal
        main_frame = tk.Frame(ventana_cilindros, bg="white", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        tk.Label(main_frame, text="Gestión de Cilindros", 
                font=("Arial", 16, "bold"), bg="white").pack(pady=(0, 10))

        # Botón registrar nuevo cilindro
        ttk.Button(main_frame, text="➕ Registrar Nuevo Cilindro", 
                command=self.registrar_cilindro).pack(anchor="w", pady=(0, 10))

        # Treeview para mostrar cilindros
        frame_tabla = tk.Frame(main_frame, bg="white")
        frame_tabla.pack(fill=tk.BOTH, expand=True)

        columns = ("ID", "RFID", "Capacidad", "Estado", "Último Mant.", "Vehículo", "Chofer")
        tree = ttk.Treeview(frame_tabla, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        tree.column("ID", width=50)
        tree.column("RFID", width=120)
        tree.column("Capacidad", width=80)
        tree.column("Estado", width=100)
        tree.column("Último Mant.", width=100)
        tree.column("Vehículo", width=100)
        tree.column("Chofer", width=120)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Cargar datos
        self.cargar_cilindros(tree)

        # Botones de acción
        frame_acciones = tk.Frame(main_frame, bg="white", pady=10)
        frame_acciones.pack(fill=tk.X)

        ttk.Button(frame_acciones, text="📊 Exportar a Excel", 
                command=lambda: self.exportar_cilindros_excel()).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame_acciones, text="📄 Exportar a PDF", 
                command=lambda: self.exportar_cilindros_pdf()).pack(side=tk.LEFT, padx=5)

        ttk.Button(frame_acciones, text="Eliminar Cilindro", 
                command=lambda: self.eliminar_cilindro(tree)).pack(side=tk.LEFT, padx=5)

        ttk.Button(frame_acciones, text="Actualizar Lista", 
                command=lambda: self.cargar_cilindros(tree)).pack(side=tk.LEFT, padx=5)

    def cargar_cilindros(self, tree):
        """Carga los cilindros en el treeview"""
        from models.cilindro import Cilindro
        
        for item in tree.get_children():
            tree.delete(item)
        
        cilindros = Cilindro.obtener_todos()
        print(f">> Cargando {len(cilindros)} cilindros")
        
        for cilindro in cilindros:
            # Formatear fecha
            fecha_mant = cilindro['fecha_ultimo_mantenimiento']
            if fecha_mant:
                fecha_str = fecha_mant.strftime('%d/%m/%Y') if hasattr(fecha_mant, 'strftime') else str(fecha_mant)
            else:
                fecha_str = "Nunca"
            
            tree.insert("", tk.END, values=(
                cilindro['id'],
                cilindro['codigo_rfid'],
                f"{cilindro['capacidad_kg']} kg",
                cilindro['estado'],
                fecha_str,
                cilindro['vehiculo_placa'] or "Sin asignar",
                cilindro['chofer_username'] or "N/A"
            ))

    def eliminar_cilindro(self, tree):
        """Elimina el cilindro seleccionado"""
        from models.cilindro import Cilindro
        
        seleccion = tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un cilindro para eliminar.")
            return

        item = tree.item(seleccion[0])
        cilindro_id = item['values'][0]
        rfid = item['values'][1]

        if messagebox.askyesno("Confirmar Eliminación", 
                            f"¿Está seguro de eliminar el cilindro:\nRFID: {rfid}?"):
            if Cilindro.eliminar_cilindro(cilindro_id):
                messagebox.showinfo("Éxito", "Cilindro eliminado correctamente.")
                self.cargar_cilindros(tree)
            else:
                messagebox.showerror("Error", "No se pudo eliminar el cilindro.")

    def registrar_cilindro(self):
        """Abre ventana para registrar nuevo cilindro"""
        from models.cilindro import Cilindro
        
        ventana_registro = tk.Toplevel(self)
        ventana_registro.title("Registrar Nuevo Cilindro")
        ventana_registro.geometry("500x600")
        ventana_registro.configure(bg="white")
        ventana_registro.grab_set()

        # Frame principal
        frame = tk.Frame(ventana_registro, bg="white", padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Registrar Nuevo Cilindro", 
                font=("Arial", 14, "bold"), bg="white").pack(pady=(0, 20))

        # RFID
        tk.Label(frame, text="Código RFID:", bg="white").pack(anchor="w", pady=(10,0))
        entry_rfid = ttk.Entry(frame)
        entry_rfid.pack(fill=tk.X, pady=5)

        # Capacidad (dropdown)
        tk.Label(frame, text="Capacidad (kg):", bg="white").pack(anchor="w", pady=(10,0))
        capacidades = ['20', '30']
        combo_capacidad = ttk.Combobox(frame, values=capacidades, state="readonly")
        combo_capacidad.pack(fill=tk.X, pady=5)
        combo_capacidad.set(capacidades[0])

        # Estado (dropdown)
        tk.Label(frame, text="Estado:", bg="white").pack(anchor="w", pady=(10,0))
        estados = ['almacen', 'en_ruta', 'entregado', 'mantenimiento']
        combo_estado = ttk.Combobox(frame, values=estados, state="readonly")
        combo_estado.pack(fill=tk.X, pady=5)
        combo_estado.set('almacen')

        # Fecha último mantenimiento
        tk.Label(frame, text="Fecha Último Mantenimiento:", bg="white").pack(anchor="w", pady=(10,0))
        frame_fecha = tk.Frame(frame, bg="white")
        frame_fecha.pack(fill=tk.X, pady=5)
        
        # Campos de fecha (día, mes, año)
        tk.Label(frame_fecha, text="Día:", bg="white").pack(side=tk.LEFT)
        entry_dia = ttk.Entry(frame_fecha, width=5)
        entry_dia.pack(side=tk.LEFT, padx=2)
        entry_dia.insert(0, datetime.now().strftime('%d'))
        
        tk.Label(frame_fecha, text="Mes:", bg="white").pack(side=tk.LEFT)
        entry_mes = ttk.Entry(frame_fecha, width=5)
        entry_mes.pack(side=tk.LEFT, padx=2)
        entry_mes.insert(0, datetime.now().strftime('%m'))
        
        tk.Label(frame_fecha, text="Año:", bg="white").pack(side=tk.LEFT)
        entry_anio = ttk.Entry(frame_fecha, width=5)
        entry_anio.pack(side=tk.LEFT, padx=2)
        entry_anio.insert(0, datetime.now().strftime('%Y'))

        # Vehículo (dropdown)
        tk.Label(frame, text="Vehículo Asignado:", bg="white").pack(anchor="w", pady=(10,0))
        vehiculos = Cilindro.obtener_vehiculos_disponibles()
        vehiculo_options = ["Sin asignar"] + [f"{v['placa']} - {v['modelo']} ({v['chofer_username']})" for v in vehiculos]
        
        var_vehiculo = tk.StringVar()
        combo_vehiculo = ttk.Combobox(frame, values=vehiculo_options, state="readonly", textvariable=var_vehiculo)
        combo_vehiculo.pack(fill=tk.X, pady=5)
        combo_vehiculo.set("Sin asignar")

        # Chofer (se actualiza automáticamente)
        tk.Label(frame, text="Chofer Asignado:", bg="white").pack(anchor="w", pady=(10,0))
        label_chofer = tk.Label(frame, text="Seleccione un vehículo", bg="white", fg="blue")
        label_chofer.pack(fill=tk.X, pady=5)

        # Variables para almacenar IDs
        self.vehiculo_id_seleccionado = None

        def actualizar_chofer(*args):
            vehiculo_seleccionado = var_vehiculo.get()
            if vehiculo_seleccionado != "Sin asignar":
                # Extraer la placa del vehículo seleccionado
                placa = vehiculo_seleccionado.split(' - ')[0]
                for vehiculo in vehiculos:
                    if vehiculo['placa'] == placa:
                        chofer_info = f"{vehiculo['chofer_username']}"
                        label_chofer.config(text=chofer_info)
                        self.vehiculo_id_seleccionado = vehiculo['id']
                        print(f">> Vehículo seleccionado: {placa}, Chofer: {chofer_info}, ID: {self.vehiculo_id_seleccionado}")
                        break
            else:
                label_chofer.config(text="Sin asignar")
                self.vehiculo_id_seleccionado = None

        var_vehiculo.trace('w', actualizar_chofer)

        # Botones
        frame_botones = tk.Frame(frame, bg="white", pady=20)
        frame_botones.pack(fill=tk.X, side=tk.BOTTOM)

        ttk.Button(frame_botones, text="Registrar Cilindro", 
                command=lambda: self.guardar_cilindro(
                    entry_rfid.get(),
                    combo_capacidad.get(),
                    combo_estado.get(),
                    entry_dia.get(),
                    entry_mes.get(),
                    entry_anio.get(),
                    self.vehiculo_id_seleccionado,
                    ventana_registro
                )).pack(side=tk.LEFT, padx=5)

        ttk.Button(frame_botones, text="Cancelar", 
                command=ventana_registro.destroy).pack(side=tk.RIGHT, padx=5)

    def guardar_cilindro(self, rfid, capacidad, estado, dia, mes, anio, vehiculo_id, ventana):
        """Guarda el nuevo cilindro en la base de datos"""
        from models.cilindro import Cilindro
        
        # Validaciones
        if not rfid:
            messagebox.showwarning("Advertencia", "El código RFID es obligatorio.")
            return

        # Validar y formatear fecha
        try:
            fecha_mantenimiento = f"{anio}-{mes}-{dia}"
            # Validar que sea una fecha real
            datetime.strptime(fecha_mantenimiento, '%Y-%m-%d')
        except ValueError:
            messagebox.showwarning("Advertencia", "La fecha de mantenimiento no es válida.")
            return

        # Si no se selecciona vehículo, establecer como NULL
        if vehiculo_id is None:
            vehiculo_id = None

        print(f">> Guardando cilindro: RFID {rfid}, {capacidad}kg, estado: {estado}")

        if Cilindro.crear_cilindro(rfid, capacidad, estado, fecha_mantenimiento, vehiculo_id):
            messagebox.showinfo("Éxito", "Cilindro registrado correctamente.")
            ventana.destroy()
        else:
            messagebox.showerror("Error", "No se pudo registrar el cilindro. Verifique que el RFID no esté duplicado.")

    def exportar_cilindros_excel(self):
        """Exporta cilindros a Excel"""
        try:
            import pandas as pd
            from tkinter import filedialog
            from models.cilindro import Cilindro
            
            cilindros = Cilindro.obtener_todos()
            df = pd.DataFrame([(
                c['id'],
                c['codigo_rfid'],
                c['capacidad_kg'],
                c['estado'],
                c['fecha_ultimo_mantenimiento'],
                c['vehiculo_placa'] or "Sin asignar",
                c['chofer_username'] or "N/A"
            ) for c in cilindros],
            columns=['ID', 'RFID', 'Capacidad_kg', 'Estado', 'Fecha_Mantenimiento', 'Vehículo', 'Chofer'])
            
            # Cuadro de diálogo para elegir ubicación
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Guardar reporte de cilindros como..."
            )
            
            if filename:  # Si el usuario no cancela
                df.to_excel(filename, index=False)
                messagebox.showinfo("Éxito", f"Cilindros exportados a {filename}")
                print(f">> Cilindros exportados a Excel: {filename}")
                
        except ImportError:
            messagebox.showwarning("Función no disponible", 
                                "La exportación a Excel requiere instalar: pip install pandas openpyxl")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {str(e)}")

    def exportar_cilindros_pdf(self):
        """Exporta cilindros a PDF"""
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            from tkinter import filedialog
            
            from models.cilindro import Cilindro
            cilindros = Cilindro.obtener_todos()
            
            # Cuadro de diálogo para elegir ubicación
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                title="Guardar reporte de cilindros como..."
            )
            
            if not filename:  # Si el usuario cancela
                return
                
            c = canvas.Canvas(filename, pagesize=letter)
            # ... el resto del código permanece igual ...
            c.setFont("Helvetica", 12)
            c.drawString(100, 750, "Reporte de Cilindros")
            c.drawString(100, 730, f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            y = 700
            for cilindro in cilindros:
                if y < 100:
                    c.showPage()
                    c.setFont("Helvetica", 12)
                    y = 750
                
                texto = f"RFID: {cilindro['codigo_rfid']} | Capacidad: {cilindro['capacidad_kg']}kg | Estado: {cilindro['estado']} | Vehículo: {cilindro['vehiculo_placa'] or 'Sin asignar'}"
                c.drawString(50, y, texto)
                y -= 20
            
            c.save()
            messagebox.showinfo("Éxito", f"Cilindros exportados a {filename}")
            print(f">> Cilindros exportados a PDF: {filename}")
        except ImportError:
            messagebox.showwarning("Función no disponible", 
                                "La exportación a PDF requiere instalar: pip install reportlab")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {str(e)}")

    def cerrar_sesion(self):
        """Cierra la sesión del usuario general"""
        if self.controlador:
            self.controlador.cerrar_sesion()