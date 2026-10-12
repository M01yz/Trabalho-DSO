from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Model.paciente import Paciente
    from Model.profissional import Profissional
    from Model.responsavel import Responsavel


class ControladorPessoas:
    def incluir_paciente(self, dados: dict) -> Paciente:
        pass

    def incluir_profissional(self, dados: dict) -> Profissional:
        pass

    def incluir_responsavel(self, dados: dict) -> Responsavel:
        pass

    def alterar(self, cpf: str, dados: dict) -> None:
        pass

    def excluir(self, cpf: str) -> None:
        pass

    def listar(self) -> list:
        pass
