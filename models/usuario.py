# models/usuario.py
from db_connection import create_connection

class Usuario:
    def __init__(self, id, username, rol, email=None):
        self.id = id
        self.username = username
        self.rol = rol
        self.email = email

    @staticmethod
    def generar_siguiente_codigo_usuario():
        """
        Genera el siguiente código de usuario basado en el último ID en la base de datos.
        """
        conn = create_connection()
        if not conn:
            return "USER001"  # Fallback si no hay conexión

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(id) FROM users")
            result = cursor.fetchone()
            next_id = 1
            if result and result[0] is not None:
                next_id = result[0] + 1
            
            # Formatear como USER001, USER002, etc.
            codigo = f"USER{next_id:03d}"
            cursor.close()
            conn.close()
            return codigo
        except Exception as e:
            print(f"Error al generar código de usuario: {e}")
            if conn.is_connected():
                conn.close()
            return "USER001"

    @staticmethod
    def crear_usuario(username, password, rol, telefono, licencia=None):
        """
        Crea un nuevo usuario en la base de datos.
        El estado por defecto es 'activo' según tu tabla SQL.
        """
        conn = create_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            
            # Solo incluir licencia si es chofer, para otros roles será NULL
            if rol == 'chofer':
                query = """INSERT INTO users (username, password_hash, rol, telefono, licencia, estado) 
                          VALUES (%s, %s, %s, %s, %s, 'activo')"""
                cursor.execute(query, (username, password, rol, telefono, licencia))
            else:
                query = """INSERT INTO users (username, password_hash, rol, telefono, estado) 
                          VALUES (%s, %s, %s, %s, 'activo')"""
                cursor.execute(query, (username, password, rol, telefono))
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            if conn.is_connected():
                conn.close()
            return False

    @staticmethod
    def autenticar(username, password):
        """
        Verifica las credenciales en la base de datos.
        Retorna un objeto Usuario si es correcto, o None si falla.
        """
        conn = create_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT * FROM users WHERE username = %s AND password_hash = %s"
            cursor.execute(query, (username, password))
            
            user_data = cursor.fetchone()
            
            cursor.close()
            conn.close()

            if user_data:
                return Usuario(
                    id=user_data['id'],
                    username=user_data['username'],
                    rol=user_data['rol']
                )
            else:
                return None

        except Exception as e:
            print(f"Error en autenticación: {e}")
            if conn.is_connected():
                conn.close()
            return None