from .erro_regra_negocio import ErroRegraNegocio


class ErroAtendimentoIndependente(ErroRegraNegocio):
    def __init__(
        self,
        mensagem: str = "O paciente não pode ser atendido sem um responsável legal.",
    ):
        super().__init__(mensagem)
