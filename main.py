
from flask import Flask, render_template, request, g, redirect, url_for
import sqlite3

app = Flask(__name__)

# Establecer la conexión con la base de datos
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect("sistema_medico.db")
    return db

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    dni = request.form.get('dni')
    usuario = request.form.get('usuario')
    contrasenia = request.form.get('contrasenia')

    # Realizar operaciones de base de datos para verificar la autenticación
    db = get_db()
    cursor = db.cursor()

    # Suponiendo que la tabla Empleado tiene campos 'Usuario' y 'Contrasenia'
    cursor.execute("SELECT Nombre, Apellido FROM Empleado WHERE Usuario = ? AND Contrasenia = ?", (usuario, contrasenia))
    resultado = cursor.fetchone()

    # Cerrar el cursor
    cursor.close()

    # Cierro la conexión con la base de datos
    db.close()

    if resultado:
        nombre, apellido = resultado
        return render_template('logueo.html', dni=dni, usuario=usuario, nombre=nombre, apellido=apellido)
    else:
      return render_template('errorLogueo.html')  # Redirecciona a pagina de error de logueo

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

