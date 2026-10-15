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

    def salvar(
        self,
        entidade: Atendimento | Clinica | Pagamento | Pessoa | Procedimento | TipoAtendimento,
    ) -> None:
        if isinstance(entidade, Atendimento):
            self.__atendimentos.append(entidade)
        elif isinstance(entidade, Clinica):
            self.__clinicas.append(entidade)
        elif isinstance(entidade, TipoAtendimento):
            self.__tipos_atendimento.append(entidade)
        elif isinstance(entidade, Procedimento):
            self.__procedimentos.append(entidade)
        elif isinstance(entidade, Pagamento):
            self.__pagamentos.append(entidade)
        elif isinstance(entidade, Pessoa):
            self.__pessoas.append(entidade)
        else:
            raise TypeError(f"Tipo de entidade não suportado: {type(entidade).__name__}")

    def buscar_por_id(self, tipo: str, chave: object) -> object | None:
        tipo_normalizado = tipo.strip().lower()
        listas = {
            "atendimento": (self.__atendimentos, "id"),
            "atendimentos": (self.__atendimentos, "id"),
            "clinica": (self.__clinicas, "id"),
            "clinicas": (self.__clinicas, "id"),
            "tipo_atendimento": (self.__tipos_atendimento, "id"),
            "tipos_atendimento": (self.__tipos_atendimento, "id"),
            "procedimento": (self.__procedimentos, "id"),
            "procedimentos": (self.__procedimentos, "id"),
            "pagamento": (self.__pagamentos, "id"),
            "pagamentos": (self.__pagamentos, "id"),
            "pessoa": (self.__pessoas, "cpf"),
            "pessoas": (self.__pessoas, "cpf"),
        }

        if tipo_normalizado not in listas:
            raise ValueError(f"Tipo de entidade não suportado: {tipo}")

        entidades, atributo_chave = listas[tipo_normalizado]
        return next(
            (entidade for entidade in entidades if getattr(entidade, atributo_chave) == chave),
            None,
        )

    def listar(self, tipo: str) -> list:
        tipo_normalizado = tipo.strip().lower()
        listas = {
            "atendimento": self.__atendimentos,
            "atendimentos": self.__atendimentos,
            "clinica": self.__clinicas,
            "clinicas": self.__clinicas,
            "tipo_atendimento": self.__tipos_atendimento,
            "tipos_atendimento": self.__tipos_atendimento,
            "procedimento": self.__procedimentos,
            "procedimentos": self.__procedimentos,
            "pagamento": self.__pagamentos,
            "pagamentos": self.__pagamentos,
            "pessoa": self.__pessoas,
            "pessoas": self.__pessoas,
        }

        if tipo_normalizado not in listas:
            raise ValueError(f"Tipo de entidade não suportado: {tipo}")

        return listas[tipo_normalizado]

    def atualizar(
        self,
        entidade: Atendimento | Clinica | Pagamento | Pessoa | Procedimento | TipoAtendimento,
    ) -> None:
        if isinstance(entidade, Atendimento):
            entidades, atributo_chave = self.__atendimentos, "id"
        elif isinstance(entidade, Clinica):
            entidades, atributo_chave = self.__clinicas, "id"
        elif isinstance(entidade, TipoAtendimento):
            entidades, atributo_chave = self.__tipos_atendimento, "id"
        elif isinstance(entidade, Procedimento):
            entidades, atributo_chave = self.__procedimentos, "id"
        elif isinstance(entidade, Pagamento):
            entidades, atributo_chave = self.__pagamentos, "id"
        elif isinstance(entidade, Pessoa):
            entidades, atributo_chave = self.__pessoas, "cpf"
        else:
            raise TypeError(f"Tipo de entidade não suportado: {type(entidade).__name__}")

        chave = getattr(entidade, atributo_chave)
        for indice, entidade_existente in enumerate(entidades):
            if getattr(entidade_existente, atributo_chave) == chave:
                entidades[indice] = entidade
                return

        raise ValueError(
            f"{type(entidade).__name__} com {atributo_chave} {chave} não encontrado."
        )

    def excluir(self, entidade: object) -> None:
        if entidade in self.__atendimentos:
            self.__atendimentos.remove(entidade)
        elif entidade in self.__clinicas:
            self.__clinicas.remove(entidade)
        elif entidade in self.__tipos_atendimento:
            self.__tipos_atendimento.remove(entidade)
        elif entidade in self.__procedimentos:
            self.__procedimentos.remove(entidade)
        elif entidade in self.__pagamentos:
            self.__pagamentos.remove(entidade)
        elif entidade in self.__pessoas:
            self.__pessoas.remove(entidade)
