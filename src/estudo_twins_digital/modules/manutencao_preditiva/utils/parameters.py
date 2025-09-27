"""Define dataclasses e classes para os parâmetros do motor de IA.

Este módulo contém as estruturas de dados que encapsulam os parâmetros
necessários para as várias funcionalidades do motor de IA, como processamento
de mensagens, carregamento de documentos e interação com modelos de linguagem.
"""

from dataclasses import dataclass

from py_return_success_or_error import ParametersReturnResult

from .erros import EstruturacaoDadosBaseError


@dataclass
class EstruturacaoDadosBaseParameters(ParametersReturnResult):
    error: EstruturacaoDadosBaseError

    def __str__(self) -> str:
        return self.__repr__()
