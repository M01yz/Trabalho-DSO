from __future__ import annotations

from datetime import date, datetime, time
from math import isfinite
from typing import TYPE_CHECKING

from exceptions.erro_cadastro_invalido import ErroCadastroInvalido
from exceptions.erro_horario_invalido import ErroHorarioInvalido
from exceptions.erro_pagamento_invalido import ErroPagamentoInvalido

from .clinica import Clinica
from .horario_funcionamento import HorarioFuncionamento
from .paciente import Paciente
from .profissional import Profissional
from .responsavel import ResponsavelLegal
from .tipo_atendimento import TipoAtendimento

if TYPE_CHECKING:
    from .pagamento import Pagamento
    from .procedimento import Procedimento


class Atendimento:
    def __init__(
        self,
        id: int,
        data: date,
        hora_inicio: time,
        hora_fim: time,
        valor: float,
        paciente: Paciente,
        tipo_atendimento: TipoAtendimento,
        responsavel_legal: ResponsavelLegal | None = None,
    ):
        self.__id = id
        self.__data = data
        self.__hora_inicio = hora_inicio
        self.__hora_fim = hora_fim
        self.__valor_inicial = valor
        self.__paciente = paciente
        self.__tipo_atendimento = tipo_atendimento
        self.__responsavel_legal = responsavel_legal
        self.__profissional: Profissional | None = None
        self.__clinica: Clinica | None = None
        self.__procedimentos: list[Procedimento] = []
        self.__pagamentos: list[Pagamento] = []

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
        if not isinstance(data, date) or isinstance(data, datetime):
            raise ErroHorarioInvalido("A data do atendimento é inválida.")
        self.__data = data

    @property
    def hora_inicio(self):
        return self.__hora_inicio

    @hora_inicio.setter
    def hora_inicio(self, hora_inicio):
        if not isinstance(hora_inicio, time):
            raise ErroHorarioInvalido("O horário de início é inválido.")
        self.__hora_inicio = hora_inicio

    @property
    def hora_fim(self):
        return self.__hora_fim

    @hora_fim.setter
    def hora_fim(self, hora_fim):
        if not isinstance(hora_fim, time):
            raise ErroHorarioInvalido("O horário de término é inválido.")
        self.__hora_fim = hora_fim

    @property
    def valor(self):
        return self.__valor_inicial + sum(
            procedimento.custo for procedimento in self.__procedimentos
        )

    @valor.setter
    def valor(self, valor):
        if (
            not isinstance(valor, (int, float))
            or isinstance(valor, bool)
            or not isfinite(valor)
            or valor <= 0
        ):
            raise ErroCadastroInvalido(
                "O valor do atendimento deve ser um número maior que zero."
            )
        total_com_novo_valor = valor + sum(
            procedimento.custo for procedimento in self.__procedimentos
        )
        if total_com_novo_valor < self.total_pago():
            raise ErroPagamentoInvalido(
                "O valor do atendimento não pode ser menor que o total pago."
            )
        self.__valor_inicial = valor

    @property
    def valor_inicial(self) -> float:
        return self.__valor_inicial

    @staticmethod
    def __validar_vinculo(valor: object, esperado: type, nome: str) -> None:
        if not isinstance(valor, esperado):
            raise ErroCadastroInvalido(
                f"O atendimento deve estar associado a {nome}."
            )

    @property
    def paciente(self) -> Paciente:
        return self.__paciente

    @paciente.setter
    def paciente(self, paciente: Paciente) -> None:
        self.__validar_vinculo(paciente, Paciente, "um paciente")
        self.__paciente = paciente

    @property
    def tipo_atendimento(self) -> TipoAtendimento:
        return self.__tipo_atendimento

    @tipo_atendimento.setter
    def tipo_atendimento(self, tipo_atendimento: TipoAtendimento) -> None:
        self.__validar_vinculo(
            tipo_atendimento,
            TipoAtendimento,
            "um tipo de atendimento",
        )
        self.__tipo_atendimento = tipo_atendimento

    @property
    def responsavel_legal(self) -> ResponsavelLegal | None:
        return self.__responsavel_legal

    @responsavel_legal.setter
    def responsavel_legal(
        self,
        responsavel_legal: ResponsavelLegal | None,
    ) -> None:
        if responsavel_legal is not None:
            self.__validar_vinculo(
                responsavel_legal,
                ResponsavelLegal,
                "um responsável legal",
            )
        self.__responsavel_legal = responsavel_legal

    @property
    def paciente_cpf(self) -> str:
        return self.__paciente.cpf

    @property
    def tipo_atendimento_nome(self) -> str:
        return self.__tipo_atendimento.nome

    @property
    def responsavel_legal_cpf(self) -> str | None:
        if self.__responsavel_legal is None:
            return None
        return self.__responsavel_legal.cpf

    @property
    def profissional_cpf(self) -> str | None:
        if self.__profissional is None:
            return None
        return self.__profissional.cpf

    @property
    def clinica_nome(self) -> str | None:
        if self.__clinica is None:
            return None
        return self.__clinica.nome

    @property
    def procedimentos(self) -> list[Procedimento]:
        return list(self.__procedimentos)

    def vincular_procedimento(self, procedimento: Procedimento) -> None:
        if procedimento not in self.__procedimentos:
            self.__procedimentos.append(procedimento)

    def desvincular_procedimento(self, procedimento: Procedimento) -> None:
        if procedimento not in self.__procedimentos:
            raise ErroCadastroInvalido(
                "O procedimento não está vinculado a este atendimento."
            )
        if self.valor - procedimento.custo < self.total_pago():
            raise ErroPagamentoInvalido(
                "Não é possível remover o procedimento: o total pago "
                "ficaria acima do valor atualizado do atendimento."
            )
        self.__procedimentos.remove(procedimento)

    @property
    def pagamentos(self) -> list[Pagamento]:
        return list(self.__pagamentos)

    def vincular_pagamento(self, pagamento: Pagamento) -> None:
        if pagamento in self.__pagamentos:
            return
        if self.total_pago() + pagamento.valor_pago > self.valor:
            raise ErroPagamentoInvalido(
                "O total pago não pode ultrapassar o valor do atendimento."
            )
        self.__pagamentos.append(pagamento)

    def desvincular_pagamento(self, pagamento: Pagamento) -> None:
        self.__pagamentos.remove(pagamento)

    @property
    def profissional(self) -> Profissional | None:
        return self.__profissional

    @profissional.setter
    def profissional(self, profissional: Profissional | None) -> None:
        if profissional is not None:
            self.__validar_vinculo(profissional, Profissional, "um profissional")
        self.__profissional = profissional

    @property
    def possui_profissional(self) -> bool:
        return self.__profissional is not None

    @property
    def clinica(self) -> Clinica | None:
        return self.__clinica

    @clinica.setter
    def clinica(self, clinica: Clinica | None) -> None:
        if clinica is not None:
            self.__validar_vinculo(clinica, Clinica, "uma clínica")
        self.__clinica = clinica

    def horario_valido(self, horario_funcionamento: HorarioFuncionamento) -> bool:
        return horario_funcionamento.contem(self.hora_inicio, self.hora_fim)

    def total_pago(self) -> float:
        return sum(pagamento.valor_pago for pagamento in self.__pagamentos)

    def saldo_restante(self) -> float:
        return self.valor - self.total_pago()