from __future__ import annotations

from math import isfinite

from exceptions.erro_cadastro_duplicado import ErroCadastroDuplicado
from exceptions.erro_cadastro_invalido import ErroCadastroInvalido

from entidades.atendimento import Atendimento
from entidades.procedimento import Procedimento
from entidades.profissional import Profissional
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
        if not isinstance(dados_procedimento, dict):
            raise ErroCadastroInvalido("Os dados do procedimento são inválidos.")
        atendimento = self.__repositorio_sistema.buscar_por_id(
            "atendimentos",
            atendimento_id,
        )
        if not isinstance(atendimento, Atendimento):
            raise ValueError(f"Atendimento com ID {atendimento_id} não encontrado.")

        try:
            procedimento_id = dados_procedimento["id"]
            tipo_atendimento_id = dados_procedimento["tipo_atendimento_id"]
            profissional_cpf = dados_procedimento["profissional_responsavel_cpf"]
            descricao = dados_procedimento["descricao"]
            custo = dados_procedimento["custo"]
        except KeyError as erro:
            raise ErroCadastroInvalido(
                f"Falta informar o campo obrigatório {erro.args[0]}."
            ) from erro

        if type(procedimento_id) is not int:
            raise ErroCadastroInvalido(
                "O ID do procedimento deve ser um número inteiro."
            )
        if type(tipo_atendimento_id) is not int:
            raise ErroCadastroInvalido(
                "O ID do tipo de atendimento deve ser um número inteiro."
            )
        if self.__repositorio_sistema.buscar_por_id(
            "procedimentos",
            procedimento_id,
        ) is not None:
            raise ErroCadastroDuplicado(
                f"Procedimento com ID {procedimento_id} já existe."
            )

        tipo_atendimento = self.__repositorio_sistema.buscar_por_id(
            "tipos_atendimento",
            tipo_atendimento_id,
        )
        if not isinstance(tipo_atendimento, TipoAtendimento):
            raise ValueError(
                f"Tipo de atendimento com ID {tipo_atendimento_id} não encontrado."
            )

        profissional = self.__buscar_profissional(profissional_cpf)

        if (
            not isinstance(custo, (int, float))
            or not isfinite(custo)
            or custo <= 0
        ):
            raise ErroCadastroInvalido(
                "O custo do procedimento deve ser maior que zero."
            )

        procedimento = Procedimento(
            id=procedimento_id,
            descricao=descricao,
            custo=custo,
            tipo_atendimento=tipo_atendimento,
            profissional_responsavel=profissional,
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
        if not isinstance(dados_atualizados, dict):
            raise ErroCadastroInvalido("Os dados do procedimento são inválidos.")

        descricao = dados_atualizados.get("descricao", procedimento.descricao)
        custo = dados_atualizados.get("custo", procedimento.custo)
        tipo_atendimento_id = dados_atualizados.get(
            "tipo_atendimento_id",
            procedimento.tipo_atendimento.id,
        )
        profissional_cpf = dados_atualizados.get(
            "profissional_responsavel_cpf",
            procedimento.profissional_responsavel.cpf,
        )
        if type(tipo_atendimento_id) is not int:
            raise ErroCadastroInvalido(
                "O ID do tipo de atendimento deve ser um número inteiro."
            )

        tipo_atendimento = self.__repositorio_sistema.buscar_por_id(
            "tipos_atendimento",
            tipo_atendimento_id,
        )
        if not isinstance(tipo_atendimento, TipoAtendimento):
            raise ValueError(
                f"Tipo de atendimento com ID {tipo_atendimento_id} não encontrado."
            )
        profissional = self.__buscar_profissional(profissional_cpf)
        if (
            not isinstance(custo, (int, float))
            or not isfinite(custo)
            or custo <= 0
        ):
            raise ErroCadastroInvalido(
                "O custo do procedimento deve ser maior que zero."
            )

        procedimento.descricao = descricao
        procedimento.custo = custo
        procedimento.tipo_atendimento = tipo_atendimento
        procedimento.profissional_responsavel = profissional

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

    def listar_profissionais(self) -> list[Profissional]:
        return [
            pessoa
            for pessoa in self.__repositorio_sistema.listar("pessoas")
            if isinstance(pessoa, Profissional)
            and any(
                pessoa in clinica.profissionais
                for clinica in self.__repositorio_sistema.listar("clinicas")
            )
        ]

    def __buscar_profissional(self, cpf: str) -> Profissional:
        profissional = self.__repositorio_sistema.buscar_por_id("pessoas", cpf)
        if not isinstance(profissional, Profissional):
            raise ValueError(
                f"Profissional com CPF {cpf} não encontrado."
            )
        if not any(
            profissional in clinica.profissionais
            for clinica in self.__repositorio_sistema.listar("clinicas")
        ):
            raise ErroCadastroInvalido(
                "O profissional responsável deve estar vinculado a uma clínica."
            )
        return profissional
