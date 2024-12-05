#reminder.py raiz 
from time import sleep
from datetime import datetime

def start_reminders():
    """Inicia los recordatorios diarios de reciclaje."""
    while True:
        hora_actual = datetime.now().hour
        if hora_actual == 8:  # Suponiendo que el recordatorio es a las 8 AM
            print("¡Es hora de reciclar! Recuerda motivar a tu grupo a colaborar.")
            # Aquí se podría integrar un sistema de notificaciones
        sleep(3600)  # Pausa de 1 hora
