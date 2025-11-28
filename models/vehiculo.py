# models/vehiculo.py
from db_connection import create_connection

class Vehiculo:
    def __init__(self, id, placa, modelo, capacidad_cilindros, estado, chofer_id=None):
        self.id = id
        self.placa = placa
        self.modelo = modelo
        self.capacidad_cilindros = capacidad_cilindros
        self.estado = estado
        self.chofer_id = chofer_id

    @staticmethod
    def obtener_todos():
        """Obtiene todos los vehículos de la base de datos"""
        conn = create_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT v.*, u.username as chofer_username 
                FROM vehiculos v 
                LEFT JOIN users u ON v.chofer_id = u.id
            """
            cursor.execute(query)
            vehiculos = cursor.fetchall()
            cursor.close()
            conn.close()
            return vehiculos
        except Exception as e:
            print(f"Error al obtener vehículos: {e}")
            if conn.is_connected():
                conn.close()
            return []

    @staticmethod
    def crear_vehiculo(placa, modelo, capacidad_cilindros, estado='disponible', chofer_id=None):
        """Crea un nuevo vehículo en la base de datos"""
        conn = create_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO vehiculos (placa, modelo, capacidad_cilindros, estado, chofer_id)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (placa, modelo, capacidad_cilindros, estado, chofer_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al crear vehículo: {e}")
            if conn.is_connected():
                conn.close()
            return False

    @staticmethod
    def obtener_choferes_disponibles():
        """Obtiene choferes que no tienen vehículo asignado"""
        conn = create_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT u.id, u.username, u.licencia 
                FROM users u 
                WHERE u.rol = 'chofer' 
                AND u.estado = 'activo'
                AND u.id NOT IN (SELECT chofer_id FROM vehiculos WHERE chofer_id IS NOT NULL)
            """
            cursor.execute(query)
            choferes = cursor.fetchall()
            cursor.close()
            conn.close()
            return choferes
        except Exception as e:
            print(f"Error al obtener choferes disponibles: {e}")
            if conn.is_connected():
                conn.close()
            return []

    @staticmethod
    def actualizar_vehiculo(vehiculo_id, placa=None, modelo=None, capacidad_cilindros=None, estado=None, chofer_id=None):
        """Actualiza un vehículo existente"""
        conn = create_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            updates = []
            params = []
            
            if placa is not None:
                updates.append("placa = %s")
                params.append(placa)
            if modelo is not None:
                updates.append("modelo = %s")
                params.append(modelo)
            if capacidad_cilindros is not None:
                updates.append("capacidad_cilindros = %s")
                params.append(capacidad_cilindros)
            if estado is not None:
                updates.append("estado = %s")
                params.append(estado)
            if chofer_id is not None:
                updates.append("chofer_id = %s")
                params.append(chofer_id)
            
            if not updates:
                return False
                
            query = f"UPDATE vehiculos SET {', '.join(updates)} WHERE id = %s"
            params.append(vehiculo_id)
            
            cursor.execute(query, params)
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al actualizar vehículo: {e}")
            if conn.is_connected():
                conn.close()
            return False

    @staticmethod
    def eliminar_vehiculo(vehiculo_id):
        """Elimina un vehículo de la base de datos"""
        conn = create_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            query = "DELETE FROM vehiculos WHERE id = %s"
            cursor.execute(query, (vehiculo_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al eliminar vehículo: {e}")
            if conn.is_connected():
                conn.close()
            return False