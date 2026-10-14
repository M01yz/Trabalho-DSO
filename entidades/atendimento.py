from __future__ import annotations

from .horario_funcionamento import HorarioFuncionamento
from .profissional import Profissional
from datetime import date, time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .clinica import Clinica
    from .pagamento import Pagamento
    from .procedimento import Procedimento


class Atendimento:
    def __init__(self, id: int, data: date, hora_inicio: time, hora_fim: time, valor: float):
        self.__id = id
        self.__data = data
        self.__hora_inicio = hora_inicio
        self.__hora_fim = hora_fim
        self.__valor_inicial = valor
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
        self.__data = data

    @property
    def hora_inicio(self):
        return self.__hora_inicio

    @hora_inicio.setter
    def hora_inicio(self, hora_inicio):
        self.__hora_inicio = hora_inicio

    @property
    def hora_fim(self):
        return self.__hora_fim

    @hora_fim.setter
    def hora_fim(self, hora_fim):
        self.__hora_fim = hora_fim

    @property
    def valor(self):
        return self.__valor_inicial + sum(
            procedimento.custo for procedimento in self.__procedimentos
        )

    @valor.setter
    def valor(self, valor):
        total_com_novo_valor = valor + sum(
            procedimento.custo for procedimento in self.__procedimentos
        )
        if total_com_novo_valor < self.total_pago():
            raise ValueError("O valor do atendimento não pode ser menor que o total pago.")
        self.__valor_inicial = valor

    @property
    def valor_inicial(self) -> float:
        return self.__valor_inicial

    @property
    def procedimentos(self) -> list[Procedimento]:
        return self.__procedimentos

    def vincular_procedimento(self, procedimento: Procedimento) -> None:
        if procedimento not in self.__procedimentos:
            self.__procedimentos.append(procedimento)

    def desvincular_procedimento(self, procedimento: Procedimento) -> None:
        self.__procedimentos.remove(procedimento)

    @property
    def pagamentos(self) -> list[Pagamento]:
        return self.__pagamentos

    def vincular_pagamento(self, pagamento: Pagamento) -> None:
        if pagamento in self.__pagamentos:
            return
        if self.total_pago() + pagamento.valor_pago > self.valor:
            raise ValueError("O total pago não pode ultrapassar o valor do atendimento.")
        self.__pagamentos.append(pagamento)

    def desvincular_pagamento(self, pagamento: Pagamento) -> None:
        self.__pagamentos.remove(pagamento)

    @property
    def profissional(self) -> Profissional | None:
        return self.__profissional

    @profissional.setter
    def profissional(self, profissional: Profissional | None) -> None:
        self.__profissional = profissional

    @property
    def possui_profissional(self) -> bool:
        return self.__profissional is not None

    @property
    def clinica(self) -> Clinica | None:
        return self.__clinica

    @clinica.setter
    def clinica(self, clinica: Clinica | None) -> None:
        self.__clinica = clinica

    def horario_valido(self, horario_funcionamento: HorarioFuncionamento) -> bool:
        return horario_funcionamento.contem(self.hora_inicio, self.hora_fim)

    def total_pago(self) -> float:
        return sum(pagamento.valor_pago for pagamento in self.__pagamentos)

    def saldo_restante(self) -> float:
        return self.valor - self.total_pago()