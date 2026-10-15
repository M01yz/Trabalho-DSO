from ._entrada import exibir_tabela, solicitar_inteiro


class VisaoRelatorios:
    def menu_relatorios(self) -> int:
        print(
            "\n=== Relatórios ===\n"
            "1. Clínicas com mais atendimentos\n"
            "2. Atendimentos por valor\n"
            "3. Procedimentos mais populares\n"
            "4. Procedimentos por custo"
        )
        while True:
            opcao = solicitar_inteiro("Selecione um relatório: ")
            if 1 <= opcao <= 4:
                return opcao
            print("Opção inválida. Selecione um número de 1 a 4.")

    def exibir_tabela(self, dados: list) -> None:
        exibir_tabela(dados)
