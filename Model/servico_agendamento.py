from servico_registro import ServicoRegistro
from atendimento import Atendimento

class ServicoAgendamento(ServicoRegistro):
    def registrar(self, dados: dict) -> object:
        pass

    def alterar(self, id: int, dados: dict) -> None:
        pass

    def excluir(self, id: int) -> None:
        pass

    def listar(self) -> list:
        pass

    def validar_agendamento(self, atendimento: Atendimento) -> None:
        pass

    def profissional_disponivel(self, atendimento: Atendimento) -> bool:
        pass