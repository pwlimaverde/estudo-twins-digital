from py_return_success_or_error import (
    ErrorReturn,
    ReturnSuccessOrError,
    SuccessReturn,
)

from estudo_twins_digital.modules.manutencao_preditiva.utils.parameters import (
    EstruturacaoDadosBaseParameters,
)
from estudo_twins_digital.modules.manutencao_preditiva.utils.types import (
    EDBUsecase,
)


class EstruturacaoDadosBaseUseCase(EDBUsecase):
    def __call__(
        self, parameters: EstruturacaoDadosBaseParameters
    ) -> ReturnSuccessOrError[str]:
        # Chamada segura ao datasource provida por UsecaseBaseCallData
        data = self._resultDatasource(
            parameters=parameters, datasource=self._datasource
        )

        if isinstance(data, SuccessReturn):
            return SuccessReturn(data.result)
        elif isinstance(data, ErrorReturn):
            return data
        else:
            return ErrorReturn(error=parameters.error)
