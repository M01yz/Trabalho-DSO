from .erro_regra_negocio import ErroRegraNegocio


class ErroCadastroInvalido(ErroRegraNegocio):
    def __init__(self, mensagem: str = "Os dados do cadastro são inválidos."):
        super().__init__(mensagem)
