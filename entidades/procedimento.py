from __future__ import annotations

from .tipo_atendimento import TipoAtendimento


class Procedimento:
    def __init__(
        self,
        id: int,
        descricao: str,
        custo: float,
        tipo_atendimento: TipoAtendimento,
    ):
        self.__id = id
        self.__descricao = descricao
        self.__custo = custo
        self.__tipo_atendimento = tipo_atendimento

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

    def custo_valido(self) -> bool:
        return self.__custo > 0
