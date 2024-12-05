#auth.py raiz
from db_connection import get_db_connection

def login(email, password):
    """Verifica las credenciales del usuario en la base de datos."""
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ? AND password = ?", (email, password))
    usuario = cursor.fetchone()
    connection.close()
    return usuario  # Devuelve el usuario si existe o None si no
