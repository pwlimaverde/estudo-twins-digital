# Reexports para facilitar imports curtos da feature
# Obs.: manter apenas símbolos públicos necessários na fachada.
from .datasource.estruturacao_dados_base_datasource import (
    EstruturacaoDadosBaseDatasource,
)
from .domain.usecase.estruturacao_dados_base_usecase import (
    EstruturacaoDadosBaseUseCase,
)

__all__ = [
    "EstruturacaoDadosBaseUseCase",
    "EstruturacaoDadosBaseDatasource",
]