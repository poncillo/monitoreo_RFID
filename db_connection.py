import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

def create_connection():
    """Establece la conexión con la base de datos MySQL"""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            port=os.getenv('DB_PORT')
        )
        
        if connection.is_connected():
            print("Conexión a MySQL exitosa")
            return connection

    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
        return None

if __name__ == "__main__":
    conn = create_connection()
    if conn:
        conn.close()
        print("Conexión cerrada")