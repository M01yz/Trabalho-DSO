from abc import ABC, abstractmethod

class ServicoRegistro(ABC):
    @abstractmethod
    def registrar(self, dados: dict) -> object:
        pass

    @abstractmethod
    def alterar(self, id: int, dados: dict) -> None:
        pass

    @abstractmethod
    def excluir(self, id: int) -> None:
        pass

    @abstractmethod
    def listar(self) -> list:
        pass