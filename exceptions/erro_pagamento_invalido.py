from .erro_regra_negocio import ErroRegraNegocio


class ErroPagamentoInvalido(ErroRegraNegocio):
    def __init__(self, mensagem: str = "Os dados do pagamento são inválidos."):
        super().__init__(mensagem)
