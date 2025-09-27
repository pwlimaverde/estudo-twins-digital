# Geração de Dados Brutos de Sensores (Motores)

Este script gera um conjunto de dados sintéticos de sensores para múltiplos motores e salva o resultado em um arquivo CSV. Ele foi pensado para apoiar experimentos de Manutenção Preditiva, prototipagem de features e testes de pipelines de dados.

## Local do Script

- Caminho: `scripts/geracao_dados_brutos_csv.py`
- Saída padrão: `dados_brutos_motores.csv` (no diretório raiz do projeto)

## O que é gerado

Para cada motor, é criada uma série temporal com as seguintes colunas:
- `motor_id`: identificador textual do motor (ex.: `motor_01`)
- `horas_operacao`: hora de operação (inteiro), começando em 1 até a vida útil simulada
- `temperatura_c`: temperatura em graus Celsius (float)
- `vibracao_hz`: vibração em Hertz (float)
- `rotacao_rpm`: rotação em RPM (float)
- `corrente_a`: corrente elétrica em Ampères (float)
- `falha_registrada`: indicador da falha (inteiro 0/1); o último registro de cada motor é marcado com `1`

Os sinais são simulados com tendência de degradação ao longo do tempo e ruídos gaussianos, de forma a mimetizar o comportamento de sensores próximos à falha.

## Pré-requisitos

- Python 3.10+ (recomendado)
- Dependências:
  - `numpy`
  - `pandas`

Para instalar rapidamente em um ambiente ativo:

```powershell
python -m pip install numpy pandas
```

> Observação: Se você já utiliza o gerenciador de dependências do projeto, siga o fluxo padrão (ex.: `uv`, `pip-tools`, etc.).

## Como executar

No PowerShell (Windows), a partir do diretório raiz do projeto:

```powershell
python scripts/geracao_dados_brutos_csv.py
```

Ao finalizar, você verá mensagens de log no console e o arquivo `dados_brutos_motores.csv` será criado.

## Parâmetros e personalização

Os parâmetros padrão estão definidos no topo do script:
- `NUM_MOTORES` (padrão: 15)
- `VIDA_MINIMA` (padrão: 180 horas)
- `VIDA_MAXIMA` (padrão: 300 horas)
- `NOME_ARQUIVO` (padrão: `dados_brutos_motores.csv`)

Para personalizar, edite estes valores diretamente no script ou importe a função `generate_data` em outro módulo Python e forneça os valores desejados.

### Reprodutibilidade (seed)

O script usa geração aleatória sem fixar *seed*. Se você precisar de resultados reproduzíveis, defina uma semente antes de chamar as funções, por exemplo:

```python
import numpy as np
np.random.seed(42)
```

## Estrutura do CSV (exemplo de cabeçalho)

```
motor_id,horas_operacao,temperatura_c,vibracao_hz,rotacao_rpm,corrente_a,falha_registrada
```

Cada motor terá várias linhas, e a última linha daquele motor terá `falha_registrada = 1`.

## Mensagens de console

Durante a execução, o script exibe:
- Quantidade de motores gerados
- Confirmação de criação do arquivo
- Total de registros e total de motores
- Amostras das primeiras e últimas linhas do DataFrame

## Erros comuns e dicas

- "Permissão negada" ao salvar CSV: verifique se o arquivo está aberto em outro programa (ex.: Excel) e feche-o.
- Pacotes não encontrados: instale `numpy` e `pandas` no ambiente que está executando o script.
- Final de linha (CRLF/LF): caso use ferramentas de lint no Windows, padronize com `.gitattributes` para evitar avisos.

## Integração em pipelines

Este CSV pode ser consumido diretamente por outros módulos do projeto (`src/estudo_twins_digital/...`) ou por notebooks de exploração. Ele é útil para:
- Testes de ingestão e transformação
- Prototipagem de features
- Demonstrações de *end-to-end* em manutenção preditiva

## Manutenção

- O script usa tipos estáticos (typing/NumPy) para facilitar a checagem em ferramentas como Pyright.
- Os nomes das colunas e variáveis foram mantidos em português para preservar compatibilidade com usos existentes.
- Ao alterar parâmetros ou lógica de geração, atualize este README conforme necessário.