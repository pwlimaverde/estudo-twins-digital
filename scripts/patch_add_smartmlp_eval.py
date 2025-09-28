import nbformat as nbf
from pathlib import Path

NB_PATH = Path(r"c:\PROJETOS\PYTHON\APPS\estudo-twins-digital\tests\debug\modelo_perceptron.ipynb")

EVAL_CELL_CODE = (
    "# Instanciar e treinar SmartMLP\n"
    "import copy as _copy\n"
    "initial_weights_smart = {k: v.copy() for k, v in initial_weights.items()}\n\n"
    "mlp = SmartMLP(initial_weights=initial_weights_smart)\n\n"
    "print(\"--- Iniciando Treinamento ---\")\n"
    "mlp.train(X_train, y_train)\n"
    "print(\"--- Treinamento Concluído ---\\n\")\n\n"
    "print(\"=\"*40)\n"
    "print(\"      AVALIAÇÃO DO SMART MLP\")\n"
    "print(\"=\"*40)\n\n"
    "# Definir os mesmos casos de teste\n"
    "test_1 = np.array([0.2, 0.8, 0.1]) # Aprovação Esperada: 1\n"
    "test_2 = np.array([0.3, 0.2, 0.2]) # Reprovação Esperada: 0\n"
    "test_3 = np.array([0.8, 0.9, 0.1]) # Reprovação por Temperatura (CASO CRÍTICO): 0\n\n"
    "tests = [test_1, test_2, test_3]\n"
    "expected_results = [1, 0, 0]\n"
    "test_names = [\"Aprovação Normal\", \"Reprovação Normal\", \"Reprovação por Temperatura (Crítico)\"]\n\n"
    "for i, test_case in enumerate(tests):\n"
    "    print(f\"\\n--- Caso de Teste: {test_names[i]} ---\")\n"
    "    print(f\"Entrada: {test_case}, Resultado Esperado: {expected_results[i]}\")\n\n"
    "    prediction = mlp.predict(test_case)\n"
    "    resultado_final = 'Aprovado' if prediction > 0.5 else 'Reprovado'\n"
    "    print(f\"  Predição da SmartMLP: {prediction[0]:.4f} -> {resultado_final}\")\n"
)



def main():
    nb = nbf.read(NB_PATH.open("r", encoding="utf-8"), as_version=4)

    # Verificar se já existe uma célula que instancia SmartMLP
    already_exists = False
    for cell in nb.cells:
        if cell.cell_type == "code" and (
            "mlp = SmartMLP(" in cell.source
        ):
            already_exists = True
            break

    if already_exists:
        print("Célula de avaliação do SmartMLP já existe. Nenhuma alteração necessária.")
        return

    # Encontrar índice da célula onde a classe SmartMLP é definida
    insert_idx = None
    for idx, cell in enumerate(nb.cells):
        if cell.cell_type == "code" and "class SmartMLP" in cell.source:
            insert_idx = idx + 1
            break

    new_cell = nbf.v4.new_code_cell(EVAL_CELL_CODE)

    if insert_idx is None:
        # Caso não encontre, adiciona ao final
        nb.cells.append(new_cell)
        print("SmartMLP não encontrado explicitamente; célula de avaliação adicionada ao final do notebook.")
    else:
        nb.cells.insert(insert_idx, new_cell)
        print(f"Célula de avaliação do SmartMLP inserida após a definição da classe (índice {insert_idx}).")

    nbf.write(nb, NB_PATH.open("w", encoding="utf-8"))
    print("Notebook atualizado com a verificação do SmartMLP.")


if __name__ == "__main__":
    main()