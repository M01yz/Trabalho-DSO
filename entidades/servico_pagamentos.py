from math import isfinite

from exceptions.erro_cadastro_duplicado import ErroCadastroDuplicado
from exceptions.erro_pagamento_invalido import ErroPagamentoInvalido
from limite.visao_pagamentos import VisaoPagamentos

from .atendimento import Atendimento
from .pagamento import Pagamento
from .pagamento_cartao import PagamentoCartao
from .pagamento_dinheiro import PagamentoDinheiro
from .pagamento_pix import PagamentoPix
from .repositorio_sistema import RepositorioSistema


class ServicoPagamentos:
    def __init__(
        self,
        repositorio_sistema: RepositorioSistema,
        visao_pagamentos: VisaoPagamentos,
    ):
        self.__repositorio_sistema = repositorio_sistema
        self.__visao_pagamentos = visao_pagamentos

    def registrar(self) -> Pagamento:
        dados = self.__visao_pagamentos.solicitar_pagamento()
        try:
            modalidade = dados["modalidade"]
            atendimento_id = dados["atendimento_id"]
            id_pagamento = dados["id"]
            data_pagamento = dados["data_pagamento"]
            valor_pago = dados["valor_pago"]
            parcelas = dados["parcelas"]
        except KeyError as erro:
            raise ErroPagamentoInvalido(
                f"Falta informar o campo obrigatório {erro.args[0]}."
            ) from erro

        if type(parcelas) is not int or not 1 <= parcelas <= 3:
            raise ErroPagamentoInvalido("O pagamento deve ter entre 1 e 3 parcelas.")
        if type(id_pagamento) is not int:
            raise ErroPagamentoInvalido("O ID do pagamento deve ser um número inteiro.")
        if type(atendimento_id) is not int:
            raise ErroPagamentoInvalido("O ID do atendimento deve ser um número inteiro.")
        if not isinstance(valor_pago, (int, float)) or not isfinite(valor_pago) or valor_pago <= 0:
            raise ErroPagamentoInvalido("O valor do pagamento deve ser maior que zero.")

        atendimento = self.__repositorio_sistema.buscar_por_id("atendimentos", atendimento_id)
        if not isinstance(atendimento, Atendimento):
            raise ErroPagamentoInvalido(f"Atendimento com ID {atendimento_id} não encontrado.")

        if self.__repositorio_sistema.buscar_por_id("pagamentos", id_pagamento) is not None:
            raise ErroCadastroDuplicado(f"Já existe um pagamento com o ID {id_pagamento}.")

        if modalidade == "dinheiro":
            pagamento = PagamentoDinheiro(
                id_pagamento,
                data_pagamento,
                valor_pago,
                parcelas,
                atendimento_id,
            )
        elif modalidade == "pix":
            try:
                cpf_pagador = dados["cpf_pagador"]
            except KeyError as erro:
                raise ErroPagamentoInvalido("Falta informar o CPF do pagador.") from erro
            pagamento = PagamentoPix(
                id_pagamento,
                data_pagamento,
                valor_pago,
                cpf_pagador,
                parcelas,
                atendimento_id,
            )
        elif modalidade == "cartao":
            try:
                numero_cartao = dados["numero_cartao"]
                bandeira = dados["bandeira"]
            except KeyError as erro:
                raise ErroPagamentoInvalido(
                    f"Falta informar o campo obrigatório {erro.args[0]}."
                ) from erro
            pagamento = PagamentoCartao(
                id_pagamento,
                data_pagamento,
                valor_pago,
                numero_cartao,
                bandeira,
                parcelas,
                atendimento_id,
            )
        else:
            raise ErroPagamentoInvalido(f"Modalidade de pagamento inválida: {modalidade}.")

        self.validar_pagamento(pagamento)
        try:
            atendimento.vincular_pagamento(pagamento)
        except ValueError as erro:
            raise ErroPagamentoInvalido(str(erro)) from erro
        self.__repositorio_sistema.salvar(pagamento)
        return pagamento

    def alterar(self, pagamento: Pagamento) -> None:
        pagamento_existente = self.__repositorio_sistema.buscar_por_id(
            "pagamentos",
            pagamento.id,
        )
        if not isinstance(pagamento_existente, Pagamento):
            raise ErroPagamentoInvalido(f"Pagamento com ID {pagamento.id} não encontrado.")

        atendimento_id = pagamento.atendimento_id
        if atendimento_id is None:
            atendimento_id = pagamento_existente.atendimento_id
        if type(atendimento_id) is not int:
            raise ErroPagamentoInvalido("O ID do atendimento deve ser um número inteiro.")
        atendimento_novo = self.__repositorio_sistema.buscar_por_id(
            "atendimentos",
            atendimento_id,
        )
        if not isinstance(atendimento_novo, Atendimento):
            raise ErroPagamentoInvalido(f"Atendimento com ID {atendimento_id} não encontrado.")

        pagamento.id = pagamento_existente.id
        pagamento.atendimento_id = atendimento_id
        self.validar_pagamento(pagamento)

        atendimento_atual = None
        if pagamento_existente.atendimento_id is not None:
            atendimento_atual = self.__repositorio_sistema.buscar_por_id(
                "atendimentos",
                pagamento_existente.atendimento_id,
            )

        pagamentos_novos = (
            pagamento.valor_pago
            + sum(
                item.valor_pago
                for item in atendimento_novo.pagamentos
                if item is not pagamento_existente
            )
        )
        if pagamentos_novos > atendimento_novo.valor:
            raise ErroPagamentoInvalido(
                "O total pago não pode ultrapassar o valor do atendimento."
            )

        if isinstance(atendimento_atual, Atendimento):
            atendimento_atual.desvincular_pagamento(pagamento_existente)
        atendimento_novo.vincular_pagamento(pagamento)

        pagamentos = self.__repositorio_sistema.listar("pagamentos")
        indice = next(
            indice
            for indice, item in enumerate(pagamentos)
            if item is pagamento_existente
        )
        pagamentos[indice] = pagamento

    def excluir(self, id: int) -> None:
        pagamento = self.__repositorio_sistema.buscar_por_id("pagamentos", id)
        if not isinstance(pagamento, Pagamento):
            raise ErroPagamentoInvalido(f"Pagamento com ID {id} não encontrado.")

        if pagamento.atendimento_id is not None:
            atendimento = self.__repositorio_sistema.buscar_por_id(
                "atendimentos",
                pagamento.atendimento_id,
            )
            if isinstance(atendimento, Atendimento) and pagamento in atendimento.pagamentos:
                atendimento.desvincular_pagamento(pagamento)
        self.__repositorio_sistema.excluir(pagamento)

    def listar(self) -> list:
        return self.__repositorio_sistema.listar("pagamentos")

    def validar_pagamento(self, pagamento: Pagamento) -> None:
        if type(pagamento.parcelas) is not int or not 1 <= pagamento.parcelas <= 3:
            raise ErroPagamentoInvalido("O pagamento deve ter entre 1 e 3 parcelas.")
        if (
            not isinstance(pagamento.valor_pago, (int, float))
            or not isfinite(pagamento.valor_pago)
            or pagamento.valor_pago <= 0
        ):
            raise ErroPagamentoInvalido("O valor do pagamento deve ser maior que zero.")
        pagamento.validar_modalidade()
