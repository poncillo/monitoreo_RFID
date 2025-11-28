# models/usuario.py
from db_connection import create_connection

class Usuario:
    def __init__(self, id, username, rol, email=None):
        self.id = id
        self.username = username
        self.rol = rol
        self.email = email

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
            cursor = conn.cursor(dictionary=True) # dictionary=True nos deja acceder por nombre de columna
            
            # NOTA: En un entorno real, la contraseña debería estar encriptada (hashing).
            # Como es un proyecto escolar inicial, comparamos texto plano por ahora.
            query = "SELECT * FROM users WHERE username = %s AND password_hash = %s"
            cursor.execute(query, (username, password))
            
            user_data = cursor.fetchone()
            
            cursor.close()
            conn.close()

            if user_data:
                # Si encontramos al usuario, creamos y retornamos el objeto
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