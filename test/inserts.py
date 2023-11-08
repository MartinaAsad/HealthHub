from flask import Flask, render_template, request, g
import sqlite3

# Conectar a la base de datos (o crearla si no existe)
conn = sqlite3.connect("sistema_medico.db")

# Crear un cursor para interactuar con la base de datos
cursor = conn.cursor()

# Definir las tablas en la base de datos
cursor.execute('''CREATE TABLE IF NOT EXISTS AreaTrabajo (
    ID INTEGER PRIMARY KEY,
    NombreArea TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS CitaMedica (
    ID INTEGER PRIMARY KEY,
    FechaHora TEXT,
    Estado TEXT,
    Paciente INTEGER,
    Medico INTEGER,
    FOREIGN KEY (Paciente) REFERENCES Paciente(ID),
    FOREIGN KEY (Medico) REFERENCES Medico(ID)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Laboratorio (
    ID INTEGER PRIMARY KEY,
    NombreLaboratorio TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Medico (
    ID INTEGER PRIMARY KEY,
    Nombre TEXT,
    Apellido TEXT,
    Especialidad TEXT,
    AniosExperiencia INTEGER,
    LugarGraduacion TEXT,
    AnioGraduacion INTEGER
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Paciente (
    ID INTEGER PRIMARY KEY,
    Nombre TEXT,
    Apellido TEXT,
    DNI TEXT,
    Contrasenia TEXT,
    CorreoElectronico TEXT,
    Telefono TEXT,
    Direccion TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Reclamo (
    NroReclamo INTEGER PRIMARY KEY,
    Descripcion TEXT,
    FechaReclamo TEXT,
    Paciente INTEGER,
    FOREIGN KEY (Paciente) REFERENCES Paciente(ID)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS RegistroHorasTrabajadas (
    ID INTEGER PRIMARY KEY,
    Fecha TEXT,
    HorasTrabajadas INTEGER,
    Medico INTEGER,
    FOREIGN KEY (Medico) REFERENCES Medico(ID)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS ResultadoLaboratorio (
    ID INTEGER PRIMARY KEY,
    FechaResultado TEXT,
    Resultado TEXT,
    Laboratorio INTEGER,
    Paciente INTEGER,
    FOREIGN KEY (Laboratorio) REFERENCES Laboratorio(ID),
    FOREIGN KEY (Paciente) REFERENCES Paciente(ID)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Empleado (
    ID INTEGER PRIMARY KEY,
    Nombre TEXT,
    Apellido TEXT,
    DNI TEXT,
    AreaTrabajo INTEGER,
    Usuario TEXT,
    Contrasenia TEXT,
    FOREIGN KEY (AreaTrabajo) REFERENCES AreaTrabajo(ID)
)''')

# Insertar el primer registro de empleado
cursor.execute('''INSERT INTO Empleado (Nombre, Apellido, DNI, AreaTrabajo, Usuario, Contrasenia)
                  VALUES (?, ?, ?, ?, ?, ?)''', ('martina', 'asad', '654321', 1, 'masad', '12345'))

# Insertar el segundo registro de empleado
cursor.execute('''INSERT INTO Empleado (Nombre, Apellido, DNI, AreaTrabajo, Usuario, Contrasenia)
                  VALUES (?, ?, ?, ?, ?, ?)''', ('sebastian', 'lopez', '987654', 2, 'slopez', '6789'))


# Realizar una consulta para seleccionar solo el nombre y el DNI de la tabla Empleado
cursor.execute('SELECT Nombre, DNI FROM Empleado')

# Obtener todos los registros seleccionados
empleados = cursor.fetchall()

# Imprimir los registros
for empleado in empleados:
    print("Nombre:", empleado[0])
    print("DNI:", empleado[1])
    print("-------------")

# Guardar los cambios en la base de datos
conn.commit()

# Cerrar la conexión con la base de datos
conn.close()