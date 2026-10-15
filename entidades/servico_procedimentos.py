from __future__ import annotations

from math import isfinite

from exceptions.erro_cadastro_invalido import ErroCadastroInvalido
from exceptions.erro_pagamento_invalido import ErroPagamentoInvalido

from .atendimento import Atendimento
from .procedimento import Procedimento
from .profissional import Profissional
from .repositorio_sistema import RepositorioSistema
from .tipo_atendimento import TipoAtendimento


class ServicoProcedimentos:
    def __init__(self, repositorio_sistema: RepositorioSistema) -> None:
        self.__repositorio_sistema = repositorio_sistema

    def incluir(self, atendimento_id: int, dados: dict) -> Procedimento:
        if not isinstance(dados, dict):
            raise ErroCadastroInvalido("Os dados do procedimento são inválidos.")

        atendimento = self.__buscar_atendimento(atendimento_id)
        procedimento_id = dados.get("id")
        if type(procedimento_id) is not int:
            raise ErroCadastroInvalido(
                "O ID do procedimento deve ser um número inteiro."
            )
        tipo_atendimento = self.__buscar_tipo_atendimento(
            dados.get("tipo_atendimento_id")
        )
        profissional = self.__buscar_profissional(
            dados.get("profissional_responsavel_cpf")
        )
        descricao = self.__validar_descricao(dados.get("descricao"))
        custo = self.__validar_custo(dados.get("custo"))

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

    def alterar(self, procedimento_id: int, dados: dict) -> None:
        if not isinstance(dados, dict):
            raise ErroCadastroInvalido("Os dados do procedimento são inválidos.")

        procedimento = self.__repositorio_sistema.buscar_por_id(
            "procedimentos",
            procedimento_id,
        )
        if not isinstance(procedimento, Procedimento):
            raise ErroCadastroInvalido(
                f"Procedimento com ID {procedimento_id} não encontrado."
            )

        descricao = self.__validar_descricao(
            dados.get("descricao", procedimento.descricao)
        )
        custo = self.__validar_custo(dados.get("custo", procedimento.custo))
        tipo_atendimento = self.__buscar_tipo_atendimento(
            dados.get(
                "tipo_atendimento_id",
                procedimento.tipo_atendimento.id,
            )
        )
        profissional = self.__buscar_profissional(
            dados.get(
                "profissional_responsavel_cpf",
                procedimento.profissional_responsavel.cpf,
            )
        )

        atendimentos_vinculados = [
            atendimento
            for atendimento in self.__repositorio_sistema.listar("atendimentos")
            if procedimento in atendimento.procedimentos
        ]
        if any(
            atendimento.valor - procedimento.custo + custo
            < atendimento.total_pago()
            for atendimento in atendimentos_vinculados
        ):
            raise ErroPagamentoInvalido(
                "Não é possível reduzir o custo do procedimento: o total pago "
                "ficaria acima do valor atualizado de um atendimento."
            )

        procedimento.descricao = descricao
        procedimento.custo = custo
        procedimento.tipo_atendimento = tipo_atendimento
        procedimento.profissional_responsavel = profissional

    def excluir(self, procedimento_id: int) -> None:
        procedimento = self.__repositorio_sistema.buscar_por_id(
            "procedimentos",
            procedimento_id,
        )
        if not isinstance(procedimento, Procedimento):
            raise ErroCadastroInvalido(
                f"Procedimento com ID {procedimento_id} não encontrado."
            )

        atendimentos_vinculados = [
            atendimento
            for atendimento in self.__repositorio_sistema.listar("atendimentos")
            if procedimento in atendimento.procedimentos
        ]
        if any(
            atendimento.valor - procedimento.custo < atendimento.total_pago()
            for atendimento in atendimentos_vinculados
        ):
            raise ErroPagamentoInvalido(
                "Não é possível excluir o procedimento: o total pago "
                "ficaria acima do valor atualizado de um atendimento."
            )

        for atendimento in atendimentos_vinculados:
            atendimento.desvincular_procedimento(procedimento)
        self.__repositorio_sistema.excluir(procedimento)

    def listar(self) -> list[Procedimento]:
        return self.__repositorio_sistema.listar("procedimentos")

    def listar_profissionais(self) -> list[Profissional]:
        clinicas = self.__repositorio_sistema.listar("clinicas")
        return [
            pessoa
            for pessoa in self.__repositorio_sistema.listar("pessoas")
            if isinstance(pessoa, Profissional)
            and any(pessoa in clinica.profissionais for clinica in clinicas)
        ]

    def __buscar_atendimento(self, atendimento_id: int) -> Atendimento:
        atendimento = self.__repositorio_sistema.buscar_por_id(
            "atendimentos",
            atendimento_id,
        )
        if not isinstance(atendimento, Atendimento):
            raise ErroCadastroInvalido(
                f"Atendimento com ID {atendimento_id} não encontrado."
            )
        return atendimento

    def __buscar_tipo_atendimento(self, tipo_id: object) -> TipoAtendimento:
        if type(tipo_id) is not int:
            raise ErroCadastroInvalido(
                "O ID do tipo de atendimento deve ser um número inteiro."
            )
        tipo = self.__repositorio_sistema.buscar_por_id(
            "tipos_atendimento",
            tipo_id,
        )
        if not isinstance(tipo, TipoAtendimento):
            raise ErroCadastroInvalido(
                f"Tipo de atendimento com ID {tipo_id} não encontrado."
            )
        return tipo

    def __buscar_profissional(self, cpf: object) -> Profissional:
        if not isinstance(cpf, str) or not cpf:
            raise ErroCadastroInvalido(
                "O CPF do profissional responsável deve ser informado."
            )
        profissional = self.__repositorio_sistema.buscar_por_id("pessoas", cpf)
        if not isinstance(profissional, Profissional):
            raise ErroCadastroInvalido(
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

    @staticmethod
    def __validar_descricao(descricao: object) -> str:
        if not isinstance(descricao, str) or not descricao.strip():
            raise ErroCadastroInvalido(
                "A descrição do procedimento não pode ficar vazia."
            )
        return descricao.strip()

    @staticmethod
    def __validar_custo(custo: object) -> float:
        if (
            not isinstance(custo, (int, float))
            or isinstance(custo, bool)
            or not isfinite(custo)
            or custo <= 0
        ):
            raise ErroCadastroInvalido(
                "O custo do procedimento deve ser maior que zero."
            )
        return float(custo)
