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
    NombreUsuario TEXT,
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

# Inserts para la tabla Medico
medico_data = [
    ('Dr. Juan', 'Pérez', 'Cardiología', 15, 'Universidad Central', 2005),
    ('Dra. María', 'Gómez', 'Dermatología', 12, 'Universidad Nacional', 2010),
    ('Dr. Carlos', 'Rodríguez', 'Pediatría', 20, 'Universidad del Este', 2002),
    ('Dra. Laura', 'López', 'Oftalmología', 18, 'Universidad del Oeste', 2007),
    ('Dr. Andrés', 'Martínez', 'Cirugía General', 22, 'Universidad Sur', 2000),
    ('Dra. Ana', 'Fernández', 'Ginecología', 17, 'Universidad Norte', 2009),
    ('Dr. Pablo', 'Herrera', 'Neurología', 14, 'Universidad Este', 2012),
    ('Dra. Isabel', 'Ramírez', 'Psiquiatría', 19, 'Universidad Oeste', 2006),
    ('Dr. Martín', 'Díaz', 'Ortopedia', 21, 'Universidad Sur', 2003),
    ('Dra. Carla', 'Gutiérrez', 'Endocrinología', 16, 'Universidad Centro', 2008)
]

for medico_entry in medico_data:
    cursor.execute('''INSERT INTO Medico (Nombre, Apellido, Especialidad, AniosExperiencia, LugarGraduacion, AnioGraduacion)
                      VALUES (?, ?, ?, ?, ?, ?)''', medico_entry)

# Inserts para la tabla Paciente
paciente_data = [
    ('Ana', 'García', '12345678', 'contrasenia1', 'ana@gmail.com', '123-456-7890', 'Calle A #123'),
    ('Pedro', 'Sánchez', '98765432', 'contrasenia2', 'pedro@gmail.com', '987-654-3210', 'Calle B #456'),
    ('Luisa', 'Hernández', '87654321', 'contrasenia3', 'luisa@gmail.com', '567-890-1234', 'Calle C #789'),
    ('Roberto', 'González', '23456789', 'contrasenia4', 'roberto@gmail.com', '234-567-8901', 'Calle D #012'),
    ('Sofía', 'Díaz', '34567890', 'contrasenia5', 'sofia@gmail.com', '345-678-9012', 'Calle E #345'),
    ('Carlos', 'Martínez', '56789012', 'contrasenia6', 'carlos@gmail.com', '456-789-0123', 'Calle F #678'),
    ('Laura', 'Ramírez', '67890123', 'contrasenia7', 'laura@gmail.com', '567-890-1234', 'Calle G #901'),
    ('Pablo', 'Gutiérrez', '78901234', 'contrasenia8', 'pablo@gmail.com', '678-901-2345', 'Calle H #234'),
    ('Isabel', 'Díaz', '89012345', 'contrasenia9', 'isabel@gmail.com', '789-012-3456', 'Calle I #567'),
    ('Martín', 'Fernández', '90123456', 'contrasenia10', 'martin@gmail.com', '890-123-4567', 'Calle J #890')
]

for paciente_entry in paciente_data:
    cursor.execute('''INSERT INTO Paciente (Nombre, Apellido, DNI, Contrasenia, CorreoElectronico, Telefono, Direccion)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''', paciente_entry)

# Consultar y mostrar los datos de la tabla Medico
cursor.execute("SELECT * FROM Medico")
medico_data = cursor.fetchall()
print("Datos de la tabla Medico:")
for row in medico_data:
    print(row)

# Consultar y mostrar los datos de la tabla Paciente
cursor.execute("SELECT * FROM Paciente")
paciente_data = cursor.fetchall()
print("\nDatos de la tabla Paciente:")
for row in paciente_data:
    print(row)

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