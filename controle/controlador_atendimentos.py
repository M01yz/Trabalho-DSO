from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Model.atendimento import Atendimento


class ControladorAtendimentos:
    def incluir(self, dados: dict) -> Atendimento:
        pass

    def alterar(self, id: int, dados: dict) -> None:
        pass

    def excluir(self, id: int) -> None:
        pass

    def listar(self) -> list:
        pass
