from ._entrada import exibir_tabela, solicitar_data, solicitar_decimal, solicitar_inteiro, solicitar_texto


class VisaoCadastros:
    def menu_cadastros(self) -> None:
        print(
            "\n=== Cadastros ===\n"
            "1. Clínica\n"
            "2. Tipo de atendimento\n"
            "3. Paciente\n"
            "4. Profissional\n"
            "5. Responsável legal\n"
            "6. Procedimento"
        )

    def solicitar_id_clinica(self) -> int:
        return solicitar_inteiro("ID da clínica: ")

    def solicitar_cpf_pessoa(self) -> str:
        return solicitar_texto("CPF da pessoa: ")

    def solicitar_dados_pessoa(self) -> dict:
        return {
            "nome": solicitar_texto("Nome: "),
            "celular": solicitar_texto("Celular: "),
        }

    def solicitar_dados(self, somente_tipo: bool = False) -> dict:
        tipos = {
            "1": "clinica",
            "2": "tipo_atendimento",
            "3": "paciente",
            "4": "profissional",
            "5": "responsavel_legal",
            "6": "procedimento",
        }
        if somente_tipo:
            tipos = {
                opcao: tipo
                for opcao, tipo in tipos.items()
                if tipo in ("paciente", "profissional", "responsavel_legal")
            }

        print("Tipo de cadastro:")
        for opcao, tipo in tipos.items():
            print(f"{opcao}. {tipo.replace('_', ' ').capitalize()}")

        while True:
            opcao = input("Selecione uma opção: ").strip()
            if opcao in tipos:
                break
            print("Opção inválida. Selecione um dos tipos listados.")

        tipo = tipos[opcao]
        dados: dict = {"tipo": tipo}
        if somente_tipo:
            return dados

        if tipo in ("clinica", "tipo_atendimento", "procedimento"):
            dados["id"] = solicitar_inteiro("ID: ")
        if tipo in ("clinica", "tipo_atendimento"):
            dados["nome"] = solicitar_texto("Nome: ")
            dados["descricao"] = solicitar_texto("Descrição: ")
            if tipo == "clinica":
                dados["cidade"] = solicitar_texto("Cidade: ")
        elif tipo == "paciente":
            dados["data_nascimento"] = solicitar_data("Data de nascimento (DD/MM/AAAA): ")
            dados["nome"] = solicitar_texto("Nome: ")
            dados["cpf"] = solicitar_texto("CPF: ")
            dados["celular"] = solicitar_texto("Celular: ")
        elif tipo == "profissional":
            dados["nome"] = solicitar_texto("Nome: ")
            dados["cpf"] = solicitar_texto("CPF: ")
            dados["celular"] = solicitar_texto("Celular: ")
            dados["especialidade"] = solicitar_texto("Especialidade: ")
            dados["registro_profissional"] = solicitar_texto("Registro profissional: ")
        elif tipo == "responsavel_legal":
            dados["nome"] = solicitar_texto("Nome: ")
            dados["cpf"] = solicitar_texto("CPF: ")
            dados["celular"] = solicitar_texto("Celular: ")
        elif tipo == "procedimento":
            dados["tipo_atendimento_id"] = solicitar_inteiro("ID do tipo de atendimento: ")
            dados["descricao"] = solicitar_texto("Descrição: ")
            dados["custo"] = float(solicitar_decimal("Custo: "))

        return dados

    def exibir_listagem(self, itens: list) -> None:
        exibir_tabela(itens)

    def exibir_mensagem(self, texto: str) -> None:
        print(texto)
