from .atendimento import Atendimento

class ServicoAgendamento:
    def agendar(self, atendimento: Atendimento) -> Atendimento:
        pass

    def alterar(self, atendimento: Atendimento) -> None:
        pass

    def cancelar(self, id: int) -> None:
        pass

    def validar_agendamento(self, atendimento: Atendimento) -> None:
        pass

    def profissional_disponivel(self, atendimento: Atendimento) -> bool:
        pass