from datetime import time

from exceptions.erro_horario_invalido import ErroHorarioInvalido


DIAS_SEMANA = (
    "segunda-feira",
    "terça-feira",
    "quarta-feira",
    "quinta-feira",
    "sexta-feira",
    "sábado",
    "domingo",
)


class HorarioFuncionamento:
    def __init__(self, dia_semana: str, hora_abertura: time, hora_fechamento: time):
        self.__validar_dia(dia_semana)
        self.__validar_intervalo(hora_abertura, hora_fechamento)
        self.__dia_semana = dia_semana
        self.__hora_abertura = hora_abertura
        self.__hora_fechamento = hora_fechamento

    @property
    def dia_semana(self):
        return self.__dia_semana

    @dia_semana.setter
    def dia_semana(self, dia_semana):
        self.__validar_dia(dia_semana)
        self.__dia_semana = dia_semana

    @property
    def hora_abertura(self):
        return self.__hora_abertura

    @hora_abertura.setter
    def hora_abertura(self, hora_abertura):
        self.__validar_intervalo(hora_abertura, self.__hora_fechamento)
        self.__hora_abertura = hora_abertura

    @property
    def hora_fechamento(self):
        return self.__hora_fechamento

    @hora_fechamento.setter
    def hora_fechamento(self, hora_fechamento):
        self.__validar_intervalo(self.__hora_abertura, hora_fechamento)
        self.__hora_fechamento = hora_fechamento

    def contem(self, inicio: time, fim: time) -> bool:
        if not isinstance(inicio, time) or not isinstance(fim, time):
            raise ErroHorarioInvalido("Os horários do atendimento são inválidos.")
        return (
            inicio < fim
            and self.hora_abertura <= inicio
            and fim <= self.hora_fechamento
        )

    @staticmethod
    def __validar_dia(dia_semana: str) -> None:
        if not isinstance(dia_semana, str) or dia_semana not in DIAS_SEMANA:
            raise ErroHorarioInvalido(f"Dia da semana inválido: {dia_semana}.")

    @staticmethod
    def __validar_intervalo(
        hora_abertura: time,
        hora_fechamento: time,
    ) -> None:
        if not isinstance(hora_abertura, time) or not isinstance(
            hora_fechamento,
            time,
        ):
            raise ErroHorarioInvalido("Os horários de funcionamento são inválidos.")
        if hora_abertura >= hora_fechamento:
            raise ErroHorarioInvalido(
                "A abertura deve ocorrer antes do fechamento."
            )
