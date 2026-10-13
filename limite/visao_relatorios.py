from ._entrada import exibir_tabela


class VisaoRelatorios:
    def menu_relatorios(self) -> None:
        print(
            "\n=== Relatórios ===\n"
            "1. Clínicas com mais atendimentos\n"
            "2. Atendimentos por valor\n"
            "3. Procedimentos mais populares\n"
            "4. Procedimentos por custo"
        )

    def exibir_tabela(self, dados: list) -> None:
        exibir_tabela(dados)
