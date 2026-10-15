from __future__ import annotations

from entidades.pagamento import Pagamento
from entidades.repositorio_sistema import RepositorioSistema
from entidades.servico_pagamentos import ServicoPagamentos
from limite.visao_pagamentos import VisaoPagamentos


class ControladorPagamentos:
    def __init__(
        self,
        repositorio_sistema: RepositorioSistema,
        visao: VisaoPagamentos | None = None,
        servico_pagamentos: ServicoPagamentos | None = None,
    ) -> None:
        self.__visao = visao if visao is not None else VisaoPagamentos()
        self.__servico_pagamentos = (
            servico_pagamentos
            if servico_pagamentos is not None
            else ServicoPagamentos(repositorio_sistema)
        )

    def incluir(self, dados: dict | None = None) -> Pagamento:
        dados_pagamento = (
            dados if dados is not None else self.__visao.solicitar_pagamento()
        )
        return self.__servico_pagamentos.registrar(dados_pagamento)

    def alterar(self, id: int, dados: dict | None = None) -> None:
        dados_pagamento = (
            dict(dados)
            if dados is not None
            else self.__visao.solicitar_pagamento(id_pagamento=id)
        )
        dados_pagamento["id"] = id
        self.__servico_pagamentos.alterar(id, dados_pagamento)

    def excluir(self, id: int) -> None:
        self.__servico_pagamentos.excluir(id)

    def listar(self) -> list:
        pagamentos = self.__servico_pagamentos.listar()
        self.__visao.exibir_pagamentos(pagamentos)
        return pagamentos
