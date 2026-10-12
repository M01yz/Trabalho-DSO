from pessoa import Pessoa
from clinica import Clinica
from tipo_atendimento import TipoAtendimento
from atendimento import Atendimento
from procedimento import Procedimento
from pagamento import Pagamento

class RepositorioSistema:
    def __init__(self, pessoas: list[Pessoa], clinicas: list[Clinica], tipo_atendimento: list[TipoAtendimento], atendimentos: list[Atendimento], procedimentos: list[Procedimento], pagamentos: list[Pagamento]):
        self.__pessoas = []
        self.__clinicas = []
        self.__tipo_atendimento = []
        self.__atendimentos = []
        self.__procedimentos = []
        self.__pagamentos = []

    def salvar(self, entidade: object) -> None:
        pass

    def buscar_por_id(self, entidade: object, chave: int) -> object:
        pass

    def listar(self, tipo: str) -> list:
        pass

    def atualizar(self, entidade: object) -> None:
        pass

    def excluir(self, entidade: object) -> None:
        pass
