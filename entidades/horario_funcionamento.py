from datetime import time


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
        if dia_semana not in DIAS_SEMANA:
            raise ValueError(f"Dia da semana inválido: {dia_semana}.")
        if hora_abertura >= hora_fechamento:
            raise ValueError("A abertura deve ocorrer antes do fechamento.")

        self.__dia_semana = dia_semana
        self.__hora_abertura = hora_abertura
        self.__hora_fechamento = hora_fechamento

    @property
    def dia_semana(self):
        return self.__dia_semana

    @dia_semana.setter
    def dia_semana(self, dia_semana):
        self.__dia_semana = dia_semana

    @property
    def hora_abertura(self):
        return self.__hora_abertura

    @hora_abertura.setter
    def hora_abertura(self, hora_abertura):
        self.__hora_abertura = hora_abertura

    @property
    def hora_fechamento(self):
        return self.__hora_fechamento

    @hora_fechamento.setter
    def hora_fechamento(self, hora_fechamento):
        self.__hora_fechamento = hora_fechamento

    def contem(self, inicio: time, fim: time) -> bool:
        return (
            inicio < fim
            and self.hora_abertura <= inicio
            and fim <= self.hora_fechamento
        )
