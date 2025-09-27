"""Facade para os casos de uso do módulo AI Engine.

Esta classe fornece uma interface simplificada para acessar as funcionalidades
de IA do sistema, como processamento de documentos, análise de mensagens e
interação com modelos de linguagem.
"""

from py_return_success_or_error import (
    ErrorReturn,
    ReturnSuccessOrError,
    SuccessReturn,
)

from ..utils.erros import EstruturacaoDadosBaseError
from ..utils.parameters import EstruturacaoDadosBaseParameters
from ..utils.types import EDBData, EDBUsecase
from .estruturacao_dados_base import (
    EstruturacaoDadosBaseDatasource,
    EstruturacaoDadosBaseUseCase,
)


class FeaturesCompose:
    """Facade para os casos de uso do módulo AI Engine."""

    @staticmethod
    def estruturacao_dados_base() -> str:
        error = EstruturacaoDadosBaseError(
            "Erro ao executar estruturacao_dados_base!"
        )
        parameters = EstruturacaoDadosBaseParameters(
            error=error,
        )
        datasource: EDBData = EstruturacaoDadosBaseDatasource()
        usecase: EDBUsecase = EstruturacaoDadosBaseUseCase(datasource)
        data: ReturnSuccessOrError[str] = usecase(parameters)
        if isinstance(data, SuccessReturn):
            return data.result
        elif isinstance(data, ErrorReturn):
            raise data.result
        else:
            raise ValueError("Unexpected return type from usecase")
