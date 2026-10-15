from datetime import date

from exceptions.erro_pagamento_invalido import ErroPagamentoInvalido

from .pagamento import Pagamento


class PagamentoCartao(Pagamento):
    def __init__(
        self,
        id: int,
        data_pagamento: date,
        valor_pago: float,
        numero_cartao: str,
        bandeira: str,
        parcelas: int = 1,
        atendimento_id: int | None = None,
    ):
        super().__init__(id, data_pagamento, valor_pago, parcelas, atendimento_id)
        self.__numero_cartao = numero_cartao
        self.__bandeira = bandeira

    @property
    def numero_cartao(self):
        return self.__numero_cartao

    @numero_cartao.setter
    def numero_cartao(self, numero_cartao):
        self.__numero_cartao = numero_cartao

    @property
    def bandeira(self):
        return self.__bandeira

    @bandeira.setter
    def bandeira(self, bandeira):
        self.__bandeira = bandeira

    def validar_modalidade(self) -> None:
        if (
            not isinstance(self.__numero_cartao, str)
            or not self.__numero_cartao.strip()
        ):
            raise ErroPagamentoInvalido("O número do cartão não pode ficar vazio.")
        if not isinstance(self.__bandeira, str) or not self.__bandeira.strip():
            raise ErroPagamentoInvalido("A bandeira do cartão não pode ficar vazia.")