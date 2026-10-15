from entidades.repositorio_sistema import RepositorioSistema
from entidades.servico_relatorios import ServicoRelatorios
from limite.visao_relatorios import VisaoRelatorios


class ControladorRelatorios:
    def __init__(
        self,
        repositorio_sistema: RepositorioSistema,
        visao: VisaoRelatorios | None = None,
        servico_relatorios: ServicoRelatorios | None = None,
    ) -> None:
        self.__visao = visao if visao is not None else VisaoRelatorios()
        self.__servico_relatorios = (
            servico_relatorios
            if servico_relatorios is not None
            else ServicoRelatorios(repositorio_sistema)
        )

    def listar(self) -> list:
        opcao = self.__visao.menu_relatorios()
        relatorios = {
            1: self.listar_clinicas_mais_atendimentos,
            2: self.listar_atendimentos_por_valor,
            3: self.listar_procedimentos_populares,
            4: self.listar_procedimentos_por_custo,
        }
        try:
            return relatorios[opcao]()
        except KeyError as erro:
            raise ValueError(f"Opção de relatório inválida: {opcao}.") from erro

    def listar_clinicas_mais_atendimentos(self) -> list:
        relatorio = self.__servico_relatorios.clinicas_mais_atendimentos()
        self.__visao.exibir_tabela(relatorio)
        return relatorio

    def listar_atendimentos_por_valor(self) -> list:
        relatorio = self.__servico_relatorios.atendimentos_por_valor()
        self.__visao.exibir_tabela(relatorio)
        return relatorio

    def listar_procedimentos_populares(self) -> list:
        relatorio = self.__servico_relatorios.procedimentos_mais_realizados()
        self.__visao.exibir_tabela(relatorio)
        return relatorio

    def listar_procedimentos_por_custo(self) -> list:
        relatorio = self.__servico_relatorios.procedimentos_por_custo()
        self.__visao.exibir_tabela(relatorio)
        return relatorio
