from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Model.tipo_atendimento import TipoAtendimento


class ControladorTiposAtendimento:
    def incluir(self, dados: dict) -> TipoAtendimento:
        pass

    def alterar(self, id: int, dados: dict) -> None:
        pass

    def excluir(self, id: int) -> None:
        pass

    def listar(self) -> list:
        pass
