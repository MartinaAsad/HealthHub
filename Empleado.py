class Empleado:
    def __init__(self, ID, Nombre, Apellido, DNI, AreaTrabajo, Usuario, Contrasenia):
        self.ID = ID
        self.Nombre = Nombre
        self.Apellido = Apellido
        self.DNI = DNI
        self.AreaTrabajo = AreaTrabajo  # Puede ser un objeto de la clase AreaTrabajo
        self.Usuario = Usuario
        self.Contrasenia = Contrasenia

    def modificar_cita_medica(self, cita_medica, nueva_fecha_hora, nuevo_estado):
        # Modificar la fecha y el estado de la cita médica
        cita_medica.FechaHora = nueva_fecha_hora
        cita_medica.Estado = nuevo_estado

    def visualizar_cita_medica(self, cita_medica):
        # Mostrar los detalles de la cita médica
        print("ID:", cita_medica.ID)
        print("Fecha y Hora:", cita_medica.FechaHora)
        print("Estado:", cita_medica.Estado)
        print("Paciente:", cita_medica.Paciente.Nombre, cita_medica.Paciente.Apellido)
        print("Médico:", cita_medica.Medico.Nombre, cita_medica.Medico.Apellido)

    def modificar_medico_cita(self, cita_medica, nuevo_medico):
        # Modificar al médico asociado a una cita médica
        cita_medica.Medico = nuevo_medico