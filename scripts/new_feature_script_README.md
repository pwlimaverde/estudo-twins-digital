# Gerador de Feature (scripts/new_feature_script.py)

Este utilitário interativo cria o esqueleto de uma nova feature seguindo um padrão de Clean Architecture, atualiza arquivos utilitários do módulo (erros, parâmetros e tipos) e insere um método na fachada `features_compose.py` para facilitar o uso da feature.

> Importante: o script está acoplado ao nome do pacote raiz retornado por `get_project_name()`, atualmente definido como `estudo_twins_digital`. Ajuste esse valor conforme o nome real do seu pacote, caso necessário.

---

## Pré-requisitos

- Python 3.13+
- Gerenciador de ambiente/dependências: [uv] (ou utilize `pip`)
- Dependências de runtime:
  - `py-return-success-or-error`
  - `rich` (para a interface no terminal)

Instalação (via uv):

```powershell
uv sync  # instala as dependências declaradas no pyproject.toml
```

Se preferir `pip`:

```powershell
pip install py-return-success-or-error rich
```

---

## Estrutura esperada do projeto

O script opera sobre a seguinte estrutura (exemplo), onde `<project>` é o pacote raiz (por padrão: `estudo_twins_digital`):

```
src/
  <project>/
    modules/
      <module>/
        utils/
          erros.py
          parameters.py
          types.py
        features/
          features_compose.py  # contém a classe FeaturesCompose
```

- Os arquivos `erros.py`, `parameters.py` e `types.py` devem existir previamente.
- `features_compose.py` deve conter a classe `FeaturesCompose`; o script insere um novo método estático nela.

---

## Como funciona (fluxo)

1. Solicita interativamente o nome do módulo e da feature.
2. Atualiza `utils/` do módulo, adicionando (se ausentes):
   - Uma classe de erro específica da feature (`<Feature>Error`)
   - Uma classe de parâmetros (`<Feature>Parameters`)
   - Type aliases para o use case (e datasource, quando aplicável)
3. Gera arquivos da feature em `features/<snake_case_da_feature>/`:
   - `domain/usecase/<feature>_usecase.py`
   - `datasource/<feature>_datasource.py` (apenas quando `--type call_data`)
4. Atualiza a fachada `features_compose.py`, adicionando:
   - Imports necessários (sem duplicação)
   - Um método estático `def <snake_case_da_feature>() -> None:` que encapsula a chamada ao use case (e datasource, quando aplicável)

---

## Uso

Execução com uv:

```powershell
uv run python scripts/new_feature_script.py --type base
```

Ou:

```powershell
uv run python scripts/new_feature_script.py --type call_data
```

Parâmetros:

- `--type {base|call_data}`
  - `base`: cria apenas o use case e tipos associados.
  - `call_data`: cria use case + datasource e respectivos tipos.

Entradas interativas:

- Nome do módulo (ex.: `ai_engine`)
- Nome da feature (ex.: `generate_chunks`)

O script normaliza o nome da feature para `snake_case` e gera o acrônimo (ex.: `generate_chunks` -> `GC`). Também cria a versão CamelCase para classes (ex.: `GenerateChunks`).

---

## Exemplos

1) Criar uma feature base:

```powershell
uv run python scripts/new_feature_script.py --type base
# Informe: módulo = ai_engine, feature = generate_chunks
```

Arquivos/alterações esperadas:

- `src/<project>/modules/ai_engine/utils/erros.py` (+ `GenerateChunksError` se não existir)
- `src/<project>/modules/ai_engine/utils/parameters.py` (+ `GenerateChunksParameters` se não existir)
- `src/<project>/modules/ai_engine/utils/types.py` (+ aliases `GCUsecase` se não existir)
- `src/<project>/modules/ai_engine/features/generate_chunks/domain/usecase/generate_chunks_usecase.py`
- `src/<project>/modules/ai_engine/features/features_compose.py` (+ método estático `generate_chunks`)

2) Criar uma feature com datasource:

```powershell
uv run python scripts/new_feature_script.py --type call_data
# Informe: módulo = ai_engine, feature = sync_documents
```

Arquivos/alterações esperadas (além dos do caso base):

- `src/<project>/modules/ai_engine/features/sync_documents/datasource/sync_documents_datasource.py`
- `src/<project>/modules/ai_engine/utils/types.py` (+ aliases `SDData`, `SDUsecase` se não existirem)

---

## Convenções seguidas

- Organização por módulos e features dentro de `src/<project>/modules/<module>/features/`.
- Padrões de nomenclatura:
  - Arquivos e métodos em `snake_case`.
  - Classes em `PascalCase`.
- Integração com `py_return_success_or_error` para padronização de retornos (`SuccessReturn`, `ErrorReturn`, `ReturnSuccessOrError`).
- O método adicionado à `FeaturesCompose` lança exceções em caso de `ErrorReturn` e retorna `None` nos casos bem-sucedidos.

---

## Mensagens e erros comuns

- `FileNotFoundError: Arquivos utils não encontrados...`
  - Verifique se `erros.py`, `parameters.py` e `types.py` existem em `utils/` do módulo.
- `features_compose.py não encontrado em '<module>'.`
  - Garanta a presença de `features_compose.py` em `features/` do módulo informado.
- `ValueError("Unexpected return type from usecase")`
  - Indica que o use case não retornou um tipo esperado (`SuccessReturn` ou `ErrorReturn`).
- Inconsistência do pacote raiz
  - Se seu pacote não se chama `estudo_twins_digital`, ajuste `get_project_name()` no script para o nome correto.

---

## Dicas de uso

- Execute o script em um branch de feature para facilitar code review e rollback se necessário.
- Após gerar a estrutura, implemente a lógica no UseCase (e Datasource, se aplicável) e ajuste os parâmetros/erros conforme a regra de negócio real.
- Mantenha os imports consistentes (absolutos nos usecases, relativos na facade), como previsto no script.

---

## Licença

Consulte a licença do repositório principal.