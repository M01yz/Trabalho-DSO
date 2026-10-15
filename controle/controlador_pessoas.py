from __future__ import annotations

from exceptions.erro_cadastro_duplicado import ErroCadastroDuplicado
from exceptions.erro_cadastro_invalido import ErroCadastroInvalido

from entidades.clinica import Clinica
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
        if dados is None:
            tipo_pessoa = self.__visao.solicitar_dados(somente_tipo=True)
            if tipo_pessoa.get("tipo") == "profissional":
                self.__visao.exibir_listagem(
                    self.__repositorio_sistema.listar("clinicas")
                )
            dados_pessoa = self.__visao.solicitar_dados(
                tipo=tipo_pessoa.get("tipo")
            )
        else:
            dados_pessoa = dados
        if not isinstance(dados_pessoa, dict):
            raise ErroCadastroInvalido("Os dados da pessoa são inválidos.")
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
        self.__validar_cpf_disponivel(dados.get("cpf"))
        paciente = Paciente(
            data_nascimento=dados["data_nascimento"],
            nome=dados["nome"],
            cpf=dados["cpf"],
            celular=dados["celular"],
        )
        self.__repositorio_sistema.salvar(paciente)
        return paciente

    def incluir_profissional(self, dados: dict) -> Profissional:
        self.__validar_cpf_disponivel(dados.get("cpf"))
        clinica_id = dados.get("clinica_id")
        if type(clinica_id) is not int:
            raise ErroCadastroInvalido(
                "O ID da clínica de atuação deve ser informado."
            )
        clinica = self.__repositorio_sistema.buscar_por_id("clinicas", clinica_id)
        if not isinstance(clinica, Clinica):
            raise ValueError(f"Clínica com ID {clinica_id} não encontrada.")

        profissional = Profissional(
            nome=dados["nome"],
            cpf=dados["cpf"],
            celular=dados["celular"],
            especialidade=dados["especialidade"],
            registro_profissional=dados["registro_profissional"],
        )
        self.__repositorio_sistema.salvar(profissional)
        clinica.vincular_profissional(profissional)
        return profissional

    def incluir_responsavel(self, dados: dict) -> ResponsavelLegal:
        self.__validar_cpf_disponivel(dados.get("cpf"))
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
        if dados is not None and not isinstance(dados, dict):
            raise ErroCadastroInvalido("Os dados da pessoa são inválidos.")

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

        atendimentos = self.__repositorio_sistema.listar("atendimentos")
        if isinstance(pessoa, Paciente) and any(
            atendimento.paciente is pessoa for atendimento in atendimentos
        ):
            raise ValueError(
                "Não é possível excluir um paciente associado a atendimentos."
            )
        if isinstance(pessoa, ResponsavelLegal) and any(
            atendimento.responsavel_legal is pessoa for atendimento in atendimentos
        ):
            raise ValueError(
                "Não é possível excluir um responsável associado a atendimentos."
            )
        if isinstance(pessoa, Profissional):
            if any(
                atendimento.profissional is pessoa
                for atendimento in atendimentos
            ):
                raise ValueError(
                    "Não é possível excluir um profissional associado a atendimentos."
                )
            if any(
                procedimento.profissional_responsavel is pessoa
                for procedimento in self.__repositorio_sistema.listar(
                    "procedimentos"
                )
            ):
                raise ValueError(
                    "Não é possível excluir um profissional responsável por procedimentos."
                )
            for clinica in self.__repositorio_sistema.listar("clinicas"):
                clinica.desvincular_profissional(pessoa)
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

    def __validar_cpf_disponivel(self, cpf: object) -> None:
        if not isinstance(cpf, str) or not cpf:
            raise ErroCadastroInvalido("O CPF da pessoa deve ser informado.")
        if self.__repositorio_sistema.buscar_por_id("pessoas", cpf) is not None:
            raise ErroCadastroDuplicado(f"Já existe uma pessoa com o CPF {cpf}.")
