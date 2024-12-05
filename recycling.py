#recycling.py raiz
from db_connection import get_db_connection
from datetime import datetime

def registrar_reciclaje(id_curso, reciclo):
    """Registra si el curso recicló o no en la base de datos."""
    connection = get_db_connection()
    cursor = connection.cursor()
    fecha = datetime.now().date()  # Fecha de hoy
    cursor.execute("""
        INSERT INTO reciclaje (curso_id, fecha, reciclo)
        VALUES (?, ?, ?)
    """, (id_curso, fecha, reciclo))
    connection.commit()
    connection.close()
