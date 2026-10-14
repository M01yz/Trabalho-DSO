from datetime import date, time

from .atendimento import Atendimento
from .clinica import Clinica
from .profissional import Profissional
from .repositorio_sistema import RepositorioSistema


class ServicoAgendamento:
    def __init__(self, repositorio_sistema: RepositorioSistema):
        self.__repositorio_sistema = repositorio_sistema

    def agendar(
        self,
        data: date,
        hora_inicio: time,
        hora_fim: time,
        valor: float,
        clinica_id: int,
    ) -> Atendimento:
        clinica = self.__repositorio_sistema.buscar_por_id("clinicas", clinica_id)
        if not isinstance(clinica, Clinica):
            raise ValueError(f"Clínica com ID {clinica_id} não encontrada.")

        ids_utilizados = {
            atendimento.id
            for atendimento in self.__repositorio_sistema.listar("atendimentos")
            if type(atendimento.id) is int and 100_000 <= atendimento.id <= 999_999
        }
        id_agendamento = 100_000
        while id_agendamento in ids_utilizados:
            id_agendamento += 1
        if id_agendamento > 999_999:
            raise ValueError("Não há mais IDs de seis dígitos disponíveis para agendamentos.")

        atendimento = Atendimento(0, data, hora_inicio, hora_fim, valor)
        atendimento.data = data
        atendimento.hora_inicio = hora_inicio
        atendimento.hora_fim = hora_fim
        atendimento.id = id_agendamento
        atendimento.clinica = clinica
        clinica.vincular_atendimento(atendimento)
        self.__repositorio_sistema.salvar(atendimento)
        return atendimento

    def alterar(self, atendimento: Atendimento) -> None:
        atendimento_existente = self.__repositorio_sistema.buscar_por_id(
            "atendimentos",
            atendimento.id,
        )
        if not isinstance(atendimento_existente, Atendimento):
            raise ValueError(f"Atendimento com ID {atendimento.id} não encontrado.")

        atendimento_existente.data = atendimento.data
        atendimento_existente.hora_inicio = atendimento.hora_inicio
        atendimento_existente.hora_fim = atendimento.hora_fim
        atendimento_existente.valor = atendimento.valor_inicial

    def cancelar(self, id: int) -> None:
        atendimento = self.__repositorio_sistema.buscar_por_id("atendimentos", id)
        if not isinstance(atendimento, Atendimento):
            raise ValueError(f"Atendimento com ID {id} não encontrado.")

        self.__repositorio_sistema.remover(atendimento)

    def validar_agendamento(self, atendimento: Atendimento) -> None:
        if type(atendimento.id) is not int or not 100_000 <= atendimento.id <= 999_999:
            raise ValueError("ID inválido.")

        ids_duplicados = any(
            outro_atendimento is not atendimento
            and outro_atendimento.id == atendimento.id
            for outro_atendimento in self.__repositorio_sistema.listar("atendimentos")
        )
        if ids_duplicados:
            raise ValueError(f"ID duplicado: {atendimento.id}.")

        if atendimento.hora_inicio >= atendimento.hora_fim:
            raise ValueError("Horário Inválido.")

        if not self.profissional_disponivel(atendimento):
            raise ValueError("Não há profissionais disponíveis para o horário solicitado.")

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