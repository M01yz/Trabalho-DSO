from __future__ import annotations

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
        if dados_clinica.get("tipo") not in (None, "clinica"):
            raise ValueError("Este controlador só pode incluir cadastros de clínica.")

        clinica = Clinica(
            id=dados_clinica["id"],
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

        if "nome" in dados:
            clinica.nome = dados["nome"]
        if "cidade" in dados:
            clinica.cidade = dados["cidade"]
        if "descricao" in dados:
            clinica.descricao = dados["descricao"]
        if "horarios_funcionamento" in dados:
            clinica.horarios_funcionamento = self.__converter_horarios(
                dados["horarios_funcionamento"]
            )

    def excluir(self, id: int | None = None) -> None:
        clinica_id = id if id is not None else self.__visao.solicitar_id_clinica()
        clinica = self.__repositorio_sistema.buscar_por_id("clinicas", clinica_id)
        if not isinstance(clinica, Clinica):
            raise ValueError(f"Clínica com ID {clinica_id} não encontrada.")
        self.__repositorio_sistema.excluir(clinica)

    def listar(self) -> list:
        return self.__repositorio_sistema.listar("clinicas")

    @staticmethod
    def __converter_horarios(horarios: list) -> list[HorarioFuncionamento]:
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
