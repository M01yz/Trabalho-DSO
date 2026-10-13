from decimal import Decimal

from ._entrada import exibir_tabela, solicitar_data, solicitar_decimal, solicitar_inteiro, solicitar_texto


class VisaoPagamentos:
    def solicitar_pagamento(self) -> dict:
        modalidades = {
            "1": "dinheiro",
            "2": "pix",
            "3": "cartao",
        }
        print("Modalidade do pagamento:")
        for opcao, modalidade in modalidades.items():
            print(f"{opcao}. {modalidade.capitalize()}")

        while True:
            opcao = input("Selecione uma opção: ").strip()
            if opcao in modalidades:
                break
            print("Opção inválida. Selecione dinheiro, Pix ou cartão.")

        modalidade = modalidades[opcao]
        dados = {
            "modalidade": modalidade,
            "id": solicitar_inteiro("ID do pagamento: "),
            "data_pagamento": solicitar_data("Data do pagamento (DD/MM/AAAA): "),
            "valor_pago": float(solicitar_decimal("Valor pago: ")),
        }

        if modalidade == "pix":
            dados["cpf_pagador"] = solicitar_texto("CPF do pagador: ")
        elif modalidade == "cartao":
            dados["numero_cartao"] = solicitar_texto("Número do cartão: ")
            dados["bandeira"] = solicitar_texto("Bandeira: ")

        return dados

    def exibir_saldo(self, valor: Decimal) -> None:
        print(f"Saldo restante: R$ {valor:.2f}")

    def exibir_pagamentos(self, itens: list) -> None:
        exibir_tabela(itens)
