from abc import ABC, abstractmethod
from datetime import date


class Pagamento(ABC):
    def __init__(self, id: int, data_pagamento: date, valor_pago: float):
        self.__id = id
        self.__data_pagamento = data_pagamento
        self.__valor_pago = valor_pago

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def data_pagamento(self):
        return self.__data_pagamento

    @data_pagamento.setter
    def data_pagamento(self, data_pagamento):
        self.__data_pagamento = data_pagamento

    @property
    def valor_pago(self):
        return self.__valor_pago

    @valor_pago.setter
    def valor_pago(self, valor_pago):
        self.__valor_pago = valor_pago

    @abstractmethod
    def validar_modalidade(self) -> None:
        pass