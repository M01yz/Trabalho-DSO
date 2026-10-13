from datetime import date

from .pagamento import Pagamento


class PagamentoDinheiro(Pagamento):
    def __init__(self, id: int, data_pagamento: date, valor_pago: float):
        super().__init__(id, data_pagamento, valor_pago)

    def validar_modalidade(self) -> None:
        pass