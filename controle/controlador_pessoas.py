from __future__ import annotations

from entidades.paciente import Paciente
from entidades.profissional import Profissional
from entidades.repositorio_sistema import RepositorioSistema
from entidades.responsavel import ResponsavelLegal
from limite.visao_cadastros import VisaoCadastros


class ControladorPessoas:
    def __init__(
        self,
        repositorio_sistema: RepositorioSistema,
        visao: VisaoCadastros | None = None,
    ) -> None:
        self.__repositorio_sistema = repositorio_sistema
        self.__visao = visao if visao is not None else VisaoCadastros()

    def incluir(
        self,
        dados: dict | None = None,
    ) -> Paciente | Profissional | ResponsavelLegal:
        dados_pessoa = dados if dados is not None else self.__visao.solicitar_dados()
        tipo = dados_pessoa.get("tipo")

        if tipo == "paciente":
            return self.incluir_paciente(dados_pessoa)
        if tipo == "profissional":
            return self.incluir_profissional(dados_pessoa)
        if tipo == "responsavel_legal":
            return self.incluir_responsavel(dados_pessoa)

        raise ValueError(
            "Este controlador só pode incluir pacientes, profissionais "
            "ou responsáveis legais."
        )

    def incluir_paciente(self, dados: dict) -> Paciente:
        paciente = Paciente(
            data_nascimento=dados["data_nascimento"],
            nome=dados["nome"],
            cpf=dados["cpf"],
            celular=dados["celular"],
        )
        self.__repositorio_sistema.salvar(paciente)
        return paciente

    def incluir_profissional(self, dados: dict) -> Profissional:
        profissional = Profissional(
            nome=dados["nome"],
            cpf=dados["cpf"],
            celular=dados["celular"],
            especialidade=dados["especialidade"],
            registro_profissional=dados["registro_profissional"],
        )
        self.__repositorio_sistema.salvar(profissional)
        return profissional

    def incluir_responsavel(self, dados: dict) -> ResponsavelLegal:
        responsavel = ResponsavelLegal(
            nome=dados["nome"],
            cpf=dados["cpf"],
            celular=dados["celular"],
        )
        self.__repositorio_sistema.salvar(responsavel)
        return responsavel

    def alterar(self, cpf: str | None = None, dados: dict | None = None) -> None:
        cpf_atual = cpf if cpf is not None else self.__visao.solicitar_cpf_pessoa()
        pessoa = self.__repositorio_sistema.buscar_por_id("pessoas", cpf_atual)
        if not isinstance(pessoa, (Paciente, Profissional, ResponsavelLegal)):
            raise ValueError(f"Pessoa com CPF {cpf_atual} não encontrada.")

        dados_atualizados = (
            dados
            if dados is not None
            else self.__visao.solicitar_dados_alteracao(
                "paciente"
                if isinstance(pessoa, Paciente)
                else "profissional"
                if isinstance(pessoa, Profissional)
                else "responsavel_legal"
            )
        )

        pessoa.nome = dados_atualizados.get("nome", pessoa.nome)
        pessoa.celular = dados_atualizados.get("celular", pessoa.celular)
        if isinstance(pessoa, Paciente) and "data_nascimento" in dados_atualizados:
            pessoa.data_nascimento = dados_atualizados["data_nascimento"]
        if isinstance(pessoa, Profissional):
            pessoa.especialidade = dados_atualizados.get(
                "especialidade",
                pessoa.especialidade,
            )
            pessoa.registro_profissional = dados_atualizados.get(
                "registro_profissional",
                pessoa.registro_profissional,
            )

    def excluir(self, cpf: str | None = None) -> None:
        cpf_pessoa = cpf if cpf is not None else self.__visao.solicitar_cpf_pessoa()
        pessoa = self.__repositorio_sistema.buscar_por_id("pessoas", cpf_pessoa)
        if not isinstance(pessoa, (Paciente, Profissional, ResponsavelLegal)):
            raise ValueError(f"Pessoa com CPF {cpf_pessoa} não encontrada.")

        self.__repositorio_sistema.excluir(pessoa)

    def listar(self, tipo: str | None = None) -> list:
        dados_tipo = (
            {"tipo": tipo}
            if tipo is not None
            else self.__visao.solicitar_dados(somente_tipo=True)
        )
        tipo_pessoa = dados_tipo.get("tipo")
        tipos_suportados = {
            "paciente": Paciente,
            "profissional": Profissional,
            "responsavel_legal": ResponsavelLegal,
        }
        if tipo_pessoa not in tipos_suportados:
            raise ValueError(f"Tipo de pessoa inválido: {tipo_pessoa}.")

        classe_pessoa = tipos_suportados[tipo_pessoa]
        pessoas = [
            pessoa
            for pessoa in self.__repositorio_sistema.listar("pessoas")
            if isinstance(pessoa, classe_pessoa)
        ]
        return pessoas
