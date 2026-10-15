from collections import Counter

from .repositorio_sistema import RepositorioSistema


class ServicoRelatorios:
    def __init__(self, repositorio_sistema: RepositorioSistema):
        self.__repositorio_sistema = repositorio_sistema

    def clinicas_mais_atendimentos(self) -> list:
        relatorio = [
            {
                "id": clinica.id,
                "nome": clinica.nome,
                "cidade": clinica.cidade,
                "quantidade_atendimentos": len(clinica.atendimentos),
            }
            for clinica in self.__repositorio_sistema.listar("clinicas")
        ]
        return sorted(
            relatorio,
            key=lambda clinica: clinica["quantidade_atendimentos"],
            reverse=True,
        )

    def atendimentos_por_valor(self) -> list:
        relatorio = [
            {
                "id": atendimento.id,
                "data": atendimento.data,
                "hora_inicio": atendimento.hora_inicio,
                "hora_fim": atendimento.hora_fim,
                "valor": atendimento.valor,
            }
            for atendimento in self.__repositorio_sistema.listar("atendimentos")
        ]
        return sorted(relatorio, key=lambda atendimento: atendimento["valor"], reverse=True)

    def procedimentos_mais_realizados(self) -> list:
        quantidades = Counter(
            procedimento.descricao
            for atendimento in self.__repositorio_sistema.listar("atendimentos")
            for procedimento in atendimento.procedimentos
        )
        return [
            {"nome": nome, "quantidade_realizada": quantidade}
            for nome, quantidade in sorted(
                quantidades.items(),
                key=lambda item: item[1],
                reverse=True,
            )
        ]

    def procedimentos_por_custo(self) -> list:
        relatorio = [
            {
                "id": procedimento.id,
                "descricao": procedimento.descricao,
                "custo": procedimento.custo,
                "tipo_atendimento": procedimento.tipo_atendimento.nome,
            }
            for procedimento in self.__repositorio_sistema.listar("procedimentos")
        ]
        return sorted(relatorio, key=lambda procedimento: procedimento["custo"], reverse=True)
