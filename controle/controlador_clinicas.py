from __future__ import annotations

from exceptions.erro_cadastro_duplicado import ErroCadastroDuplicado
from exceptions.erro_cadastro_invalido import ErroCadastroInvalido
from exceptions.erro_horario_invalido import ErroHorarioInvalido

from entidades.clinica import Clinica
from entidades.horario_funcionamento import HorarioFuncionamento
from entidades.repositorio_sistema import RepositorioSistema
from limite.visao_cadastros import VisaoCadastros


class ControladorClinicas:
    def __init__(
        self,
        repositorio_sistema: RepositorioSistema,
        visao: VisaoCadastros | None = None,
    ) -> None:
        self.__repositorio_sistema = repositorio_sistema
        self.__visao = visao if visao is not None else VisaoCadastros()

    def incluir(self, dados: dict | None = None) -> Clinica:
        dados_clinica = (
            dados
            if dados is not None
            else self.__visao.solicitar_dados(tipo="clinica")
        )
        if not isinstance(dados_clinica, dict):
            raise ErroCadastroInvalido("Os dados da clínica são inválidos.")
        if dados_clinica.get("tipo") not in (None, "clinica"):
            raise ErroCadastroInvalido(
                "Este controlador só pode incluir cadastros de clínica."
            )
        clinica_id = dados_clinica.get("id")
        if type(clinica_id) is not int:
            raise ErroCadastroInvalido("O ID da clínica deve ser um número inteiro.")
        if self.__repositorio_sistema.buscar_por_id("clinicas", clinica_id) is not None:
            raise ErroCadastroDuplicado(
                f"Já existe uma clínica com o ID {clinica_id}."
            )

        clinica = Clinica(
            id=clinica_id,
            nome=dados_clinica["nome"],
            cidade=dados_clinica["cidade"],
            descricao=dados_clinica["descricao"],
        )
        if "horarios_funcionamento" in dados_clinica:
            clinica.horarios_funcionamento = self.__converter_horarios(
                dados_clinica["horarios_funcionamento"]
            )
        self.__repositorio_sistema.salvar(clinica)
        return clinica

    def alterar(self, id: int, dados: dict) -> None:
        clinica = self.__repositorio_sistema.buscar_por_id("clinicas", id)
        if not isinstance(clinica, Clinica):
            raise ValueError(f"Clínica com ID {id} não encontrada.")
        if not isinstance(dados, dict):
            raise ErroCadastroInvalido("Os dados da clínica são inválidos.")

        horarios = None
        if "horarios_funcionamento" in dados:
            horarios = self.__converter_horarios(
                dados["horarios_funcionamento"]
            )
        if "nome" in dados:
            clinica.nome = dados["nome"]
        if "cidade" in dados:
            clinica.cidade = dados["cidade"]
        if "descricao" in dados:
            clinica.descricao = dados["descricao"]
        if horarios is not None:
            clinica.horarios_funcionamento = horarios

    def excluir(self, id: int | None = None) -> None:
        clinica_id = id if id is not None else self.__visao.solicitar_id_clinica()
        clinica = self.__repositorio_sistema.buscar_por_id("clinicas", clinica_id)
        if not isinstance(clinica, Clinica):
            raise ValueError(f"Clínica com ID {clinica_id} não encontrada.")
        if clinica.atendimentos or clinica.profissionais:
            raise ErroCadastroInvalido(
                "Não é possível excluir uma clínica com profissionais ou atendimentos vinculados."
            )
        self.__repositorio_sistema.excluir(clinica)

    def listar(self) -> list:
        return self.__repositorio_sistema.listar("clinicas")

    @staticmethod
    def __converter_horarios(horarios: list) -> list[HorarioFuncionamento]:
        if not isinstance(horarios, list):
            raise ErroHorarioInvalido(
                "Os horários de funcionamento devem ser informados em uma lista."
            )
        if any(
            not isinstance(horario, (HorarioFuncionamento, dict))
            for horario in horarios
        ):
            raise ErroHorarioInvalido(
                "Cada horário deve conter dia, abertura e fechamento válidos."
            )
        if any(
            isinstance(horario, dict)
            and not {
                "dia_semana",
                "hora_abertura",
                "hora_fechamento",
            }.issubset(horario)
            for horario in horarios
        ):
            raise ErroHorarioInvalido(
                "Cada horário deve informar dia, abertura e fechamento."
            )
        return [
            horario
            if isinstance(horario, HorarioFuncionamento)
            else HorarioFuncionamento(
                horario["dia_semana"],
                horario["hora_abertura"],
                horario["hora_fechamento"],
            )
            for horario in horarios
        ]
