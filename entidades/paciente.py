from datetime import date, datetime

from exceptions.erro_cadastro_invalido import ErroCadastroInvalido

from .pessoa import Pessoa

class Paciente(Pessoa):
    def __init__(self, data_nascimento: date, nome: str, cpf: str, celular: str):
        super().__init__(nome, cpf, celular)
        self.data_nascimento = data_nascimento

    @property
    def data_nascimento(self) -> date:
        return self.__data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, data_nascimento: date) -> None:
        if not isinstance(data_nascimento, date) or isinstance(
            data_nascimento,
            datetime,
        ):
            raise ErroCadastroInvalido(
                "A data de nascimento deve ser uma data válida."
            )
        self.__data_nascimento = data_nascimento

    def idade_na_data(self, data: date) -> int:
        if not isinstance(data, date) or isinstance(data, datetime):
            raise ErroCadastroInvalido(
                "A data de referência para calcular a idade é inválida."
            )
        data_paciente = self.__data_nascimento
        idade = data.year - data_paciente.year - ((data.month, data.day) < (data_paciente.month, data_paciente.day))
        return idade

    def pode_atender_sozinho(self, data: date) -> bool:
        idade = self.idade_na_data(data)
        return idade >= 18

    def tipo_pessoa(self) -> str:
        return "Paciente"