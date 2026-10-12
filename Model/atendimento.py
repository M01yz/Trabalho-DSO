from .horario_funcionamento import HorarioFuncionamento
from datetime import date, time


class Atendimento:
    def __init__(self, id: int, data: date, hora_inicio: time, hora_fim: time, valor: float):
        self.__id = id
        self.__data = data
        self.__hora_inicio = hora_inicio
        self.__hora_fim = hora_fim
        self.__valor = valor

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        self.__data = data

    @property
    def hora_inicio(self):
        return self.__hora_inicio

    @hora_inicio.setter
    def hora_inicio(self, hora_inicio):
        self.__hora_inicio = hora_inicio

    @property
    def hora_fim(self):
        return self.__hora_fim

    @hora_fim.setter
    def hora_fim(self, hora_fim):
        self.__hora_fim = hora_fim

    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, valor):
        self.__valor = valor

    def horario_valido(self, horario_funcionamento: HorarioFuncionamento) -> bool:
        pass

    def total_pago(self) -> float:
        pass

    def saldo_restante(self) -> float:
        pass