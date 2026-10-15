from collections.abc import Callable

from controle.controlador_atendimentos import ControladorAtendimentos
from controle.controlador_clinicas import ControladorClinicas
from controle.controlador_pagamentos import ControladorPagamentos
from controle.controlador_pessoas import ControladorPessoas
from controle.controlador_procedimentos import ControladorProcedimentos
from controle.controlador_relatorios import ControladorRelatorios
from controle.controlador_tipos_atendimento import ControladorTiposAtendimento
from entidades.repositorio_sistema import RepositorioSistema
from exceptions.erro_regra_negocio import ErroRegraNegocio
from limite.visao_atendimentos import VisaoAtendimentos
from limite.visao_cadastros import VisaoCadastros
from limite.visao_principal import VisaoPrincipal


def executar() -> None:
    repositorio = RepositorioSistema()
    visao_principal = VisaoPrincipal()
    visao_cadastros = VisaoCadastros()
    visao_atendimentos = VisaoAtendimentos()

    controladores_cadastros = {
        "clinica": ControladorClinicas(repositorio, visao_cadastros),
        "tipo_atendimento": ControladorTiposAtendimento(repositorio, visao_cadastros),
        "paciente": ControladorPessoas(repositorio, visao_cadastros),
        "profissional": ControladorPessoas(repositorio, visao_cadastros),
        "responsavel_legal": ControladorPessoas(repositorio, visao_cadastros),
        "procedimento": ControladorProcedimentos(repositorio, visao_atendimentos),
    }
    controlador_atendimentos = ControladorAtendimentos(
        repositorio,
        visao_atendimentos,
    )
    controlador_pagamentos = ControladorPagamentos(repositorio)
    controlador_relatorios = ControladorRelatorios(repositorio)

    while True:
        opcao = visao_principal.menu_principal()
        if opcao == 0:
            visao_principal.exibir_mensagem("Até logo.")
            return

        if opcao == 1:
            acao = lambda: __executar_menu_cadastros(
                visao_principal,
                visao_cadastros,
                visao_atendimentos,
                controladores_cadastros,
                controlador_atendimentos,
            )
        elif opcao == 2:
            acao = lambda: __executar_menu_crud(
                visao_principal,
                visao_cadastros,
                "atendimento",
                "Atendimentos",
                controlador_atendimentos,
                visao_atendimentos=visao_atendimentos,
                controlador_atendimentos=controlador_atendimentos,
            )
        elif opcao == 3:
            acao = lambda: __executar_menu_crud(
                visao_principal,
                visao_cadastros,
                "pagamento",
                "Pagamentos",
                controlador_pagamentos,
            )
        else:
            acao = controlador_relatorios.listar
        executar_com_tratamento_de_erros(acao, visao_principal)


def __executar_menu_cadastros(
    visao_principal: VisaoPrincipal,
    visao_cadastros: VisaoCadastros,
    visao_atendimentos: VisaoAtendimentos,
    controladores: dict,
    controlador_atendimentos: ControladorAtendimentos,
) -> None:
    tipos = {
        1: ("clinica", "Clínicas"),
        2: ("tipo_atendimento", "Tipos de atendimento"),
        3: ("paciente", "Pacientes"),
        4: ("profissional", "Profissionais"),
        5: ("responsavel_legal", "Responsáveis legais"),
        6: ("procedimento", "Procedimentos"),
    }

    while True:
        opcao = visao_principal.menu_cadastros()
        if opcao == 0:
            return
        tipo, descricao = tipos[opcao]
        __executar_menu_crud(
            visao_principal,
            visao_cadastros,
            tipo,
            descricao,
            controladores[tipo],
            visao_atendimentos=visao_atendimentos,
            controlador_atendimentos=controlador_atendimentos,
            controlador_clinicas=controladores["clinica"],
        )


def __executar_menu_crud(
    visao_principal: VisaoPrincipal,
    visao_cadastros: VisaoCadastros,
    tipo: str,
    descricao: str,
    controlador: object,
    visao_atendimentos: VisaoAtendimentos | None = None,
    controlador_atendimentos: ControladorAtendimentos | None = None,
    controlador_clinicas: ControladorClinicas | None = None,
) -> None:
    while True:
        opcao = visao_principal.menu_operacoes(descricao)
        if opcao == 0:
            return

        if opcao == 1:
            if tipo == "procedimento":
                if visao_atendimentos is None or controlador_atendimentos is None:
                    raise ValueError("Não foi possível iniciar o cadastro do procedimento.")
                visao_cadastros.exibir_listagem(controlador_atendimentos.listar())
                visao_cadastros.exibir_listagem(controlador.listar_profissionais())
                atendimento_id = visao_principal.solicitar_id("atendimento")
                dados = visao_cadastros.solicitar_dados(tipo=tipo)
                controlador.incluir(atendimento_id, dados)
            elif tipo == "profissional":
                if controlador_clinicas is None:
                    raise ValueError(
                        "Não foi possível listar as clínicas disponíveis."
                    )
                visao_cadastros.exibir_listagem(controlador_clinicas.listar())
                controlador.incluir(visao_cadastros.solicitar_dados(tipo=tipo))
            elif tipo in ("atendimento", "pagamento"):
                controlador.incluir()
            else:
                controlador.incluir(visao_cadastros.solicitar_dados(tipo=tipo))
            visao_principal.exibir_mensagem("Cadastro incluído.")
        elif opcao == 2:
            identificador = visao_principal.solicitar_id(tipo)
            if tipo == "atendimento":
                controlador.alterar(identificador)
            elif tipo == "pagamento":
                controlador.alterar(identificador)
            elif tipo == "procedimento":
                visao_cadastros.exibir_listagem(controlador.listar_profissionais())
                dados = visao_atendimentos.solicitar_procedimento(
                    id_procedimento=identificador
                )
                controlador.alterar(identificador, dados)
            elif tipo in ("paciente", "profissional", "responsavel_legal"):
                controlador.alterar(
                    identificador,
                    visao_cadastros.solicitar_dados_alteracao(tipo),
                )
            else:
                controlador.alterar(
                    identificador,
                    visao_cadastros.solicitar_dados_alteracao(tipo),
                )
            visao_principal.exibir_mensagem("Cadastro alterado.")
        elif opcao == 3:
            identificador = visao_principal.solicitar_id(tipo)
            if tipo == "clinica":
                controlador.excluir(identificador)
            elif tipo == "atendimento":
                controlador.excluir(identificador)
            elif tipo in ("paciente", "profissional", "responsavel_legal"):
                controlador.excluir(identificador)
            else:
                controlador.excluir(identificador)
            visao_principal.exibir_mensagem("Cadastro excluído.")
        elif opcao == 4:
            itens = (
                controlador.listar(tipo)
                if tipo in ("paciente", "profissional", "responsavel_legal")
                else controlador.listar()
            )
            visao_cadastros.exibir_listagem(itens)


def executar_com_tratamento_de_erros(
    acao: Callable[[], object],
    visao: VisaoPrincipal,
) -> bool:
    try:
        acao()
    except (ErroRegraNegocio, ValueError) as erro:
        visao.exibir_mensagem(
            f"Não foi possível concluir a operação: {erro}"
        )
        return False
    return True


if __name__ == "__main__":
    executar()