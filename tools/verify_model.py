#!/usr/bin/env python3
"""Runner de verificacao automatizada de integridade e testes do modelo ABM.

Aplica Clean Code e YAGNI:
1. Executa a suite de testes pytest no diretorio tests/
2. Verifica presenca e consistencia de experiment-config.yaml
"""

import argparse
from pathlib import Path
import subprocess
import sys


def run_tests(model_dir: Path) -> tuple[int, str]:
    """Executa a suite pytest dentro da pasta de testes do modelo."""
    tests_dir = model_dir / "tests"
    if not tests_dir.exists():
        return 1, f"Diretorio de testes '{tests_dir}' nao encontrado."

    cmd = [sys.executable, "-m", "pytest", str(tests_dir), "-v"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout or result.stderr
    return result.returncode, output.strip()


def check_config(model_dir: Path) -> list[str]:
    """Verifica se o arquivo de configuracao basico existe."""
    config_path = model_dir / "experiment-config.yaml"
    if not config_path.exists():
        return [f"Aviso: '{config_path.name}' nao encontrado."]
    return []


def verify_model(model_dir: Path) -> int:
    """Orquestra a verificacao do modelo e imprime relatorio conciso."""
    print(f"\nVerificacao do Modelo: {model_dir.resolve()}")
    print("=" * 60)

    # 1. Checagem de configuracao
    warnings = check_config(model_dir)
    for w in warnings:
        print(f"  {w}")

    # 2. Execucao dos testes
    code, test_output = run_tests(model_dir)
    print("\nExecucao dos Testes (pytest):")
    print("-" * 60)
    print(test_output)
    print("-" * 60)

    if code != 0:
        print("\nVeredito: FALHA - Testes automatizados falharam.")
        return 1

    print("\nVeredito: APROVADO - Todos os testes de integridade passaram.")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Runner de verificacao automatizada de modelo ABM.")
    parser.add_argument("path", nargs="?", default=".", help="Diretorio do modelo (padrao: .)")
    parser.add_argument("--model-dir", dest="model_dir", default=None, help="Caminho do diretorio do modelo")
    args = parser.parse_args()
    target_dir = Path(args.model_dir if args.model_dir else args.path)
    exit_code = verify_model(target_dir)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()

