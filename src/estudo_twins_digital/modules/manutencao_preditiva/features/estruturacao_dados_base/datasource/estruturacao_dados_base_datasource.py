from estudo_twins_digital.modules.manutencao_preditiva.utils.parameters import (
    EstruturacaoDadosBaseParameters,
)
from estudo_twins_digital.modules.manutencao_preditiva.utils.types import (
    EDBData,
)


class EstruturacaoDadosBaseDatasource(EDBData):
    def __call__(self, parameters: EstruturacaoDadosBaseParameters) -> None:
        # TODO: Implementar acesso a dados/API.
        pass
