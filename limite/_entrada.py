from datetime import date, datetime, time
from decimal import Decimal, InvalidOperation
from typing import Callable, TypeVar


T = TypeVar("T")


def solicitar_texto(mensagem: str) -> str:
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("O valor não pode ficar vazio.")


def solicitar_valor(mensagem: str, conversor: Callable[[str], T], formato: str) -> T:
    while True:
        valor = input(mensagem).strip()
        try:
            return conversor(valor)
        except (ValueError, InvalidOperation):
            print(f"Entrada inválida. Informe {formato}.")


def solicitar_inteiro(mensagem: str) -> int:
    return solicitar_valor(mensagem, int, "um número inteiro")


def solicitar_data(mensagem: str) -> date:
    return solicitar_valor(
        mensagem,
        lambda valor: datetime.strptime(valor, "%d/%m/%Y").date(),
        "uma data no formato DD/MM/AAAA",
    )


def solicitar_hora(mensagem: str) -> time:
    return solicitar_valor(mensagem, time.fromisoformat, "um horário no formato HH:MM")


def solicitar_decimal(mensagem: str) -> Decimal:
    return solicitar_valor(
        mensagem,
        lambda valor: Decimal(valor.replace(",", ".")),
        "um valor numérico",
    )


def exibir_tabela(itens: list) -> None:
    if not itens:
        print("Nenhum item encontrado.")
        return

    campos_conhecidos = (
        "id",
        "nome",
        "cpf",
        "celular",
        "data_nascimento",
        "especialidade",
        "registro_profissional",
        "cidade",
        "descricao",
        "custo",
        "data",
        "hora_inicio",
        "hora_fim",
        "valor",
        "data_pagamento",
        "valor_pago",
        "cpf_pagador",
        "numero_cartao",
        "bandeira",
    )
    linhas = []
    colunas = []

    for item in itens:
        if isinstance(item, dict):
            linha = item
        else:
            linha = {
                campo: getattr(item, campo)
                for campo in campos_conhecidos
                if hasattr(item, campo)
            }

        for coluna in linha:
            if coluna not in colunas:
                colunas.append(coluna)
        linhas.append(linha)

    larguras = {
        coluna: max(
            len(coluna),
            *(len(str(linha.get(coluna, ""))) for linha in linhas),
        )
        for coluna in colunas
    }
    cabecalho = " | ".join(coluna.ljust(larguras[coluna]) for coluna in colunas)
    separador = "-+-".join("-" * larguras[coluna] for coluna in colunas)
    print(cabecalho)
    print(separador)
    for linha in linhas:
        print(" | ".join(str(linha.get(coluna, "")).ljust(larguras[coluna]) for coluna in colunas))
