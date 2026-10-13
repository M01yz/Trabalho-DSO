from .atendimento import Atendimento
from .profissional import Profissional
from .repositorio_sistema import RepositorioSistema


class ServicoAgendamento:
    def __init__(self, repositorio_sistema: RepositorioSistema):
        self.__repositorio_sistema = repositorio_sistema

    def agendar(self, atendimento: Atendimento) -> Atendimento:
        pass

    def alterar(self, atendimento: Atendimento) -> None:
        pass

    def cancelar(self, id: int) -> None:
        pass

    def validar_agendamento(self, atendimento: Atendimento) -> None:
        pass

    def profissional_disponivel(self, atendimento: Atendimento) -> bool:
        if atendimento.hora_inicio >= atendimento.hora_fim:
            atendimento.profissional = None
            return False

        atendimentos = self.__repositorio_sistema.listar("atendimentos")
        pessoas = self.__repositorio_sistema.listar("pessoas")

        for pessoa in pessoas:
            if not isinstance(pessoa, Profissional) or pessoa.tipo_pessoa() != "Profissional":
                continue

            conflito = any(
                outro_atendimento is not atendimento
                and outro_atendimento.profissional is pessoa
                and outro_atendimento.data == atendimento.data
                and atendimento.hora_inicio < outro_atendimento.hora_fim
                and outro_atendimento.hora_inicio < atendimento.hora_fim
                for outro_atendimento in atendimentos
            )
            if not conflito:
                atendimento.profissional = pessoa
                return True

        atendimento.profissional = None
        return False