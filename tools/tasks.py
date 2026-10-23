#!/usr/bin/env python3
"""CLI simples para gerenciar TASKS.md sem edicao direta de texto.

Operacoes suportadas:
  python tools/tasks.py init [--path TASKS.md]
  python tools/tasks.py add "descricao" [--section Pending|In Progress|Decisions Needed]
  python tools/tasks.py complete "trecho_da_tarefa" --evidence <arquivo> [--approver researcher]
"""

import argparse
from datetime import date
from pathlib import Path
import sys

TEMPLATE = """# Tasks

## In Progress

## Pending

## Decisions Needed

## Completed
"""


def cmd_init(args: argparse.Namespace) -> None:
    path = Path(args.path)
    if path.exists():
        print(f"Arquivo ja existe: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(TEMPLATE, encoding="utf-8")
    print(f"Criado: {path}")


def cmd_add(args: argparse.Namespace) -> None:
    path = Path(args.path)
    if not path.exists():
        sys.exit(f"Arquivo nao encontrado: {path}")

    section_header = f"## {args.section}"
    content = path.read_text(encoding="utf-8")
    if section_header not in content:
        sys.exit(f"Secao '{section_header}' nao encontrada em {path}")

    new_line = f"- [ ] {args.text}\n"
    parts = content.split(section_header, 1)
    updated = f"{parts[0]}{section_header}\n{new_line}{parts[1].lstrip('\n')}"
    path.write_text(updated, encoding="utf-8")
    print(f"Adicionado em '{args.section}': {args.text}")


def cmd_complete(args: argparse.Namespace) -> None:
    path = Path(args.path)
    if not path.exists():
        sys.exit(f"Arquivo nao encontrado: {path}")

    # Valida que o arquivo de evidencia realmente existe antes de concluir
    evidence_path = Path(args.evidence)
    if not evidence_path.exists() and not (path.parent / evidence_path).exists():
        sys.exit(f"Erro: o arquivo de evidencia '{args.evidence}' nao existe no disco.")

    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()

    # Localiza a tarefa pelo trecho do texto
    target_idx = None
    for idx, line in enumerate(lines):
        if line.startswith("- [ ]") and args.task.lower() in line.lower():
            target_idx = idx
            break

    if target_idx is None:
        sys.exit(f"Tarefa contendo '{args.task}' nao encontrada em estado pendente (- [ ]).")

    raw_text = lines.pop(target_idx).replace("- [ ]", "").strip()
    today = date.today().isoformat()
    completed_entry = f"- [x] {raw_text} (evidence: {args.evidence}; approved by {args.approver} {today})"

    # Insere imediatamente apos o cabecalho ## Completed
    try:
        completed_sec_idx = lines.index("## Completed")
        lines.insert(completed_sec_idx + 1, completed_entry)
    except ValueError:
        lines.extend(["", "## Completed", completed_entry])

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Concluido: {completed_entry}")


def cmd_remove(args: argparse.Namespace) -> None:
    path = Path(args.path)
    if not path.exists():
        sys.exit(f"Arquivo nao encontrado: {path}")

    content = path.read_text(encoding="utf-8")
    lines = [l for l in content.splitlines() if not (l.startswith("- [") and args.task.lower() in l.lower())]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Removido: {args.task}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gerenciador simples de TASKS.md")
    parser.add_argument("--path", default="TASKS.md", help="Caminho do arquivo TASKS.md (padrao: TASKS.md)")
    sub = parser.add_subparsers(dest="subcommand", required=True)

    # init
    p_init = sub.add_parser("init", help="Cria um TASKS.md vazio com as 4 secoes")
    p_init.set_defaults(func=cmd_init)

    # add
    p_add = sub.add_parser("add", help="Adiciona uma tarefa")
    p_add.add_argument("text", help="Descricao da tarefa")
    p_add.add_argument(
        "--section",
        default="Pending",
        choices=["Pending", "In Progress", "Decisions Needed"],
        help="Secao de destino (padrao: Pending)",
    )
    p_add.set_defaults(func=cmd_add)

    # complete
    p_comp = sub.add_parser("complete", help="Marca uma tarefa como concluida")
    p_comp.add_argument("task", help="Trecho do texto da tarefa a concluir")
    p_comp.add_argument("--evidence", required=True, help="Caminho do arquivo que comprova a conclusao")
    p_comp.add_argument("--approver", default="researcher", help="Aprovador (padrao: researcher)")
    p_comp.set_defaults(func=cmd_complete)

    # remove
    p_rem = sub.add_parser("remove", help="Remove uma tarefa pelo trecho do texto")
    p_rem.add_argument("task", help="Trecho do texto da tarefa a remover")
    p_rem.set_defaults(func=cmd_remove)

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
