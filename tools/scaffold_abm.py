#!/usr/bin/env python3
"""Inicializador simples de novos modelos ABM com governanca pronta.

Aplica Clean Code e YAGNI:
1. Copia templates formais (ODD, Specification, Decision-Log, YAML)
2. Cria estrutura de codigo modular e testes
3. Inicializa o TASKS.md contratual via tools/tasks.py
"""

import argparse
from pathlib import Path
import shutil
import subprocess
import sys

DEFAULT_REQUIREMENTS = """mesa>=3.5.0,<4.0.0
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
pytest>=7.0.0
networkx>=3.0
pyyaml>=6.0.0
"""

CODE_STUBS = {
    "agents.py": '"""Definicoes de agentes e submodelos de comportamento."""\n\nimport mesa\n',
    "model.py": '"""Controlador do modelo, inicializacao e coleta de dados."""\n\nimport mesa\n',
    "metrics.py": '"""Funcoes de observacao, agregacoes estatisticas e graficos."""\n',
    "experiments.py": '"""Executor de cenarios, varredura de parametros e exportador CSV."""\n',
    "tests/__init__.py": "",
    "tests/test_model.py": '"""Suite de verificacao automatizada (Checks V1 a V8)."""\n\nimport pytest\n',
}


def scaffold_model(model_name: str, target_dir: Path) -> Path:
    """Cria a estrutura de diretorios e arquivos do modelo a partir dos templates."""
    if target_dir.exists():
        sys.exit(f"Erro: Diretorio '{target_dir}' ja existe.")

    target_dir.mkdir(parents=True, exist_ok=True)
    repo_root = Path(__file__).resolve().parent.parent
    resources_dir = repo_root / ".agents" / "skills" / "abm-modeler" / "resources"

    # 1. Copia templates formais
    template_map = {
        "model-specification.md": "model-specification.md",
        "odd-template.md": "odd.md",
        "decision-log.md": "decision-log.md",
        "experiment-config.yaml": "experiment-config.yaml",
    }
    for src_name, dest_name in template_map.items():
        src_path = resources_dir / src_name
        if src_path.exists():
            shutil.copy2(src_path, target_dir / dest_name)

    # 2. Inicializa requirements.txt com versoes pinadas
    (target_dir / "requirements.txt").write_text(DEFAULT_REQUIREMENTS, encoding="utf-8")

    # 3. Cria estrutura e stubs de codigo
    for rel_path, stub_content in CODE_STUBS.items():
        dest = target_dir / rel_path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(stub_content, encoding="utf-8")

    # 4. Inicializa TASKS.md via tools/tasks.py
    tasks_script = repo_root / "tools" / "tasks.py"
    tasks_file = target_dir / "TASKS.md"
    subprocess.run([sys.executable, str(tasks_script), "--path", str(tasks_file), "init"], check=True)

    # 5. Cria README basico
    readme_content = f"# Modelo: {model_name}\n\nInicializado via scaffold_abm.py seguindo o protocolo ODD e ABMforAI.\n"
    (target_dir / "README.md").write_text(readme_content, encoding="utf-8")

    return target_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold simples de novo modelo ABM")
    parser.add_argument("model_name", help="Nome do novo modelo (ex: market-dynamics)")
    parser.add_argument("--output-dir", default=".", help="Diretorio pai de destino (padrao: diretorio atual)")
    args = parser.parse_args()

    dest_dir = Path(args.output_dir) / args.model_name
    created = scaffold_model(args.model_name, dest_dir)
    print(f"\nModelo '{args.model_name}' inicializado com sucesso em:\n{created.resolve()}")


if __name__ == "__main__":
    main()
