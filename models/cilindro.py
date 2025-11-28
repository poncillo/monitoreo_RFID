# models/cilindro.py
from db_connection import create_connection
from datetime import datetime

class Cilindro:
    def __init__(self, id, codigo_rfid, capacidad_kg, estado, fecha_ultimo_mantenimiento, vehiculo_id, ruta_id=None):
        self.id = id
        self.codigo_rfid = codigo_rfid
        self.capacidad_kg = capacidad_kg
        self.estado = estado
        self.fecha_ultimo_mantenimiento = fecha_ultimo_mantenimiento
        self.vehiculo_id = vehiculo_id
        self.ruta_id = ruta_id

    @staticmethod
    def obtener_todos():
        """Obtiene todos los cilindros de la base de datos"""
        conn = create_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT c.*, v.placa as vehiculo_placa, u.username as chofer_username
                FROM cilindros c 
                LEFT JOIN vehiculos v ON c.vehiculo_id = v.id
                LEFT JOIN users u ON v.chofer_id = u.id
            """
            cursor.execute(query)
            cilindros = cursor.fetchall()
            cursor.close()
            conn.close()
            return cilindros
        except Exception as e:
            print(f"Error al obtener cilindros: {e}")
            if conn.is_connected():
                conn.close()
            return []

    @staticmethod
    def crear_cilindro(codigo_rfid, capacidad_kg, estado, fecha_ultimo_mantenimiento, vehiculo_id):
        """Crea un nuevo cilindro en la base de datos"""
        conn = create_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO cilindros (codigo_rfid, capacidad_kg, estado, fecha_ultimo_mantenimiento, vehiculo_id)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (codigo_rfid, capacidad_kg, estado, fecha_ultimo_mantenimiento, vehiculo_id))
            conn.commit()
            cursor.close()
            conn.close()
            print(f">> Cilindro creado: RFID {codigo_rfid}, Capacidad {capacidad_kg}kg, Vehículo ID: {vehiculo_id}")
            return True
        except Exception as e:
            print(f"Error al crear cilindro: {e}")
            if conn.is_connected():
                conn.close()
            return False

    @staticmethod
    def obtener_vehiculos_disponibles():
        """Obtiene vehículos disponibles (no en mantenimiento)"""
        conn = create_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT v.*, u.username as chofer_username 
                FROM vehiculos v 
                LEFT JOIN users u ON v.chofer_id = u.id
                WHERE v.estado != 'mantenimiento'
            """
            cursor.execute(query)
            vehiculos = cursor.fetchall()
            cursor.close()
            conn.close()
            return vehiculos
        except Exception as e:
            print(f"Error al obtener vehículos disponibles: {e}")
            if conn.is_connected():
                conn.close()
            return []

    @staticmethod
    def actualizar_cilindro(cilindro_id, codigo_rfid=None, capacidad_kg=None, estado=None, fecha_ultimo_mantenimiento=None, vehiculo_id=None):
        """Actualiza un cilindro existente"""
        conn = create_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            updates = []
            params = []
            
            if codigo_rfid is not None:
                updates.append("codigo_rfid = %s")
                params.append(codigo_rfid)
            if capacidad_kg is not None:
                updates.append("capacidad_kg = %s")
                params.append(capacidad_kg)
            if estado is not None:
                updates.append("estado = %s")
                params.append(estado)
            if fecha_ultimo_mantenimiento is not None:
                updates.append("fecha_ultimo_mantenimiento = %s")
                params.append(fecha_ultimo_mantenimiento)
            if vehiculo_id is not None:
                updates.append("vehiculo_id = %s")
                params.append(vehiculo_id)
            
            if not updates:
                return False
                
            query = f"UPDATE cilindros SET {', '.join(updates)} WHERE id = %s"
            params.append(cilindro_id)
            
            cursor.execute(query, params)
            conn.commit()
            cursor.close()
            conn.close()
            print(f">> Cilindro actualizado: ID {cilindro_id}")
            return True
        except Exception as e:
            print(f"Error al actualizar cilindro: {e}")
            if conn.is_connected():
                conn.close()
            return False

    @staticmethod
    def eliminar_cilindro(cilindro_id):
        """Elimina un cilindro de la base de datos"""
        conn = create_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            query = "DELETE FROM cilindros WHERE id = %s"
            cursor.execute(query, (cilindro_id,))
            conn.commit()
            cursor.close()
            conn.close()
            print(f">> Cilindro eliminado: ID {cilindro_id}")
            return True
        except Exception as e:
            print(f"Error al eliminar cilindro: {e}")
            if conn.is_connected():
                conn.close()
            return False