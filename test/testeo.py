import unittest
import sqlite3
from datetime import datetime

def ejecutar_consulta(sql_query, params, fetchall=False):
    # Aquí se hace la conexión a la base de datos
    conexion = sqlite3.connect('sistema_medico.db')
    cursor = conexion.cursor()

    try:
        cursor.execute(sql_query, params)
        resultado = cursor.fetchall() if fetchall else None
        conexion.commit()  # Guardar los cambios en la base de datos
        conexion.close()
        return resultado
    except Exception as e:
        conexion.close()
        raise e

class Testeo(unittest.TestCase):
  #linea 21 a 24 para el metodo submit
    usuario = "slopez"
    contrasenia = 6789
    query_submit = "SELECT Nombre, Apellido FROM Empleado WHERE Usuario = ? AND Contrasenia = ? LIMIT 1"

  #linea 27 a 30 para el metodo agendar_cita
    fecha_hora = datetime(2023, 12, 29, 10, 45)
    estado = "postergada"
    id_paciente = 2
    id_medico = 3
    nombre_usuario = "masad"

  #linea 34 y 35 para editar cita
    id_cita = 30
    nuevo_estado="cancelada"
  
  
    query_agendar_cita = "INSERT INTO CitaMedica (FechaHora, Estado, Paciente, Medico, NombreUsuario) VALUES (?, ?, ?, ?, ?)"
  
    query_obtener_cita = "SELECT FechaHora, Estado, Paciente, Medico, NombreUsuario FROM CitaMedica WHERE FechaHora = ? AND Estado = ? AND Paciente = ? AND Medico = ? AND NombreUsuario = ? LIMIT 1"

    def test_submit_usuario_contra_correcto(self):
        resultado = ejecutar_consulta(self.query_submit, (self.usuario, self.contrasenia), fetchall=True)
        resultadoEsperado = [('sebastian', 'lopez')]
        self.assertEqual(resultado, resultadoEsperado, "Pasó la prueba")

    def test_agendar_cita(self):
        # Realizar la inserción antes de la prueba
        ejecutar_consulta(self.query_agendar_cita, (self.fecha_hora, self.estado, self.id_paciente, self.id_medico, self.nombre_usuario))

        # Realizar la consulta después de la inserción
        resultado = ejecutar_consulta(self.query_obtener_cita, (self.fecha_hora, self.estado, self.id_paciente, self.id_medico, self.nombre_usuario), fetchall=True)

        # Verificar que se obtenga algún resultado
        self.assertIsNotNone(resultado, "No se obtuvieron resultados")

        # Convertir la cadena de fecha en objeto datetime durante la comparación
        resultadoEsperado = [(self.fecha_hora.strftime('%Y-%m-%d %H:%M:%S'), self.estado, self.id_paciente, self.id_medico, self.nombre_usuario)]
        self.assertEqual(resultado, resultadoEsperado, "Pasó la prueba")

    def test_consultar_cita(self): #para facilitar el testeo, se agrego una clausula where para limitar el resultado esperado
      usuario = "slopez"
      resultado = ejecutar_consulta("""
          SELECT CitaMedica.ID, CitaMedica.FechaHora, CitaMedica.Estado, CitaMedica.Paciente,
                 Paciente.Nombre AS NombrePaciente, Paciente.Apellido AS ApellidoPaciente,
                 CitaMedica.Medico, Medico.Nombre AS NombreMedico, Medico.Apellido AS ApellidoMedico,
                 CitaMedica.NombreUsuario
          FROM CitaMedica
          INNER JOIN Paciente ON CitaMedica.Paciente = Paciente.ID
          INNER JOIN Medico ON CitaMedica.Medico = Medico.ID
          WHERE CitaMedica.NombreUsuario = ?
      """, (usuario,), fetchall=True)

      #print("algo: ",resultado)
      #aca se puso lo colocado en el print comentado
      resultadoEsperado = [(11,'2023-11-17T13:16',
                           'confirmada',
                            9,
                             'Isabel',
                             'Díaz',
                             6,
                             'Dra. Ana',
                             'Fernández',
                             'slopez'),
                            (17,
                             '2024-01-31T18:34',
                             'postergada',
                             1,
                             'Ana',
                             'García',
                             5,
                             'Dr. Andrés',
                             'Martínez',
                             'slopez'),
                            (19,
                             '2024-01-29T18:34',
                             'suspendida',
                             9,
                             'Isabel',
                             'Díaz',
                             8,
                             'Dra. Isabel',
                             'Ramírez',
                             'slopez')]
      self.assertEqual(resultado, resultadoEsperado, "Pasó la prueba")  

    def test_editar_cita(self): 
      usuario = "masad"
      fecha_hora = datetime(2023, 1, 24, 19, 12)
      estado = "postergada"
      id_paciente = 2
      id_medico = 3
      id_consulta=21

# Actualizar la cita en la base de datos
      ejecutar_consulta("""
    UPDATE CitaMedica SET FechaHora = ?, Estado = ?, Paciente = ?, Medico = ?, NombreUsuario = ? WHERE ID = ?
""", (fecha_hora, estado, id_paciente, id_medico, usuario, id_consulta))

# Verificar que la actualización se haya realizado correctamente
      resultado_actualizado = ejecutar_consulta("""
    SELECT * FROM CitaMedica WHERE ID = ?
""", (id_consulta,), fetchall=True)
      #print("algo: ",resultado_actualizado)
      #aca se puso lo colocado en el print comentado
      resultadoEsperado = [(21, '2023-01-24 19:12:00', 'postergada', 2, 3, 'masad')]
      self.assertEqual(resultado_actualizado, resultadoEsperado, "Pasó la prueba")     

if __name__ == '__main__':
     unittest.main()