from abc import ABC, abstractmethod


class Pessoa(ABC):
    def __init__(self, nome: str, cpf: str, celular: str):
        self.__nome = nome
        self.__cpf = cpf
        self.__celular = celular

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf):
        self.__cpf = cpf

    @property
    def celular(self):
        return self.__celular

    @celular.setter
    def celular(self, celular):
        self.__celular = celular

    def validar_cpf(self) -> bool:
        if len(self.cpf) != 11 or not self.cpf.isdigit():
            return False
        else:
            return True

    @abstractmethod
    def tipo_pessoa(self) -> str:
        pass