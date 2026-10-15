from datetime import date, time
from math import isfinite

from exceptions.erro_conflito_agendamento import ErroConflitoAgendamento
from exceptions.erro_horario_invalido import ErroHorarioInvalido
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

        atendimento = Atendimento(id_agendamento, data, hora_inicio, hora_fim, valor)
        atendimento.clinica = clinica
        self.validar_agendamento(atendimento)
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

        atendimento.clinica = atendimento_existente.clinica
        self.validar_agendamento(
            atendimento,
            ignorar_id=atendimento_existente.id,
        )
        atendimento_existente.valor = atendimento.valor_inicial
        atendimento_existente.data = atendimento.data
        atendimento_existente.hora_inicio = atendimento.hora_inicio
        atendimento_existente.hora_fim = atendimento.hora_fim
        atendimento_existente.profissional = atendimento.profissional

    def cancelar(self, id: int) -> None:
        atendimento = self.__repositorio_sistema.buscar_por_id("atendimentos", id)
        if not isinstance(atendimento, Atendimento):
            raise ValueError(f"Atendimento com ID {id} não encontrado.")

        self.__repositorio_sistema.excluir(atendimento)
        if atendimento.clinica is not None:
            atendimento.clinica.desvincular_atendimento(atendimento)

    def validar_agendamento(
        self,
        atendimento: Atendimento,
        ignorar_id: int | None = None,
    ) -> None:
        if type(atendimento.id) is not int or not 100_000 <= atendimento.id <= 999_999:
            raise ErroConflitoAgendamento("O ID do atendimento é inválido.")

        ids_duplicados = any(
            outro_atendimento is not atendimento
            and outro_atendimento.id != ignorar_id
            and outro_atendimento.id == atendimento.id
            for outro_atendimento in self.__repositorio_sistema.listar("atendimentos")
        )
        if ids_duplicados:
            raise ErroConflitoAgendamento(f"ID duplicado: {atendimento.id}.")

        if not isinstance(atendimento.data, date):
            raise ErroHorarioInvalido("A data do atendimento é inválida.")
        if not isinstance(atendimento.hora_inicio, time) or not isinstance(
            atendimento.hora_fim,
            time,
        ):
            raise ErroHorarioInvalido("Os horários do atendimento são inválidos.")
        if atendimento.hora_inicio >= atendimento.hora_fim:
            raise ErroHorarioInvalido("O horário de início deve ser anterior ao término.")
        if (
            not isinstance(atendimento.valor_inicial, (int, float))
            or not isfinite(atendimento.valor_inicial)
            or atendimento.valor_inicial <= 0
        ):
            raise ValueError("O valor do atendimento deve ser maior que zero.")

        if not isinstance(atendimento.clinica, Clinica):
            raise ValueError("O atendimento deve estar associado a uma clínica.")
        if not atendimento.clinica.dentro_do_expediente(
            atendimento.data,
            atendimento.hora_inicio,
            atendimento.hora_fim,
        ):
            raise ErroHorarioInvalido(
                "O horário solicitado está fora do expediente da clínica."
            )

        if not self.profissional_disponivel(atendimento, ignorar_id):
            raise ErroConflitoAgendamento(
                "Não há profissionais disponíveis para o horário solicitado."
            )

    def profissional_disponivel(
        self,
        atendimento: Atendimento,
        ignorar_id: int | None = None,
    ) -> bool:
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
                and outro_atendimento.id != ignorar_id
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