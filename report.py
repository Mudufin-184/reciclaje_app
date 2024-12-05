#report.py raiz
from db_connection import get_db_connection
from datetime import datetime, timedelta

def reporte_semanal():
    """Genera un reporte del reciclaje semanal por curso."""
    connection = get_db_connection()
    cursor = connection.cursor()
    hoy = datetime.now().date()
    inicio_semana = hoy - timedelta(days=hoy.weekday())  # Fecha de inicio de la semana actual

    cursor.execute("""
        SELECT c.nombre AS nombre_curso, COUNT(r.reciclo) AS total_reciclaje
        FROM reciclaje r
        JOIN cursos c ON r.curso_id = c.id
        WHERE r.fecha BETWEEN ? AND ? AND r.reciclo = 1
        GROUP BY r.curso_id
    """, (inicio_semana, hoy))
    
    reporte = cursor.fetchall()
    connection.close()
    return reporte
