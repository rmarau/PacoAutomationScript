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

    @property
    def isPublished(self):
        if self.status is None:
            return False
        
        return "PUBLISHED" in self.status
    
    @property
    def publish_code(self):
        if self.status is None:
            return None

        res = self.status.split(":")
        if len(res) != 2:
            raise RuntimeError("The status code in Excel must be in the format:    <status>:<pub_code>")
        
        _, code = res 
        
        if not code.strip():
            raise RuntimeError(f"Detected a Statuis publication code that is empty in {self.status}")

        return code.strip()
    
    @publish_code.setter
    def publish_code(self, value):
        if value is None:
            self.status = None    
        self.status = "PUBLISHED"+":"+str(value.strip())

    def __repr__(self):
        return str((self.datetime, self.hora, self.aula, self.sala, self.status, self.sumario, self.bibliografia))

