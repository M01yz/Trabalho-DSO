from .pessoa import Pessoa


class ResponsavelLegal(Pessoa):
    def __init__(self, nome: str, cpf: str, celular: str):
        super().__init__(nome, cpf, celular)

    def tipo_pessoa(self) -> str:
        return "Responsável"


Responsavel = ResponsavelLegal