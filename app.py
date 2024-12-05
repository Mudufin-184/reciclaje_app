from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import date, timedelta, datetime
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Configuración del correo
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'example@gmail.com'  # Cambia esto por tu correo
app.config['MAIL_PASSWORD'] = '1234'  # Cambia esto por tu contraseña
app.config['MAIL_DEFAULT_SENDER'] = 'example26@gmail.com'  # Cambia esto por tu correo

mail = Mail(app)
scheduler = BackgroundScheduler()

# Datos predefinidos
usuarios = [
    {"id_usuario": 1, "nombre": "Juan Pérez", "email": "juan@example.com", "password": generate_password_hash("1234"), "rol": "profesor"},
    {"id_usuario": 2, "nombre": "Ana Gómez", "email": "ana@example.com", "password": generate_password_hash("5678"), "rol": "profesor"},
]

cursos = [
    {"id_curso": 1001, "nombre_curso": "Curso 1001"},
    {"id_curso": 1002, "nombre_curso": "Curso 1002"},
    {"id_curso": 1003, "nombre_curso": "Curso 1003"},
    {"id_curso": 1101, "nombre_curso": "Curso 1101"},
    {"id_curso": 1102, "nombre_curso": "Curso 1102"},
    {"id_curso": 1103, "nombre_curso": "Curso 1103"},
]

reciclaje_registros = [
    {"id_reciclaje": 1, "id_curso": 1001, "fecha": date.today() - timedelta(days=1), "reciclo": True},
    {"id_reciclaje": 2, "id_curso": 1002, "fecha": date.today() - timedelta(days=2), "reciclo": False},
    {"id_reciclaje": 3, "id_curso": 1003, "fecha": date.today() - timedelta(days=3), "reciclo": True},
    {"id_reciclaje": 4, "id_curso": 1001, "fecha": date.today() - timedelta(days=4), "reciclo": False},
    {"id_reciclaje": 5, "id_curso": 1002, "fecha": date.today() - timedelta(days=5), "reciclo": True},
    {"id_reciclaje": 6, "id_curso": 1003, "fecha": date.today() - timedelta(days=6), "reciclo": True},
    {"id_reciclaje": 7, "id_curso": 1101, "fecha": date.today() - timedelta(days=7), "reciclo": False},
    {"id_reciclaje": 8, "id_curso": 1102, "fecha": date.today() - timedelta(days=8), "reciclo": True},
    {"id_reciclaje": 9, "id_curso": 1103, "fecha": date.today() - timedelta(days=9), "reciclo": False},
    {"id_reciclaje": 10, "id_curso": 1001, "fecha": date.today() - timedelta(days=10), "reciclo": True},
    {"id_reciclaje": 11, "id_curso": 1103, "fecha": date.today() - timedelta(days=5), "reciclo": True},
    {"id_reciclaje": 12, "id_curso": 1001, "fecha": date.today() - timedelta(days=3), "reciclo": False},
    {"id_reciclaje": 13, "id_curso": 1102, "fecha": date.today() - timedelta(days=3), "reciclo": True},
    {"id_reciclaje": 14, "id_curso": 1103, "fecha": date.today() - timedelta(days=2), "reciclo": False},
    {"id_reciclaje": 15, "id_curso": 1101, "fecha": date.today() - timedelta(days=1), "reciclo": True},
]


# Función para verificar sesión activa
def verificar_sesion():
    return session.get('user_id') is not None


# Rutas
@app.route('/home')
def home():
    if verificar_sesion():
        user_id = session['user_id']
        usuario = next((user for user in usuarios if user["id_usuario"] == user_id), None)
        return render_template('home.html', usuario=usuario, cursos=cursos)
    flash("Por favor, inicia sesión para continuar", "error")
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = next((user for user in usuarios if user["email"] == email), None)
        if user and check_password_hash(user["password"], password):
            session['user_id'] = user["id_usuario"]
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('home'))
        else:
            flash('Email o contraseña incorrectos', 'error')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        nuevo_usuario = {"id_usuario": len(usuarios) + 1, "nombre": name, "email": email, "password": hashed_password, "rol": "profesor"}
        usuarios.append(nuevo_usuario)
        flash('Usuario registrado con éxito', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/report')
def report():
    fecha_hoy = date.today()
    fecha_inicio = fecha_hoy - timedelta(days=5)

    reporte = [
        {
            "nombre_curso": curso["nombre_curso"],
            "total_reciclaje": sum(
                1 for r in reciclaje_registros 
                if r["id_curso"] == curso["id_curso"] and r["reciclo"] and r["fecha"] >= fecha_inicio
            )
        }
        for curso in cursos
    ]
    
    return render_template('report.html', reporte=reporte)

@app.route('/reminder')
def reminder():
    puntos_reciclaje = [
        {"ubicacion": "Parque Central", "descripcion": "Contenedor de plástico"},
        {"ubicacion": "Biblioteca", "descripcion": "Contenedor de papel"},
    ]
    return render_template('reminder.html', puntos=puntos_reciclaje, mensaje="Puntos de Reciclaje Disponibles")

@app.route('/recycling', methods=['POST'])
def recycling():
    curso_id = int(request.form['curso'])
    reciclo = request.form['reciclo'] == 'si'
    nuevo_registro = {"id_reciclaje": len(reciclaje_registros) + 1, "id_curso": curso_id, "fecha": date.today(), "reciclo": reciclo}
    reciclaje_registros.append(nuevo_registro)
    flash('Registro de reciclaje exitoso', 'success')
    return redirect(url_for('home'))

def send_reminder(email, message):
    msg = Message("Recordatorio de Reciclaje", recipients=[email])
    msg.body = message
    mail.send(msg)

def send_weekly_report():
    fecha_hoy = date.today()
    inicio_semana = fecha_hoy - timedelta(days=fecha_hoy.weekday())
    message = "Reporte Semanal de Reciclaje:\n\n"
    for curso in cursos:
        total_reciclaje = sum(1 for r in reciclaje_registros if r["id_curso"] == curso["id_curso"] and r["reciclo"] and r["fecha"] >= inicio_semana)
        message += f"Curso: {curso['nombre_curso']}, Total Reciclaje: {total_reciclaje}\n"
    for user in usuarios:
        send_reminder(user["email"], message)

@app.route('/historial_reciclaje')
def historial_reciclaje():
    total_reciclajes = []
    for curso in cursos:
        total_reciclaje = sum(1 for r in reciclaje_registros if r["id_curso"] == curso["id_curso"] and r["reciclo"])
        total_no_reciclaje = sum(1 for r in reciclaje_registros if r["id_curso"] == curso["id_curso"] and not r["reciclo"])
        total_reciclajes.append({
            "nombre_curso": curso["nombre_curso"],
            "total_reciclaje": total_reciclaje,
            "total_no_reciclaje": total_no_reciclaje
        })

    historial = [{
        "nombre_curso": next((c["nombre_curso"] for c in cursos if c["id_curso"] == registro["id_curso"]), ""),
        "fecha": registro["fecha"],
        "reciclo": registro["reciclo"]
    } for registro in reciclaje_registros]

    return render_template('historial_reciclaje.html', total_reciclajes=total_reciclajes, historial=historial)

@app.route('/')
def index():
    return redirect(url_for('login'))  # Redirige a la página de login al acceder a la raíz

if __name__ == "__main__":
    # Programar el envío del informe semanal cada lunes a las 8:00 AM
    scheduler.add_job(send_weekly_report, 'cron', day_of_week='mon', hour=8)
    scheduler.start()
    app.run(debug=True)
