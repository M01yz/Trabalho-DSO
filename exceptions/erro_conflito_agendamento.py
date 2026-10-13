from .erro_regra_negocio import ErroRegraNegocio


class ErroConflitoAgendamento(ErroRegraNegocio):
    def __init__(
        self,
        mensagem: str = "Já existe um atendimento agendado para esse horário.",
    ):
        super().__init__(mensagem)
