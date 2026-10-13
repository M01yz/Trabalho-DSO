from .erro_regra_negocio import ErroRegraNegocio


class ErroHorarioInvalido(ErroRegraNegocio):
    def __init__(self, mensagem: str = "O horário informado é inválido."):
        super().__init__(mensagem)
