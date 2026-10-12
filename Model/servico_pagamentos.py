from servico_registro import ServicoRegistro
from pagamento import Pagamento

class ServicoPagamentos(ServicoRegistro):
    def registrar(self, dados: dict) -> object:
        pass

    def alterar(self, id: int, dados: dict) -> None:
        pass

    def excluir(self, id: int) -> None:
        pass

    def listar(self) -> list:
        pass

    def validar_pagamento(self, pagamento: Pagamento) -> None:
        pass
