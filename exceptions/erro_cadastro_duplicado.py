from .erro_regra_negocio import ErroRegraNegocio


class ErroCadastroDuplicado(ErroRegraNegocio):
    def __init__(
        self,
        mensagem: str = "Já existe um cadastro com os dados informados.",
    ):
        super().__init__(mensagem)
