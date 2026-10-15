from datetime import date

from .pagamento import Pagamento


class PagamentoDinheiro(Pagamento):
    def __init__(
        self,
        id: int,
        data_pagamento: date,
        valor_pago: float,
        parcelas: int = 1,
        atendimento_id: int | None = None,
    ):
        super().__init__(id, data_pagamento, valor_pago, parcelas, atendimento_id)

    def validar_modalidade(self) -> None:
        return None