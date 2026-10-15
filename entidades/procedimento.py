from __future__ import annotations

from .profissional import Profissional
from .tipo_atendimento import TipoAtendimento


class Procedimento:
    def __init__(
        self,
        id: int,
        descricao: str,
        custo: float,
        tipo_atendimento: TipoAtendimento,
        profissional_responsavel: Profissional,
    ):
        self.__id = id
        self.__descricao = descricao
        self.__custo = custo
        self.__tipo_atendimento = tipo_atendimento
        self.__profissional_responsavel = profissional_responsavel

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao):
        self.__descricao = descricao

    @property
    def custo(self):
        return self.__custo

    @custo.setter
    def custo(self, custo):
        self.__custo = custo

    @property
    def tipo_atendimento(self) -> TipoAtendimento:
        return self.__tipo_atendimento

    @tipo_atendimento.setter
    def tipo_atendimento(self, tipo_atendimento: TipoAtendimento) -> None:
        self.__tipo_atendimento = tipo_atendimento

    @property
    def profissional_responsavel(self) -> Profissional:
        return self.__profissional_responsavel

    @profissional_responsavel.setter
    def profissional_responsavel(self, profissional: Profissional) -> None:
        self.__profissional_responsavel = profissional

    @property
    def profissional_responsavel_cpf(self) -> str:
        return self.__profissional_responsavel.cpf

    def custo_valido(self) -> bool:
        return self.__custo > 0
