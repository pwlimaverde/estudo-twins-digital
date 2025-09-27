"""Define classes de erro personalizadas para o motor de IA.

Este módulo contém dataclasses para erros de aplicação específicos que podem
ocorrer dentro do motor de IA, proporcionando um tratamento de erros claro e
consistente para diferentes funcionalidades.
"""

from dataclasses import dataclass

from py_return_success_or_error import AppError


@dataclass
class EstruturacaoDadosBaseError(AppError):
    message: str

    def __str__(self) -> str:
        return f"EstruturacaoDadosBaseError - {self.message}"
