#OPERACIONES CRUD DE LA BD...
# models/database.py
from db_connection import create_connection

class Database:
    @staticmethod
    def obtener_usuarios():
        """Obtiene todos los usuarios excepto el admin actual"""
        conn = create_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT id, username, rol, licencia, telefono, estado FROM users WHERE rol != 'admin'"
            cursor.execute(query)
            usuarios = cursor.fetchall()
            cursor.close()
            conn.close()
            return usuarios
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            if conn.is_connected():
                conn.close()
            return []

    @staticmethod
    def actualizar_usuario(user_id, campo, valor):
        """Actualiza un campo específico de un usuario"""
        conn = create_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            query = f"UPDATE users SET {campo} = %s WHERE id = %s"
            cursor.execute(query, (valor, user_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al actualizar usuario: {e}")
            if conn.is_connected():
                conn.close()
            return False

    @staticmethod
    def eliminar_usuario(user_id):
        """Elimina un usuario de la base de datos"""
        conn = create_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            query = "DELETE FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error al eliminar usuario: {e}")
            if conn.is_connected():
                conn.close()
            return False