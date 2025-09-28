import json
from pathlib import Path
from typing import List

# Caminho absoluto do notebook a ser modificado
NB_PATH = Path(r"c:\PROJETOS\PYTHON\APPS\estudo-twins-digital\tests\debug\modelo_perceptron.ipynb")


def insert_generate_initial_weights_cell(cells: List[dict]) -> List[dict]:
    """Insere uma célula com a função generate_initial_weights logo abaixo da célula que contém generate_data."""
    target_idx = None
    for i, cell in enumerate(cells):
        if cell.get("cell_type") == "code":
            src_lines = cell.get("source", [])
            if any("def generate_data(" in line for line in src_lines):
                target_idx = i
                break

    if target_idx is None:
        return cells

    new_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def generate_initial_weights(input_size=3, h1_size=5, h2_size=4, output_size=1, seed=42):\n",
            "    \"\"\"Gera pesos/vieses iniciais determinísticos para comparar modelos.\"\"\"\n",
            "    rng = np.random.default_rng(seed)\n",
            "    # Camada H1\n",
            "    weights_h1 = rng.normal(0, 0.1, size=(input_size, h1_size))\n",
            "    bias_h1 = np.zeros(h1_size)\n",
            "    # Camada H2 (densa)\n",
            "    weights_h2 = rng.normal(0, 0.1, size=(h1_size, h2_size))\n",
            "    bias_h2 = np.zeros(h2_size)\n",
            "    # Saída\n",
            "    weights_out = rng.normal(0, 0.1, size=(h2_size, output_size))\n",
            "    bias_out = np.zeros(output_size)\n",
            "    return {\n",
            "        'weights_h1': weights_h1,\n",
            "        'bias_h1': bias_h1,\n",
            "        'weights_h2': weights_h2,\n",
            "        'bias_h2': bias_h2,\n",
            "        'weights_out': weights_out,\n",
            "        'bias_out': bias_out,\n",
            "    }\n",
        ],
    }

    # Inserir imediatamente após a célula de generate_data
    cells.insert(target_idx + 1, new_cell)
    return cells


def patch_standard_mlp_cell(cell: dict) -> bool:
    """Atualiza a classe StandardMLP para receber pesos por parâmetro."""
    if cell.get("cell_type") != "code":
        return False
    src = cell.get("source", [])
    if not any("class StandardMLP:" in line for line in src):
        return False

    changed = False
    new_src = []
    for line in src:
        # Altera assinatura do construtor
        if "def __init__(self, input_size=3, h1_size=5, h2_size=4, output_size=1):" in line:
            new_src.append("    def __init__(self, initial_weights, input_size=3, h1_size=5, h2_size=4, output_size=1):\n")
            changed = True
            continue
        # Substitui inicializações aleatórias por pesos do parâmetro
        if "self.weights_h1 = np.random.randn" in line:
            new_src.append("        self.weights_h1 = initial_weights[\"weights_h1\"]\n")
            changed = True
            continue
        if "self.bias_h1 = np.zeros(" in line:
            new_src.append("        self.bias_h1 = initial_weights[\"bias_h1\"]\n")
            changed = True
            continue
        if "self.weights_h2 = np.random.randn" in line:
            new_src.append("        self.weights_h2 = initial_weights[\"weights_h2\"]\n")
            changed = True
            continue
        if "self.bias_h2 = np.zeros(" in line:
            new_src.append("        self.bias_h2 = initial_weights[\"bias_h2\"]\n")
            changed = True
            continue
        if "self.weights_out = np.random.randn" in line:
            new_src.append("        self.weights_out = initial_weights[\"weights_out\"]\n")
            changed = True
            continue
        if "self.bias_out = np.zeros(" in line:
            new_src.append("        self.bias_out = initial_weights[\"bias_out\"]\n")
            changed = True
            continue
        new_src.append(line)

    if changed:
        cell["source"] = new_src
    return changed


def patch_trainable_gated_perceptron_cell(cell: dict) -> bool:
    """Atualiza a classe TrainableGatedPerceptron para receber pesos/bias por parâmetro."""
    if cell.get("cell_type") != "code":
        return False
    src = cell.get("source", [])
    if not any("class TrainableGatedPerceptron:" in line for line in src):
        return False

    changed = False
    new_src = []
    for line in src:
        if "def __init__(self, num_inputs):" in line:
            new_src.append("    def __init__(self, weights, bias):\n")
            changed = True
            continue
        if "self.weights = np.random.randn(num_inputs)" in line:
            new_src.append("        self.weights = np.array(weights, dtype=float)\n")
            changed = True
            continue
        if "self.bias = np.random.randn()" in line:
            new_src.append("        self.bias = float(bias)\n")
            changed = True
            continue
        new_src.append(line)
    if changed:
        cell["source"] = new_src
    return changed


def patch_gated_mlp_cell(cell: dict) -> bool:
    """Atualiza a classe GatedMLP para usar pesos por parâmetro e neurônios H2 com pesos/bias providos."""
    if cell.get("cell_type") != "code":
        return False
    src = cell.get("source", [])
    if not any("class GatedMLP:" in line for line in src):
        return False

    changed = False
    new_src = []
    for line in src:
        if "def __init__(self, input_size=3, h1_size=5, h2_size=4, output_size=1):" in line:
            new_src.append("    def __init__(self, initial_weights, input_size=3, h1_size=5, h2_size=4, output_size=1):\n")
            changed = True
            continue
        if "self.weights_h1 = np.random.randn(input_size, h1_size)" in line:
            new_src.append("        self.weights_h1 = initial_weights[\"weights_h1\"]\n")
            changed = True
            continue
        if "self.bias_h1 = np.zeros(h1_size)" in line:
            new_src.append("        self.bias_h1 = initial_weights[\"bias_h1\"]\n")
            changed = True
            continue
        if "self.hidden_layer_2 = [TrainableGatedPerceptron(h1_size) for _ in range(h2_size)]" in line:
            new_src.append(
                "        self.hidden_layer_2 = [TrainableGatedPerceptron(weights=initial_weights[\"weights_h2\"][:, i], bias=initial_weights[\"bias_h2\"][i]) for i in range(h2_size)]\n"
            )
            changed = True
            continue
        if "self.weights_out = np.random.randn(h2_size, output_size)" in line:
            new_src.append("        self.weights_out = initial_weights[\"weights_out\"]\n")
            changed = True
            continue
        if "self.bias_out = np.zeros(output_size)" in line:
            new_src.append("        self.bias_out = initial_weights[\"bias_out\"]\n")
            changed = True
            continue
        new_src.append(line)
    if changed:
        cell["source"] = new_src
    return changed


def patch_smart_mlp_cell(cell: dict) -> bool:
    """Atualiza a classe SmartMLP para receber pesos por parâmetro."""
    if cell.get("cell_type") != "code":
        return False
    src = cell.get("source", [])
    if not any("class SmartMLP:" in line for line in src):
        return False

    changed = False
    new_src = []
    for line in src:
        if "def __init__(self, input_size=3, h1_size=5, h2_size=4, output_size=1):" in line:
            new_src.append("    def __init__(self, initial_weights, input_size=3, h1_size=5, h2_size=4, output_size=1):\n")
            changed = True
            continue
        if "self.weights_h1 = np.random.randn(input_size, h1_size)" in line:
            new_src.append("        self.weights_h1 = initial_weights[\"weights_h1\"]\n")
            changed = True
            continue
        if "self.bias_h1 = np.zeros(h1_size)" in line:
            new_src.append("        self.bias_h1 = initial_weights[\"bias_h1\"]\n")
            changed = True
            continue
        if "self.weights_h2 = np.random.randn(h1_size, h2_size)" in line:
            new_src.append("        self.weights_h2 = initial_weights[\"weights_h2\"]\n")
            changed = True
            continue
        if "self.bias_h2 = np.zeros(h2_size)" in line:
            new_src.append("        self.bias_h2 = initial_weights[\"bias_h2\"]\n")
            changed = True
            continue
        if "self.weights_out = np.random.randn(h2_size, output_size)" in line:
            new_src.append("        self.weights_out = initial_weights[\"weights_out\"]\n")
            changed = True
            continue
        if "self.bias_out = np.zeros(output_size)" in line:
            new_src.append("        self.bias_out = initial_weights[\"bias_out\"]\n")
            changed = True
            continue
        new_src.append(line)
    if changed:
        cell["source"] = new_src
    return changed


def patch_instantiations(cell: dict) -> bool:
    """Atualiza as instâncias para usar generate_initial_weights() e passar initial_weights."""
    if cell.get("cell_type") != "code":
        return False
    src = cell.get("source", [])
    changed = False
    new_src = []

    i = 0
    while i < len(src):
        line = src[i]
        if "standard_mlp = StandardMLP()" in line:
            new_src.append("initial_weights = generate_initial_weights()\n")
            new_src.append("standard_mlp = StandardMLP(initial_weights=initial_weights)\n")
            changed = True
            i += 1
            continue
        if "mlp = GatedMLP()" in line:
            new_src.append("initial_weights = generate_initial_weights()\n")
            new_src.append("mlp = GatedMLP(initial_weights=initial_weights)\n")
            changed = True
            i += 1
            continue
        if "SmartMLP()" in line and "=" in line:
            # Substitui qualquer instância de SmartMLP sem parâmetros
            before, sep, after = line.partition("SmartMLP()")
            new_line = before + "SmartMLP(initial_weights=generate_initial_weights())" + after
            new_src.append(new_line)
            changed = True
            i += 1
            continue
        new_src.append(line)
        i += 1

    if changed:
        cell["source"] = new_src
    return changed


def main():
    if not NB_PATH.exists():
        raise FileNotFoundError(f"Notebook não encontrado: {NB_PATH}")

    with NB_PATH.open("r", encoding="utf-8") as f:
        nb = json.load(f)

    cells = nb.get("cells", [])

    # 1) Inserir função generate_initial_weights
    cells = insert_generate_initial_weights_cell(cells)

    # 2) Patches nas classes
    total_changes = 0
    for cell in cells:
        if patch_standard_mlp_cell(cell):
            total_changes += 1
        if patch_trainable_gated_perceptron_cell(cell):
            total_changes += 1
        if patch_gated_mlp_cell(cell):
            total_changes += 1
        if patch_smart_mlp_cell(cell):
            total_changes += 1
        if patch_instantiations(cell):
            total_changes += 1

    nb["cells"] = cells

    with NB_PATH.open("w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)

    print(f"Patch aplicado. Células alteradas/atualizadas: {total_changes}")


if __name__ == "__main__":
    main()