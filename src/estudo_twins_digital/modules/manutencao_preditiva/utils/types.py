"""Define apelidos de tipo e estruturas de dados para o módulo de IA.

Este módulo centraliza as definições de tipo usadas nas
funcionalidades do motor de IA, melhorando a legibilidade e a
manutenção do código.

Inclui apelidos para casos de uso e fontes de dados, bem como
estruturas de dados específicas.
"""

from typing import TypeAlias

from py_return_success_or_error import Datasource, UsecaseBaseCallData

from .parameters import EstruturacaoDadosBaseParameters

# Usamos TypeAlias para manter o alias com valor em runtime, permitindo
# que seja usado como base de classe (ex.: class Foo(EDBUsecase)).
# Suprimimos UP040 pois preferimos compatibilidade de runtime.
EDBData: TypeAlias = Datasource[
    str,
    EstruturacaoDadosBaseParameters,
] 

EDBUsecase: TypeAlias = UsecaseBaseCallData[
    str,
    str,
    EstruturacaoDadosBaseParameters,
]  
