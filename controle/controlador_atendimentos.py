from __future__ import annotations

from exceptions.erro_cadastro_invalido import ErroCadastroInvalido

from entidades.atendimento import Atendimento
from entidades.paciente import Paciente
from entidades.profissional import Profissional
from entidades.responsavel import ResponsavelLegal
from entidades.repositorio_sistema import RepositorioSistema
from entidades.servico_agendamento import ServicoAgendamento
from entidades.tipo_atendimento import TipoAtendimento
from limite.visao_atendimentos import VisaoAtendimentos


class ControladorAtendimentos:
    def __init__(
        self,
        repositorio_sistema: RepositorioSistema,
        visao: VisaoAtendimentos | None = None,
    ) -> None:
        self.__repositorio_sistema = repositorio_sistema
        self.__servico_agendamento = ServicoAgendamento(repositorio_sistema)
        self.__visao = visao if visao is not None else VisaoAtendimentos()

    def __exibir_opcoes_agendamento(self) -> None:
        self.__visao.exibir_opcoes(
            "Clínicas",
            self.__repositorio_sistema.listar("clinicas")
        )
        self.__visao.exibir_opcoes(
            "Pacientes",
            [
                pessoa
                for pessoa in self.__repositorio_sistema.listar("pessoas")
                if isinstance(pessoa, Paciente)
            ],
        )
        self.__visao.exibir_opcoes(
            "Tipos de atendimento",
            self.__repositorio_sistema.listar("tipos_atendimento"),
        )
        self.__visao.exibir_opcoes(
            "Responsáveis legais",
            [
                pessoa
                for pessoa in self.__repositorio_sistema.listar("pessoas")
                if isinstance(pessoa, ResponsavelLegal)
            ],
        )
        self.__visao.exibir_opcoes(
            "Profissionais",
            [
                pessoa
                for pessoa in self.__repositorio_sistema.listar("pessoas")
                if isinstance(pessoa, Profissional)
            ],
        )

    def incluir(
        self,
        dados: dict | None = None,
    ) -> Atendimento:
        if dados is None:
            self.__exibir_opcoes_agendamento()
            dados_agendamento = self.__visao.solicitar_agendamento()
        else:
            dados_agendamento = dados
        if not isinstance(dados_agendamento, dict):
            raise ErroCadastroInvalido("Os dados do agendamento são inválidos.")
        campos_obrigatorios = {
            "clinica_id",
            "paciente_cpf",
            "tipo_atendimento_id",
            "data",
            "hora_inicio",
            "hora_fim",
            "valor",
        }
        campos_ausentes = campos_obrigatorios - dados_agendamento.keys()
        if campos_ausentes:
            raise ErroCadastroInvalido(
                f"Falta informar o campo obrigatório {sorted(campos_ausentes)[0]}."
            )
        campos_nao_reconhecidos = dados_agendamento.keys() - (
            campos_obrigatorios | {"responsavel_legal_cpf"}
        )
        if campos_nao_reconhecidos:
            raise ErroCadastroInvalido(
                "Os dados do agendamento contêm campos não reconhecidos."
            )
        return self.__servico_agendamento.agendar(**dados_agendamento)

    def alterar(self, id: int, dados: dict | None = None) -> None:
        atendimento_existente = self.__repositorio_sistema.buscar_por_id(
            "atendimentos",
            id,
        )
        if not isinstance(atendimento_existente, Atendimento):
            raise ErroCadastroInvalido(
                f"Atendimento com ID {id} não encontrado."
            )

        if dados is None:
            self.__exibir_opcoes_agendamento()
            dados = self.__visao.solicitar_dados_alteracao()
        if not isinstance(dados, dict):
            raise ErroCadastroInvalido("Os dados do agendamento são inválidos.")

        paciente = self.__repositorio_sistema.buscar_por_id(
            "pessoas",
            dados.get("paciente_cpf", atendimento_existente.paciente.cpf),
        )
        if not isinstance(paciente, Paciente):
            raise ErroCadastroInvalido("O paciente informado não foi encontrado.")

        tipo_atendimento = self.__repositorio_sistema.buscar_por_id(
            "tipos_atendimento",
            dados.get(
                "tipo_atendimento_id",
                atendimento_existente.tipo_atendimento.id,
            ),
        )
        if not isinstance(tipo_atendimento, TipoAtendimento):
            raise ErroCadastroInvalido(
                "O tipo de atendimento informado não foi encontrado."
            )

        responsavel_cpf = dados.get(
            "responsavel_legal_cpf",
            atendimento_existente.responsavel_legal.cpf
            if atendimento_existente.responsavel_legal is not None
            else None,
        )
        responsavel = None
        if responsavel_cpf:
            responsavel = self.__repositorio_sistema.buscar_por_id(
                "pessoas",
                responsavel_cpf,
            )
            if not isinstance(responsavel, ResponsavelLegal):
                raise ErroCadastroInvalido(
                    "O responsável legal informado não foi encontrado."
                )

        atendimento_atualizado = Atendimento(
            id,
            dados.get("data", atendimento_existente.data),
            dados.get("hora_inicio", atendimento_existente.hora_inicio),
            dados.get("hora_fim", atendimento_existente.hora_fim),
            dados.get("valor", atendimento_existente.valor_inicial),
            paciente,
            tipo_atendimento,
            responsavel,
        )
        self.__servico_agendamento.alterar(atendimento_atualizado)

    def excluir(self, id: int | None = None) -> None:
        atendimento_id = (
            id if id is not None else self.__visao.solicitar_id_atendimento()
        )
        atendimento = self.__repositorio_sistema.buscar_por_id(
            "atendimentos",
            atendimento_id,
        )
        if not isinstance(atendimento, Atendimento):
            raise ErroCadastroInvalido(
                f"Atendimento com ID {atendimento_id} não encontrado."
            )
        if any(
            pagamento.atendimento_id == atendimento_id
            for pagamento in self.__repositorio_sistema.listar("pagamentos")
        ):
            raise ErroCadastroInvalido(
                "Não é possível excluir um atendimento que possui pagamentos."
            )

        self.__repositorio_sistema.excluir(atendimento)
        if atendimento.clinica is not None:
            atendimento.clinica.desvincular_atendimento(atendimento)

    def listar(self) -> list:
        return self.__repositorio_sistema.listar("atendimentos")
