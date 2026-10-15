from .erro_atendimento_independente import ErroAtendimentoIndependente
from .erro_cadastro_invalido import ErroCadastroInvalido
from .erro_cadastro_duplicado import ErroCadastroDuplicado
from .erro_conflito_agendamento import ErroConflitoAgendamento
from .erro_horario_invalido import ErroHorarioInvalido
from .erro_pagamento_invalido import ErroPagamentoInvalido
from .erro_regra_negocio import ErroRegraNegocio

__all__ = [
    "ErroAtendimentoIndependente",
    "ErroCadastroInvalido",
    "ErroCadastroDuplicado",
    "ErroConflitoAgendamento",
    "ErroHorarioInvalido",
    "ErroPagamentoInvalido",
    "ErroRegraNegocio",
]
