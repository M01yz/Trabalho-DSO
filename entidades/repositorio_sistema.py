from .atendimento import Atendimento
from .clinica import Clinica
from .pagamento import Pagamento
from .pessoa import Pessoa
from .procedimento import Procedimento
from .tipo_atendimento import TipoAtendimento

class RepositorioSistema:
    def __init__(
        self,
        pessoas: list[Pessoa] | None = None,
        clinicas: list[Clinica] | None = None,
        tipos_atendimento: list[TipoAtendimento] | None = None,
        atendimentos: list[Atendimento] | None = None,
        procedimentos: list[Procedimento] | None = None,
        pagamentos: list[Pagamento] | None = None,
    ):
        self.__pessoas = pessoas if pessoas is not None else []
        self.__clinicas = clinicas if clinicas is not None else []
        self.__tipos_atendimento = tipos_atendimento if tipos_atendimento is not None else []
        self.__atendimentos = atendimentos if atendimentos is not None else []
        self.__procedimentos = procedimentos if procedimentos is not None else []
        self.__pagamentos = pagamentos if pagamentos is not None else []

    def salvar(self, entidade: object) -> None:
        pass

    def buscar_por_id(self, tipo: str, chave: object) -> object:
        pass

    def listar(self, tipo: str) -> list:
        pass

    def atualizar(self, entidade: object) -> None:
        pass

    def excluir(self, entidade: object) -> None:
        pass
