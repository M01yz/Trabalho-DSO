from entidades.procedimento import Procedimento
from entidades.profissional import Profissional
from entidades.repositorio_sistema import RepositorioSistema
from entidades.servico_procedimentos import ServicoProcedimentos
from limite.visao_atendimentos import VisaoAtendimentos


class ControladorProcedimentos:
    def __init__(
        self,
        repositorio_sistema: RepositorioSistema,
        visao: VisaoAtendimentos | None = None,
        servico: ServicoProcedimentos | None = None,
    ) -> None:
        self.__visao = visao if visao is not None else VisaoAtendimentos()
        self.__servico = servico or ServicoProcedimentos(repositorio_sistema)

    def incluir(
        self,
        atendimento_id: int,
        dados: dict | None = None,
    ) -> Procedimento:
        dados_procedimento = (
            dados if dados is not None else self.__visao.solicitar_procedimento()
        )
        return self.__servico.incluir(atendimento_id, dados_procedimento)

    def alterar(self, procedimento_id: int, dados: dict | None = None) -> None:
        dados_atualizados = (
            dados
            if dados is not None
            else self.__visao.solicitar_procedimento(
                id_procedimento=procedimento_id
            )
        )
        self.__servico.alterar(procedimento_id, dados_atualizados)

    def excluir(self, procedimento_id: int) -> None:
        self.__servico.excluir(procedimento_id)

    def listar(self) -> list[Procedimento]:
        return self.__servico.listar()

    def listar_profissionais(self) -> list[Profissional]:
        return self.__servico.listar_profissionais()
