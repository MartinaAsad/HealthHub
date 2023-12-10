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




@app.route('/agendar_cita', methods=['GET', 'POST'])
def agendar_cita():
    if request.method == 'POST':
        # Obtener datos del formulario
        fecha_hora = request.form['fecha_hora']
        estado = request.form['estado']
        paciente = request.form['paciente']
        medico = request.form['medico']
        nombre_usuario = request.form['nombreUusuario']

        # Realizar la inserción en la base de datos
        conn = sqlite3.connect('sistema_medico.db')
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO CitaMedica (FechaHora, Estado, Paciente, Medico, NombreUsuario) 
                          VALUES (?, ?, ?, ?, ?)''', (fecha_hora, estado, paciente, medico, nombre_usuario))

        conn.commit()

      # Comprobar si los datos se insertaron correctamente
        cursor.execute("SELECT * FROM CitaMedica WHERE FechaHora = ? AND Paciente = ?", (fecha_hora, paciente))
        resultado = cursor.fetchone()

        conn.close()

        # Redirigir a la página de confirmación de agenda sin pasar 'mensaje_bienvenida' como parámetro
        return redirect(url_for('confAgenda'))
    else:
        # Mostrar el formulario de agendar cita
        return render_template('agendar_cita.html')


@app.route('/confAgenda')
def confAgenda():
    # Lógica para la página de confirmación de la agenda
    return render_template('confAgenda.html')



@app.route('/consultar_citas', methods=['GET'])
def consultar_citas():
    # Realizar la consulta a la base de datos para obtener todas las citas con información de pacientes y médicos
    conn = sqlite3.connect('sistema_medico.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT CitaMedica.ID, CitaMedica.FechaHora, CitaMedica.Estado,
                           CitaMedica.Paciente, Paciente.Nombre AS NombrePaciente, Paciente.Apellido AS ApellidoPaciente,
                           CitaMedica.Medico, Medico.Nombre AS NombreMedico, Medico.Apellido AS ApellidoMedico,
                           CitaMedica.NombreUsuario
                    FROM CitaMedica
                    INNER JOIN Paciente ON CitaMedica.Paciente = Paciente.ID
                    INNER JOIN Medico ON CitaMedica.Medico = Medico.ID''')
    citas = cursor.fetchall()
    conn.close()

    # Imprimir citas para depurar
    print(citas)

    # Renderizar la plantilla y pasar los datos de las citas
    return render_template('consultar_citas.html', citas=citas)



# Editar_cita
@app.route('/editar_cita/<int:cita_id>', methods=['GET', 'POST'])
def editar_cita(cita_id):
    if request.method == 'POST':
        # Lógica de edición
        nueva_fecha_hora = request.form.get('fecha_hora')
        nuevo_estado = request.form.get('estado')
        nuevo_paciente = request.form.get('paciente')
        nuevo_medico = request.form.get('medico')
        nuevo_nombre_usuario = request.form.get('nombreUusuario')

        # Conecta a la base de datos y realiza la actualización
        db = get_db()
        cursor = db.cursor()

        cursor.execute("UPDATE CitaMedica SET FechaHora = ?, Estado = ?, Paciente = ?, Medico = ?, NombreUsuario = ? WHERE ID = ?", 
                       (nueva_fecha_hora, nuevo_estado, nuevo_paciente, nuevo_medico, nuevo_nombre_usuario, cita_id))

        db.commit()
        db.close()

        return redirect(url_for('consultar_citas'))

    # Lógica para cargar los datos de la cita existente
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM CitaMedica WHERE ID = ?", (cita_id,))
    cita_existente = cursor.fetchone()

    db.close()

    if cita_existente:
        # Pasa los datos de la cita existente al renderizar el formulario de edición
        return render_template('editar_cita.html', cita_existente=cita_existente)
    else:
        return render_template('error.html', mensaje="La cita no existe.")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


