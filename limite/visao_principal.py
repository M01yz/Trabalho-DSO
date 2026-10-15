from ._entrada import solicitar_inteiro, solicitar_texto


class VisaoPrincipal:
    def menu_principal(self) -> int:
        print(
            "\n=== Sistema de Gestão ===\n"
            "1. Cadastros\n"
            "2. Atendimentos\n"
            "3. Pagamentos\n"
            "4. Relatórios\n"
            "0. Sair"
        )
        return self.__solicitar_opcao(0, 4)

    def menu_cadastros(self) -> int:
        print(
            "\n=== Cadastros ===\n"
            "1. Clínicas\n"
            "2. Tipos de atendimento\n"
            "3. Pacientes\n"
            "4. Profissionais\n"
            "5. Responsáveis legais\n"
            "6. Procedimentos\n"
            "0. Voltar"
        )
        return self.__solicitar_opcao(0, 6)

    def menu_operacoes(self, descricao: str) -> int:
        print(
            f"\n=== {descricao} ===\n"
            "1. Incluir\n"
            "2. Alterar\n"
            "3. Excluir\n"
            "4. Listar\n"
            "0. Voltar"
        )
        return self.__solicitar_opcao(0, 4)

    def solicitar_id(self, tipo: str) -> int | str:
        if tipo in ("paciente", "profissional", "responsavel_legal"):
            return solicitar_texto("CPF: ")
        return solicitar_inteiro(f"ID de {tipo.replace('_', ' ')}: ")

    def exibir_mensagem(self, mensagem: str) -> None:
        print(mensagem)

    @staticmethod
    def __solicitar_opcao(minimo: int, maximo: int) -> int:
        while True:
            opcao = solicitar_inteiro("Selecione uma opção: ")
            if minimo <= opcao <= maximo:
                return opcao
            print(f"Opção inválida. Selecione um número de {minimo} a {maximo}.")
