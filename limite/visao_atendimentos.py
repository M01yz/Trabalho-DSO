from ._entrada import exibir_tabela, solicitar_data, solicitar_decimal, solicitar_hora, solicitar_inteiro, solicitar_texto


class VisaoAtendimentos:
    def menu_atendimentos(self) -> None:
        print(
            "\n=== Atendimentos ===\n"
            "1. Agendar atendimento\n"
            "2. Incluir procedimento\n"
            "3. Listar atendimentos"
        )

    def solicitar_agendamento(self) -> dict:
        return {
            "clinica_id": solicitar_inteiro("ID da clínica: "),
            "data": solicitar_data("Data (DD/MM/AAAA): "),
            "hora_inicio": solicitar_hora("Horário de início (HH:MM): "),
            "hora_fim": solicitar_hora("Horário de término (HH:MM): "),
            "valor": float(solicitar_decimal("Valor: ")),
        }

    def solicitar_procedimento(self) -> dict:
        return {
            "id": solicitar_inteiro("ID do procedimento: "),
            "descricao": solicitar_texto("Descrição do procedimento: "),
            "custo": float(solicitar_decimal("Custo: ")),
        }

    def exibir_atendimentos(self, itens: list) -> None:
        exibir_tabela(itens)
