import mysql.connector
from mysql.connector import Error

def get_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            database='reciclaje_escuelas',
            user='root',
            password=''
        )
        if connection.is_connected():
            print("Conexión a MySQL exitosa.")
    except Error as e:
        print("Error al conectarse a MySQL", e)
    return connection
