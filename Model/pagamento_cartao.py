from datetime import date

from .pagamento import Pagamento

class PagamentoCartao(Pagamento):
    def __init__(self, id: int, data_pagamento: date, valor_pago: float, numero_cartao: str, bandeira: str):
        super().__init__(id, data_pagamento, valor_pago)
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
        pass