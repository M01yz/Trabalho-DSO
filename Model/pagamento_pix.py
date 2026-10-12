from datetime import date

from .pagamento import Pagamento


class PagamentoPix(Pagamento):
    def __init__(self, id: int, data_pagamento: date, valor_pago: float, cpf_pagador: str):
        super().__init__(id, data_pagamento, valor_pago)
        self.__cpf_pagador = cpf_pagador

    @property
    def cpf_pagador(self) -> str:
        return self.__cpf_pagador

    @cpf_pagador.setter
    def cpf_pagador(self, cpf_pagador: str):
        self.__cpf_pagador = cpf_pagador

    def validar_modalidade(self) -> None:
        pass