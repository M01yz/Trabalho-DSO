from __future__ import annotations

from math import isfinite

from entidades.atendimento import Atendimento
from entidades.procedimento import Procedimento
from entidades.repositorio_sistema import RepositorioSistema
from entidades.tipo_atendimento import TipoAtendimento
from limite.visao_atendimentos import VisaoAtendimentos


class ControladorProcedimentos:
    def __init__(
        self,
        repositorio_sistema: RepositorioSistema,
        visao: VisaoAtendimentos | None = None,
    ) -> None:
        self.__repositorio_sistema = repositorio_sistema
        self.__visao = visao if visao is not None else VisaoAtendimentos()

    def incluir(
        self,
        atendimento_id: int,
        dados: dict | None = None,
    ) -> Procedimento:
        dados_procedimento = (
            dados if dados is not None else self.__visao.solicitar_procedimento()
        )
        atendimento = self.__repositorio_sistema.buscar_por_id(
            "atendimentos",
            atendimento_id,
        )
        if not isinstance(atendimento, Atendimento):
            raise ValueError(f"Atendimento com ID {atendimento_id} não encontrado.")

        try:
            procedimento_id = dados_procedimento["id"]
            tipo_atendimento_id = dados_procedimento["tipo_atendimento_id"]
            descricao = dados_procedimento["descricao"]
            custo = dados_procedimento["custo"]
        except KeyError as erro:
            raise ValueError(
                f"Falta informar o campo obrigatório {erro.args[0]}."
            ) from erro

        if type(procedimento_id) is not int:
            raise ValueError("O ID do procedimento deve ser um número inteiro.")
        if type(tipo_atendimento_id) is not int:
            raise ValueError("O ID do tipo de atendimento deve ser um número inteiro.")
        if self.__repositorio_sistema.buscar_por_id(
            "procedimentos",
            procedimento_id,
        ) is not None:
            raise ValueError(f"Procedimento com ID {procedimento_id} já existe.")

        tipo_atendimento = self.__repositorio_sistema.buscar_por_id(
            "tipos_atendimento",
            tipo_atendimento_id,
        )
        if not isinstance(tipo_atendimento, TipoAtendimento):
            raise ValueError(
                f"Tipo de atendimento com ID {tipo_atendimento_id} não encontrado."
            )

        if (
            not isinstance(custo, (int, float))
            or not isfinite(custo)
            or custo <= 0
        ):
            raise ValueError("O custo do procedimento deve ser maior que zero.")

        procedimento = Procedimento(
            id=procedimento_id,
            descricao=descricao,
            custo=custo,
            tipo_atendimento=tipo_atendimento,
        )
        self.__repositorio_sistema.salvar(procedimento)
        atendimento.vincular_procedimento(procedimento)
        return procedimento

    def alterar(self, id: int, dados: dict | None = None) -> None:
        procedimento = self.__repositorio_sistema.buscar_por_id("procedimentos", id)
        if not isinstance(procedimento, Procedimento):
            raise ValueError(f"Procedimento com ID {id} não encontrado.")

        dados_atualizados = (
            dados
            if dados is not None
            else self.__visao.solicitar_procedimento(id_procedimento=id)
        )

        descricao = dados_atualizados.get("descricao", procedimento.descricao)
        custo = dados_atualizados.get("custo", procedimento.custo)
        tipo_atendimento_id = dados_atualizados.get(
            "tipo_atendimento_id",
            procedimento.tipo_atendimento.id,
        )
        if type(tipo_atendimento_id) is not int:
            raise ValueError("O ID do tipo de atendimento deve ser um número inteiro.")

        tipo_atendimento = self.__repositorio_sistema.buscar_por_id(
            "tipos_atendimento",
            tipo_atendimento_id,
        )
        if not isinstance(tipo_atendimento, TipoAtendimento):
            raise ValueError(
                f"Tipo de atendimento com ID {tipo_atendimento_id} não encontrado."
            )
        if (
            not isinstance(custo, (int, float))
            or not isfinite(custo)
            or custo <= 0
        ):
            raise ValueError("O custo do procedimento deve ser maior que zero.")

        procedimento.descricao = descricao
        procedimento.custo = custo
        procedimento.tipo_atendimento = tipo_atendimento

    def excluir(self, id: int) -> None:
        procedimento = self.__repositorio_sistema.buscar_por_id("procedimentos", id)
        if not isinstance(procedimento, Procedimento):
            raise ValueError(f"Procedimento com ID {id} não encontrado.")

        for atendimento in self.__repositorio_sistema.listar("atendimentos"):
            if procedimento in atendimento.procedimentos:
                atendimento.desvincular_procedimento(procedimento)

        self.__repositorio_sistema.excluir(procedimento)

    def listar(self) -> list:
        return self.__repositorio_sistema.listar("procedimentos")
