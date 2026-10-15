from datetime import date, datetime, time
from math import isfinite

from exceptions.erro_atendimento_independente import ErroAtendimentoIndependente
from exceptions.erro_conflito_agendamento import ErroConflitoAgendamento
from exceptions.erro_horario_invalido import ErroHorarioInvalido
from exceptions.erro_cadastro_invalido import ErroCadastroInvalido
from .atendimento import Atendimento
from .clinica import Clinica
from .pagamento import Pagamento
from .paciente import Paciente
from .profissional import Profissional
from .repositorio_sistema import RepositorioSistema
from .responsavel import ResponsavelLegal
from .tipo_atendimento import TipoAtendimento


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
        paciente_cpf: str,
        tipo_atendimento_id: int,
        responsavel_legal_cpf: str | None = None,
    ) -> Atendimento:
        clinica = self.__repositorio_sistema.buscar_por_id("clinicas", clinica_id)
        if not isinstance(clinica, Clinica):
            raise ErroCadastroInvalido(f"Clínica com ID {clinica_id} não encontrada.")

        if not isinstance(paciente_cpf, str) or not paciente_cpf:
            raise ErroCadastroInvalido("O CPF do paciente deve ser informado.")
        paciente = self.__repositorio_sistema.buscar_por_id("pessoas", paciente_cpf)
        if not isinstance(paciente, Paciente):
            raise ErroCadastroInvalido(
                f"Paciente com CPF {paciente_cpf} não encontrado."
            )

        if type(tipo_atendimento_id) is not int:
            raise ErroCadastroInvalido(
                "O ID do tipo de atendimento deve ser um número inteiro."
            )
        tipo_atendimento = self.__repositorio_sistema.buscar_por_id(
            "tipos_atendimento",
            tipo_atendimento_id,
        )
        if not isinstance(tipo_atendimento, TipoAtendimento):
            raise ErroCadastroInvalido(
                f"Tipo de atendimento com ID {tipo_atendimento_id} não encontrado."
            )

        responsavel_legal = None
        if responsavel_legal_cpf:
            if not isinstance(responsavel_legal_cpf, str):
                raise ErroCadastroInvalido(
                    "O CPF do responsável legal deve ser texto."
                )
            responsavel_legal = self.__repositorio_sistema.buscar_por_id(
                "pessoas",
                responsavel_legal_cpf,
            )
            if not isinstance(responsavel_legal, ResponsavelLegal):
                raise ErroCadastroInvalido(
                    f"Responsável legal com CPF {responsavel_legal_cpf} não encontrado."
                )

        ids_utilizados = {
            atendimento.id
            for atendimento in self.__repositorio_sistema.listar("atendimentos")
            if type(atendimento.id) is int and 100_000 <= atendimento.id <= 999_999
        }
        id_agendamento = 100_000
        while id_agendamento in ids_utilizados:
            id_agendamento += 1
        if id_agendamento > 999_999:
            raise ErroConflitoAgendamento(
                "Não há mais IDs de seis dígitos disponíveis para agendamentos."
            )

        atendimento = Atendimento(
            id_agendamento,
            data,
            hora_inicio,
            hora_fim,
            valor,
            paciente,
            tipo_atendimento,
            responsavel_legal,
        )
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
            raise ErroCadastroInvalido(
                f"Atendimento com ID {atendimento.id} não encontrado."
            )

        atendimento.clinica = atendimento_existente.clinica
        self.validar_agendamento(
            atendimento,
            ignorar_id=atendimento_existente.id,
        )
        atendimento_existente.valor = atendimento.valor_inicial
        atendimento_existente.data = atendimento.data
        atendimento_existente.hora_inicio = atendimento.hora_inicio
        atendimento_existente.hora_fim = atendimento.hora_fim
        atendimento_existente.paciente = atendimento.paciente
        atendimento_existente.tipo_atendimento = atendimento.tipo_atendimento
        atendimento_existente.responsavel_legal = atendimento.responsavel_legal
        atendimento_existente.profissional = atendimento.profissional

    def cancelar(self, id: int) -> None:
        atendimento = self.__repositorio_sistema.buscar_por_id("atendimentos", id)
        if not isinstance(atendimento, Atendimento):
            raise ErroCadastroInvalido(f"Atendimento com ID {id} não encontrado.")

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

        if not isinstance(atendimento.data, date) or isinstance(
            atendimento.data,
            datetime,
        ):
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
            raise ErroCadastroInvalido(
                "O valor do atendimento deve ser maior que zero."
            )

        if not isinstance(atendimento.paciente, Paciente):
            raise ErroCadastroInvalido(
                "O atendimento deve estar associado a um paciente."
            )
        if not isinstance(atendimento.tipo_atendimento, TipoAtendimento):
            raise ErroCadastroInvalido(
                "O atendimento deve estar associado a um tipo de atendimento."
            )
        if atendimento.paciente.idade_na_data(atendimento.data) < 0:
            raise ErroHorarioInvalido(
                "A data do atendimento não pode ser anterior ao nascimento."
            )
        if (
            not atendimento.paciente.pode_atender_sozinho(atendimento.data)
            and not isinstance(atendimento.responsavel_legal, ResponsavelLegal)
        ):
            raise ErroAtendimentoIndependente()
        if (
            atendimento.responsavel_legal is not None
            and not isinstance(atendimento.responsavel_legal, ResponsavelLegal)
        ):
            raise ErroCadastroInvalido(
                "O responsável informado deve ser um responsável legal."
            )
        pagamentos_vinculados = (
            pagamento
            for pagamento in self.__repositorio_sistema.listar("pagamentos")
            if isinstance(pagamento, Pagamento)
            and pagamento.atendimento_id == atendimento.id
        )
        if any(
            pagamento.data_pagamento > atendimento.data
            for pagamento in pagamentos_vinculados
        ):
            raise ErroHorarioInvalido(
                "A data do atendimento não pode ser anterior à data de um pagamento."
            )

        if not isinstance(atendimento.clinica, Clinica):
            raise ErroCadastroInvalido(
                "O atendimento deve estar associado a uma clínica."
            )
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

        if not isinstance(atendimento.clinica, Clinica):
            atendimento.profissional = None
            return False

        for pessoa in atendimento.clinica.profissionais:
            if not isinstance(pessoa, Profissional):
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