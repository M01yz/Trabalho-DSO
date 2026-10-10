from Model import pessoa
from pagamento import Pagamento
from pessoa import Pessoa
from datetime import date

class PagamentoPix(Pagamento):
    def __init__(self, id: int, data_pagamento: date, valor_pago: float, cpf_pagador: str,):
        super().__init__(id, data_pagamento, valor_pago)
        self.__pessoa = pessoa

    @property
    def pessoa(self):
        return self.__pessoa

    @pessoa.setter
    def pessoa(self, pessoa):
        self.__pessoa = pessoa

    def validar_modalidade(self) -> None:
        if not isinstance(self.__pessoa, Pessoa):
            raise ValueError