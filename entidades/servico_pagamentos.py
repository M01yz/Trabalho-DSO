from .pagamento import Pagamento

class ServicoPagamentos:
    def registrar(self, pagamento: Pagamento) -> Pagamento:
        pass

    def alterar(self, pagamento: Pagamento) -> None:
        pass

    def excluir(self, id: int) -> None:
        pass

    def listar(self) -> list:
        pass

    def validar_pagamento(self, pagamento: Pagamento) -> None:
        pass
