from ._entrada import (
    exibir_tabela,
    solicitar_data,
    solicitar_decimal,
    solicitar_hora,
    solicitar_inteiro,
    solicitar_texto,
    solicitar_texto_opcional,
)


class VisaoAtendimentos:
    def menu_atendimentos(self) -> int:
        print(
            "\n=== Atendimentos ===\n"
            "1. Agendar/modificar atendimento\n"
            "2. Incluir/modificar procedimento\n"
            "3. Listar atendimentos"
        )
        while True:
            opcao = solicitar_inteiro("Escolha uma opção: ")
            if 1 <= opcao <= 3:
                return opcao
            print("Opção inválida. Escolha uma opção de 1 a 3.")

    def solicitar_agendamento(self) -> dict:
        return {
            "clinica_id": solicitar_inteiro("ID da clínica: "),
            "paciente_cpf": solicitar_texto("CPF do paciente: "),
            "tipo_atendimento_id": solicitar_inteiro(
                "ID do tipo de atendimento: "
            ),
            "responsavel_legal_cpf": solicitar_texto_opcional(
                "CPF do responsável legal (deixe vazio se não houver): "
            ),
            "data": solicitar_data("Data (DD/MM/AAAA): "),
            "hora_inicio": solicitar_hora("Horário de início (HH:MM): "),
            "hora_fim": solicitar_hora("Horário de término (HH:MM): "),
            "valor": float(solicitar_decimal("Valor: ")),
        }

    def solicitar_dados_alteracao(self) -> dict:
        return {
            "paciente_cpf": solicitar_texto("CPF do paciente: "),
            "tipo_atendimento_id": solicitar_inteiro(
                "ID do tipo de atendimento: "
            ),
            "responsavel_legal_cpf": solicitar_texto_opcional(
                "CPF do responsável legal (deixe vazio se não houver): "
            ),
            "data": solicitar_data("Data (DD/MM/AAAA): "),
            "hora_inicio": solicitar_hora("Horário de início (HH:MM): "),
            "hora_fim": solicitar_hora("Horário de término (HH:MM): "),
            "valor": float(solicitar_decimal("Valor: ")),
        }

    def solicitar_id_atendimento(self) -> int:
        return solicitar_inteiro("ID do atendimento: ")

    def solicitar_procedimento(self, id_procedimento: int | None = None) -> dict:
        return {
            "id": (
                id_procedimento
                if id_procedimento is not None
                else solicitar_inteiro("ID do procedimento: ")
            ),
            "tipo_atendimento_id": solicitar_inteiro("ID do tipo de atendimento: "),
            "profissional_responsavel_cpf": solicitar_texto(
                "CPF do profissional responsável: "
            ),
            "descricao": solicitar_texto("Descrição do procedimento: "),
            "custo": float(solicitar_decimal("Custo: ")),
        }

    def exibir_atendimentos(self, itens: list) -> None:
        exibir_tabela(itens)

    def exibir_opcoes(self, titulo: str, itens: list) -> None:
        print(f"\n{titulo}:")
        exibir_tabela(itens)

    def exibir_procedimentos(self, itens: list) -> None:
        exibir_tabela(itens)
