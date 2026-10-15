from __future__ import annotations

from entidades.atendimento import Atendimento
from entidades.repositorio_sistema import RepositorioSistema
from entidades.servico_agendamento import ServicoAgendamento
from limite.visao_atendimentos import VisaoAtendimentos


class ControladorAtendimentos:
    def __init__(
        self,
        repositorio_sistema: RepositorioSistema,
        visao: VisaoAtendimentos | None = None,
    ) -> None:
        self.__repositorio_sistema = repositorio_sistema
        self.__servico_agendamento = ServicoAgendamento(repositorio_sistema)
        self.__visao = visao if visao is not None else VisaoAtendimentos()

    def incluir(
        self,
        dados: dict | None = None,
    ) -> Atendimento:
        dados_agendamento = (
            dados if dados is not None else self.__visao.solicitar_agendamento()
        )
        return self.__servico_agendamento.agendar(**dados_agendamento)

    def alterar(self, id: int, dados: dict | None = None) -> None:
        atendimento_existente = self.__repositorio_sistema.buscar_por_id(
            "atendimentos",
            id,
        )
        if not isinstance(atendimento_existente, Atendimento):
            raise ValueError(f"Atendimento com ID {id} não encontrado.")

        dados = (
            dados
            if dados is not None
            else self.__visao.solicitar_dados_alteracao()
        )
        atendimento_atualizado = Atendimento(
            id,
            dados.get("data", atendimento_existente.data),
            dados.get("hora_inicio", atendimento_existente.hora_inicio),
            dados.get("hora_fim", atendimento_existente.hora_fim),
            dados.get("valor", atendimento_existente.valor_inicial),
        )
        self.__servico_agendamento.alterar(atendimento_atualizado)

    def excluir(self, id: int | None = None) -> None:
        atendimento_id = (
            id if id is not None else self.__visao.solicitar_id_atendimento()
        )
        atendimento = self.__repositorio_sistema.buscar_por_id(
            "atendimentos",
            atendimento_id,
        )
        if not isinstance(atendimento, Atendimento):
            raise ValueError(f"Atendimento com ID {atendimento_id} não encontrado.")

        self.__repositorio_sistema.excluir(atendimento)
        if atendimento.clinica is not None:
            atendimento.clinica.desvincular_atendimento(atendimento)

    def listar(self) -> list:
        return self.__repositorio_sistema.listar("atendimentos")
