from __future__ import annotations

from entidades.clinica import Clinica
from entidades.repositorio_sistema import RepositorioSistema
from limite.visao_cadastros import VisaoCadastros


class ControladorClinicas:
    def __init__(
        self,
        repositorio_sistema: RepositorioSistema,
        visao: VisaoCadastros | None = None,
    ) -> None:
        self.__repositorio_sistema = repositorio_sistema
        self.__visao = visao if visao is not None else VisaoCadastros()

    def incluir(self, dados: dict | None = None) -> Clinica:
        dados_clinica = dados if dados is not None else self.__visao.solicitar_dados()
        if dados_clinica.get("tipo") not in (None, "clinica"):
            raise ValueError("Este controlador só pode incluir cadastros de clínica.")

        clinica = Clinica(
            id=dados_clinica["id"],
            nome=dados_clinica["nome"],
            cidade=dados_clinica["cidade"],
            descricao=dados_clinica["descricao"],
        )
        self.__repositorio_sistema.salvar(clinica)
        return clinica

    def alterar(self, id: int, dados: dict) -> None:
        clinica = self.__repositorio_sistema.buscar_por_id("clinicas", id)
        if not isinstance(clinica, Clinica):
            raise ValueError(f"Clínica com ID {id} não encontrada.")

        if "nome" in dados:
            clinica.nome = dados["nome"]
        if "cidade" in dados:
            clinica.cidade = dados["cidade"]
        if "descricao" in dados:
            clinica.descricao = dados["descricao"]

    def excluir(self) -> None:
        clinica_id = self.__visao.solicitar_id_clinica()
        clinica = self.__repositorio_sistema.buscar_por_id("clinicas", clinica_id)
        if not isinstance(clinica, Clinica):
            raise ValueError(f"Clínica com ID {clinica_id} não encontrada.")
        self.__repositorio_sistema.excluir(clinica)

    def listar(self) -> list:
        return self.__repositorio_sistema.listar("clinicas")
