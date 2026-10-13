from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entidades.procedimento import Procedimento


class ControladorProcedimentos:
    def incluir(self, atendimento_id: int, dados: dict) -> Procedimento:
        pass

    def alterar(self, id: int, dados: dict) -> None:
        pass

    def excluir(self, id: int) -> None:
        pass

    def listar(self) -> list:
        pass
