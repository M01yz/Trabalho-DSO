from __future__ import annotations

from exceptions.erro_cadastro_duplicado import ErroCadastroDuplicado
from exceptions.erro_cadastro_invalido import ErroCadastroInvalido

from entidades.repositorio_sistema import RepositorioSistema
from entidades.tipo_atendimento import TipoAtendimento
from limite.visao_cadastros import VisaoCadastros


class ControladorTiposAtendimento:
    def __init__(
        self,
        repositorio_sistema: RepositorioSistema,
        visao: VisaoCadastros | None = None,
    ) -> None:
        self.__repositorio_sistema = repositorio_sistema
        self.__visao = visao if visao is not None else VisaoCadastros()

    def incluir(self, dados: dict | None = None) -> TipoAtendimento:
        dados_tipo = (
            dados
            if dados is not None
            else self.__visao.solicitar_dados(tipo="tipo_atendimento")
        )
        if not isinstance(dados_tipo, dict):
            raise ErroCadastroInvalido(
                "Os dados do tipo de atendimento são inválidos."
            )
        if dados_tipo.get("tipo") != "tipo_atendimento":
            raise ErroCadastroInvalido(
                "Este controlador só pode incluir tipos de atendimento."
            )

        tipo_id = dados_tipo["id"]
        if type(tipo_id) is not int:
            raise ErroCadastroInvalido(
                "O ID do tipo de atendimento deve ser um número inteiro."
            )
        if self.__repositorio_sistema.buscar_por_id(
            "tipos_atendimento",
            tipo_id,
        ) is not None:
            raise ErroCadastroDuplicado(
                f"Tipo de atendimento com ID {tipo_id} já existe."
            )

        tipo_atendimento = TipoAtendimento(
            id=tipo_id,
            nome=dados_tipo["nome"],
            descricao=dados_tipo["descricao"],
        )
        self.__repositorio_sistema.salvar(tipo_atendimento)
        return tipo_atendimento

    def alterar(self, id: int, dados: dict | None = None) -> None:
        tipo_atendimento = self.__repositorio_sistema.buscar_por_id(
            "tipos_atendimento",
            id,
        )
        if not isinstance(tipo_atendimento, TipoAtendimento):
            raise ValueError(f"Tipo de atendimento com ID {id} não encontrado.")

        dados = (
            dados
            if dados is not None
            else self.__visao.solicitar_dados_alteracao("tipo_atendimento")
        )
        if "nome" in dados:
            tipo_atendimento.nome = dados["nome"]
        if "descricao" in dados:
            tipo_atendimento.descricao = dados["descricao"]

    def excluir(self, id: int) -> None:
        tipo_atendimento = self.__repositorio_sistema.buscar_por_id(
            "tipos_atendimento",
            id,
        )
        if not isinstance(tipo_atendimento, TipoAtendimento):
            raise ValueError(f"Tipo de atendimento com ID {id} não encontrado.")
        self.__repositorio_sistema.excluir(tipo_atendimento)

    def listar(self) -> list:
        return self.__repositorio_sistema.listar("tipos_atendimento")
