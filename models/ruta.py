# models/ruta.py
from db_connection import create_connection

class Ruta:
    def __init__(self, id, chofer_id, vehiculo_id, origen, destino, distancia_km, tiempo_estimado_min, estado):
        self.id = id
        self.chofer_id = chofer_id
        self.vehiculo_id = vehiculo_id
        self.origen = origen
        self.destino = destino
        self.distancia_km = distancia_km
        self.tiempo_estimado_min = tiempo_estimado_min
        self.estado = estado

    @staticmethod
    def obtener_todas():
        """Obtiene todas las rutas de la base de datos"""
        conn = create_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT r.*, u.username as chofer_username, v.placa as vehiculo_placa
                FROM rutas r 
                LEFT JOIN users u ON r.chofer_id = u.id
                LEFT JOIN vehiculos v ON r.vehiculo_id = v.id
            """
            cursor.execute(query)
            rutas = cursor.fetchall()
            cursor.close()
            conn.close()
            return rutas
        except Exception as e:
            print(f"Error al obtener rutas: {e}")
            if conn.is_connected():
                conn.close()
            return []

    @staticmethod
    def crear_ruta(chofer_id, vehiculo_id, origen, destino, distancia_km, tiempo_estimado_min, estado='programada'):
        """Crea una nueva ruta en la base de datos"""
        conn = create_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO rutas (chofer_id, vehiculo_id, origen, destino, distancia_km, tiempo_estimado_min, estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (chofer_id, vehiculo_id, origen, destino, distancia_km, tiempo_estimado_min, estado))
            conn.commit()
            cursor.close()
            conn.close()
            print(f">> Ruta creada: {origen} -> {destino}, Chofer ID: {chofer_id}, Vehículo ID: {vehiculo_id}")
            return True
        except Exception as e:
            print(f"Error al crear ruta: {e}")
            if conn.is_connected():
                conn.close()
            return False

    @staticmethod
    def obtener_choferes_con_vehiculos():
        """Obtiene choferes que tienen vehículo asignado"""
        conn = create_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT u.id, u.username, u.licencia, v.id as vehiculo_id, v.placa, v.modelo
                FROM users u 
                JOIN vehiculos v ON u.id = v.chofer_id
                WHERE u.rol = 'chofer' AND u.estado = 'activo'
            """
            cursor.execute(query)
            choferes = cursor.fetchall()
            cursor.close()
            conn.close()
            print(f">> Choferes con vehículos obtenidos: {len(choferes)}")
            return choferes
        except Exception as e:
            print(f"Error al obtener choferes con vehículos: {e}")
            if conn.is_connected():
                conn.close()
            return []

    @staticmethod
    def eliminar_ruta(ruta_id):
        """Elimina una ruta de la base de datos"""
        conn = create_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            query = "DELETE FROM rutas WHERE id = %s"
            cursor.execute(query, (ruta_id,))
            conn.commit()
            cursor.close()
            conn.close()
            print(f">> Ruta eliminada: ID {ruta_id}")
            return True
        except Exception as e:
            print(f"Error al eliminar ruta: {e}")
            if conn.is_connected():
                conn.close()
            return False