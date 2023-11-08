import unittest
import sqlite3

def ejecutar_consulta(sql_query, params):
    # conexion a la bbdd
    conexion = sqlite3.connect('sistema_medico.db')
    cursor = conexion.cursor()

    try:
        cursor.execute(sql_query, params)
        resultado = cursor.fetchall()
        conexion.close()
        return resultado
    except Exception as e:
        conexion.close()
        raise e

class testeo(unittest.TestCase):
    usuario = "slopez"
    contrasenia = 6789
    query_submit = "SELECT Nombre, Apellido FROM Empleado WHERE Usuario = ? AND Contrasenia = ?"

    def test_submit_usuario_contra_correcto(self):
        resultado = ejecutar_consulta(self.query_submit, (self.usuario, self.contrasenia))

        resultadoEsperado = [('sebastian', 'lopez')]  # poner resultado esperado segun la bbdd
        self.assertEqual(resultado, resultadoEsperado, "Pasó la prueba")

if __name__ == '__main__':
    unittest.main()