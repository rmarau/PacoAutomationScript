class Sumario:
    def __init__(self, datetime, hora, aula, status, sumario, bibliografia, sala, presencas_mec):
        self.datetime = datetime
        self.hora = hora
        self.aula = aula
        self.status = status
        self.sumario = sumario
        self.bibliografia = bibliografia
        self.sala = sala
        self.presencas_mec = presencas_mec

    @property
    def date(self):
        return self.datetime.strftime("%d-%m-%Y") if self.datetime is not None else None

    def __repr__(self):
        return str((self.datetime, self.hora, self.aula, self.sala, self.status, self.sumario, self.bibliografia))

