from datetime import date, time
from .horario_funcionamento import HorarioFuncionamento
from .profissional import Profissional


class Clinica:
    def __init__(self, id: int, nome: str, cidade: str, descricao: str):
        self.__id = id
        self.__nome = nome
        self.__cidade = cidade
        self.__descricao = descricao
        self.__profissionais = []

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def cidade(self):
        return self.__cidade

    @cidade.setter
    def cidade(self, cidade):
        self.__cidade = cidade

    @property
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao):
        self.__descricao = descricao

    def dentro_do_expediente(self, data: date, inicio: time, fim: time) -> bool:
        return horario_funcionamento.contem(inicio, fim)

    def vincular_profissional(self, prof: Profissional) -> None:
        self.__profissionais.append(prof)

    def desvincular_profissional(self, prof: Profissional) -> None:
        self.__profissionais.remove(prof)
