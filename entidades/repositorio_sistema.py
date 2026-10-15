from .atendimento import Atendimento
from .clinica import Clinica
from .pagamento import Pagamento
from .pessoa import Pessoa
from .procedimento import Procedimento
from .tipo_atendimento import TipoAtendimento
from exceptions.erro_cadastro_duplicado import ErroCadastroDuplicado


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
        self.__pessoas = list(pessoas) if pessoas is not None else []
        self.__clinicas = list(clinicas) if clinicas is not None else []
        self.__tipos_atendimento = (
            list(tipos_atendimento) if tipos_atendimento is not None else []
        )
        self.__atendimentos = list(atendimentos) if atendimentos is not None else []
        self.__procedimentos = list(procedimentos) if procedimentos is not None else []
        self.__pagamentos = list(pagamentos) if pagamentos is not None else []

    def salvar(
        self,
        entidade: Atendimento | Clinica | Pagamento | Pessoa | Procedimento | TipoAtendimento,
    ) -> None:
        if isinstance(entidade, Atendimento):
            entidades, tipo_busca, nome_entidade = (
                self.__atendimentos,
                "atendimentos",
                "atendimento",
            )
        elif isinstance(entidade, Clinica):
            entidades, tipo_busca, nome_entidade = (
                self.__clinicas,
                "clinicas",
                "clínica",
            )
        elif isinstance(entidade, TipoAtendimento):
            entidades, tipo_busca, nome_entidade = (
                self.__tipos_atendimento,
                "tipos_atendimento",
                "tipo de atendimento",
            )
        elif isinstance(entidade, Procedimento):
            entidades, tipo_busca, nome_entidade = (
                self.__procedimentos,
                "procedimentos",
                "procedimento",
            )
        elif isinstance(entidade, Pagamento):
            entidades, tipo_busca, nome_entidade = (
                self.__pagamentos,
                "pagamentos",
                "pagamento",
            )
        elif isinstance(entidade, Pessoa):
            entidades, tipo_busca, nome_entidade = (
                self.__pessoas,
                "pessoas",
                "pessoa",
            )
        else:
            raise TypeError(f"Tipo de entidade não suportado: {type(entidade).__name__}")

        chave = self.__chave(entidade)
        if self.buscar_por_id(tipo_busca, chave) is not None:
            raise ErroCadastroDuplicado(
                f"Já existe um cadastro de {nome_entidade} "
                f"com o identificador {chave}."
            )
        entidades.append(entidade)

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

        return list(listas[tipo_normalizado])

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

    @staticmethod
    def __chave(entidade: object) -> object:
        if isinstance(entidade, Pessoa):
            return entidade.cpf
        return getattr(entidade, "id")

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
