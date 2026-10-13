from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entidades.clinica import Clinica


class ControladorClinicas:
    def incluir(self, dados: dict) -> Clinica:
        pass

    def alterar(self, id: int, dados: dict) -> None:
        pass

    def excluir(self, id: int) -> None:
        pass

    def listar(self) -> list:
        pass
