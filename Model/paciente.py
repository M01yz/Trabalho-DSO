from datetime import date
from pessoa import Pessoa

class Paciente(Pessoa):
    def __init__(self, data_nascimento, nome, cpf, celular):
        super().__init__(nome, cpf, celular)
        self.__data_nascimento = data_nascimento

    def idade_na_data(self, data: date) -> int:
        data_paciente = self.__data_nascimento
        idade = data.year - data_paciente.year - ((data.month, data.day) < (data_paciente.month, data_paciente.day))
        if idade < 18:
            raise ValueError
        else:
            return idade
    def pode_atender_sozinho(self) -> bool:
        idade = self.idade_na_data(date.today())
        return idade >= 18

    def tipo_pessoa(self) -> str:
        return "Paciente"