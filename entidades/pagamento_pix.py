from datetime import date

from exceptions.erro_pagamento_invalido import ErroPagamentoInvalido

from .pagamento import Pagamento


class PagamentoPix(Pagamento):
    def __init__(
        self,
        id: int,
        data_pagamento: date,
        valor_pago: float,
        cpf_pagador: str,
        parcelas: int = 1,
        atendimento_id: int | None = None,
    ):
        super().__init__(id, data_pagamento, valor_pago, parcelas, atendimento_id)
        self.__cpf_pagador = cpf_pagador

    @property
    def cpf_pagador(self) -> str:
        return self.__cpf_pagador

    @cpf_pagador.setter
    def cpf_pagador(self, cpf_pagador: str):
        self.__cpf_pagador = cpf_pagador

    def validar_modalidade(self) -> None:
        if (
            not isinstance(self.__cpf_pagador, str)
            or len(self.__cpf_pagador) != 11
            or not self.__cpf_pagador.isdigit()
        ):
            raise ErroPagamentoInvalido(
                "O CPF do pagador deve conter 11 dígitos numéricos."
            )