from ._entrada import (
    exibir_tabela,
    solicitar_data,
    solicitar_decimal,
    solicitar_hora,
    solicitar_inteiro,
    solicitar_texto,
)
from entidades.horario_funcionamento import DIAS_SEMANA


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

    def solicitar_dados(
        self,
        somente_tipo: bool = False,
        tipo: str | None = None,
    ) -> dict:
        tipos = {
            "1": "clinica",
            "2": "tipo_atendimento",
            "3": "paciente",
            "4": "profissional",
            "5": "responsavel_legal",
            "6": "procedimento",
        }
        if tipo is not None:
            if tipo not in tipos.values():
                raise ValueError(f"Tipo de cadastro inválido: {tipo}.")
        elif somente_tipo:
            tipos = {
                opcao: tipo
                for opcao, tipo in tipos.items()
                if tipo in ("paciente", "profissional", "responsavel_legal")
            }

        if tipo is None:
            print("Tipo de cadastro:")
            for opcao, nome_tipo in tipos.items():
                print(f"{opcao}. {nome_tipo.replace('_', ' ').capitalize()}")

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
                dados["horarios_funcionamento"] = (
                    self.solicitar_horarios_funcionamento()
                )
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
            dados["clinica_id"] = solicitar_inteiro(
                "ID da clínica de atuação: "
            )
        elif tipo == "responsavel_legal":
            dados["nome"] = solicitar_texto("Nome: ")
            dados["cpf"] = solicitar_texto("CPF: ")
            dados["celular"] = solicitar_texto("Celular: ")
        elif tipo == "procedimento":
            dados["tipo_atendimento_id"] = solicitar_inteiro("ID do tipo de atendimento: ")
            dados["profissional_responsavel_cpf"] = solicitar_texto(
                "CPF do profissional responsável: "
            )
            dados["descricao"] = solicitar_texto("Descrição: ")
            dados["custo"] = float(solicitar_decimal("Custo: "))

        return dados

    def solicitar_id(self, tipo: str) -> int | str:
        if tipo in ("paciente", "profissional", "responsavel_legal"):
            return self.solicitar_cpf_pessoa()
        if tipo in (
            "clinica",
            "tipo_atendimento",
            "procedimento",
            "atendimento",
            "pagamento",
        ):
            return solicitar_inteiro(f"ID de {tipo.replace('_', ' ')}: ")
        raise ValueError(f"Tipo de cadastro inválido: {tipo}.")

    def solicitar_dados_alteracao(self, tipo: str) -> dict:
        if tipo == "clinica":
            return {
                "nome": solicitar_texto("Nome: "),
                "cidade": solicitar_texto("Cidade: "),
                "descricao": solicitar_texto("Descrição: "),
                "horarios_funcionamento": self.solicitar_horarios_funcionamento(),
            }
        if tipo == "tipo_atendimento":
            return {
                "nome": solicitar_texto("Nome: "),
                "descricao": solicitar_texto("Descrição: "),
            }
        if tipo in ("paciente", "profissional", "responsavel_legal"):
            dados = {
                "nome": solicitar_texto("Nome: "),
                "celular": solicitar_texto("Celular: "),
            }
            if tipo == "paciente":
                dados["data_nascimento"] = solicitar_data(
                    "Data de nascimento (DD/MM/AAAA): "
                )
            elif tipo == "profissional":
                dados.update(
                    especialidade=solicitar_texto("Especialidade: "),
                    registro_profissional=solicitar_texto("Registro profissional: "),
                )
            return dados
        if tipo == "procedimento":
            return {
                "tipo_atendimento_id": solicitar_inteiro(
                    "ID do tipo de atendimento: "
                ),
                "profissional_responsavel_cpf": solicitar_texto(
                    "CPF do profissional responsável: "
                ),
                "descricao": solicitar_texto("Descrição: "),
                "custo": float(solicitar_decimal("Custo: ")),
            }
        raise ValueError(f"Tipo de cadastro inválido: {tipo}.")

    def solicitar_horarios_funcionamento(self) -> list[dict]:
        horarios = []
        print("Informe se a clínica funciona em cada dia da semana.")

        for dia in DIAS_SEMANA:
            while True:
                resposta = solicitar_texto(
                    f"{dia.capitalize()} (s/n): "
                ).casefold()
                if resposta in ("s", "n"):
                    break
                print("Resposta inválida. Digite s ou n.")

            if resposta == "n":
                continue

            while True:
                abertura = solicitar_hora(
                    f"Horário de abertura ({dia}): "
                )
                fechamento = solicitar_hora(
                    f"Horário de fechamento ({dia}): "
                )
                if abertura < fechamento:
                    break
                print("A abertura deve ocorrer antes do fechamento.")

            horarios.append(
                {
                    "dia_semana": dia,
                    "hora_abertura": abertura,
                    "hora_fechamento": fechamento,
                }
            )

        return horarios

    def exibir_listagem(self, itens: list) -> None:
        exibir_tabela(itens)

    def exibir_mensagem(self, texto: str) -> None:
        print(texto)
