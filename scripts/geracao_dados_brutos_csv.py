from collections.abc import Iterable
from typing import Any, cast

import numpy as np
import pandas as pd
from numpy import float64, int64
from numpy.typing import NDArray

# --- Parâmetros da Simulação (valores padrão) ---
# Mantemos os nomes das variáveis e das colunas em português para preservar
# a compatibilidade com o arquivo CSV e com usos existentes.
NUM_MOTORES: int = 15
VIDA_MINIMA: int = 180  # Horas mínimas de operação antes da falha
VIDA_MAXIMA: int = 300  # Horas máximas de operação antes da falha
NOME_ARQUIVO: str = "dados_brutos_motores.csv"


def generate_data(
    num_motores: int = NUM_MOTORES,
    vida_minima: int = VIDA_MINIMA,
    vida_maxima: int = VIDA_MAXIMA,
) -> pd.DataFrame:
    """Gera dados sintéticos de sensores para múltiplos motores.

    Comentários:
    - Utiliza um fator de degradação (0 → novo, 1 → falha)
      ao longo da vida útil simulada para cada motor.
    - Todos os arrays NumPy são tipados para reduzir ambiguidade
      na checagem estática (Pyright, modo estrito).
    - Retorna um DataFrame consolidado com os dados de todos os motores.
    """
    lista_de_dados_motores: list[pd.DataFrame] = []

    print(f"Iniciando a geração de dados para {num_motores} motores...")

    for i in range(1, num_motores + 1):
        motor_id: str = f"motor_{i:02d}"

        # Define uma vida útil aleatória para este motor
        vida_total_motor: int = int(
            np.random.randint(vida_minima, vida_maxima + 1)
        )

        # Cria a série temporal de horas de operação
        horas_operacao: NDArray[int64] = np.arange(
            1, vida_total_motor + 1, dtype=np.int64
        )

        # --- Simulação dos Sensores com Degradação ---

        # Fator de degradação: um valor que vai de 0 (novo) a 1 (falha)
        fator_degradacao: NDArray[float64] = horas_operacao / float(
            vida_total_motor
        )

        # Temperatura: começa em ~70°C e aumenta até ~100°C, com ruído
        temp_base: float = 70.0
        temp_aumento: float = 30.0
        temperatura: NDArray[float64] = (
            temp_base
            + (fator_degradacao * temp_aumento)
            + np.random.normal(0.0, 1.5, size=vida_total_motor).astype(
                np.float64
            )
        )

        # Vibração: começa em ~10 Hz e aumenta até ~25 Hz,
        # com mais ruído no final
        vib_base: float = 10.0
        vib_aumento: float = 15.0
        vibracao: NDArray[float64] = (
            vib_base
            + (fator_degradacao**2 * vib_aumento)
            + np.random.normal(0.0, 0.8, size=vida_total_motor).astype(
                np.float64
            )
        )

        # Rotação: começa estável em ~1800 RPM e cai um pouco perto da falha
        rotacao: NDArray[float64] = (
            1800.0
            - (fator_degradacao**3 * 50.0)
            + np.random.normal(0.0, 5.0, size=vida_total_motor).astype(
                np.float64
            )
        )

        # Corrente: começa em ~15 A e aumenta um pouco com a carga/desgaste
        corrente: NDArray[float64] = (
            15.0
            + (fator_degradacao * 3.0)
            + np.random.normal(0.0, 0.2, size=vida_total_motor).astype(
                np.float64
            )
        )

        # Coluna de falha: 0 para todos os registros, exceto o último
        falha_registrada: NDArray[int64] = np.zeros(
            vida_total_motor, dtype=np.int64
        )
        falha_registrada[-1] = 1

        # Monta o DataFrame para este motor
        dados_motor: pd.DataFrame = pd.DataFrame(
            {
                "motor_id": motor_id,
                "horas_operacao": horas_operacao,
                "temperatura_c": temperatura.round(2),
                "vibracao_hz": vibracao.round(2),
                "rotacao_rpm": rotacao.round(2),
                "corrente_a": corrente.round(2),
                "falha_registrada": falha_registrada.astype(int),
            }
        )

        lista_de_dados_motores.append(dados_motor)

    # Concatena os dados de todos os motores em um único DataFrame
    df_final_bruto: pd.DataFrame = pd.concat(
        lista_de_dados_motores, ignore_index=True
    )
    return df_final_bruto


def save_csv(df: pd.DataFrame, filename: str) -> None:
    """Salva o DataFrame em um arquivo .csv."""
    df.to_csv(filename, index=False)  # pyright: ignore[reportUnknownMemberType]


def main() -> None:
    """Ponto de entrada para geração e gravação do CSV.

    Mostra amostras no console.
    """
    df_final_bruto: pd.DataFrame = generate_data()
    save_csv(df_final_bruto, NOME_ARQUIVO)

    print("\n--- Geração Concluída! ---")
    print(f"Arquivo '{NOME_ARQUIVO}' criado com sucesso.")
    print(f"Total de registros: {len(df_final_bruto)}")
    # Converte a lista de IDs para tipos conhecidos (Pyright estrito)
    motor_ids_any: Iterable[Any] = cast(
        Iterable[Any], df_final_bruto["motor_id"].tolist()
    )  # pyright: ignore[reportUnknownMemberType]
    motor_ids: list[str] = [str(x) for x in motor_ids_any]
    total_motores: int = len(set(motor_ids))
    print(f"Total de motores: {total_motores}")

    print("\n--- Amostra dos Dados Gerados (primeiras linhas) ---")
    print(df_final_bruto.head())

    print("\n--- Amostra dos Dados Gerados (últimas linhas) ---")
    print(df_final_bruto.tail())


if __name__ == "__main__":
    main()
