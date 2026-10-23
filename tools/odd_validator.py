#!/usr/bin/env python3
"""Validador de conformidade do protocolo ODD e tags metodologicas.

Verifica:
1. Presenca das 7 secoes canonicas de Grimm et al. (2020)
2. Mapeamento de submodelos (Implemented in:)
3. Ausencia de tags bloqueantes [DECISION NEEDED]
4. Rastreabilidade de [ASSUMPTION] no decision-log.md
"""

from pathlib import Path
import re
import sys

CANONICAL_SECTIONS = [
    "1. Purpose",
    "2. Entities, State Variables, and Scales",
    "3. Process Overview and Scheduling",
    "4. Design Concepts",
    "5. Initialization",
    "6. Input Data",
    "7. Submodels",
]


def check_sections(content: str) -> list[str]:
    """Retorna secoes canonicas ausentes no ODD."""
    lower_content = content.lower()
    return [sec for sec in CANONICAL_SECTIONS if sec.lower() not in lower_content]


def check_submodel_links(content: str) -> list[str]:
    """Verifica se cada submodelo possui ligacao com codigo."""
    submodels = re.findall(r"###\s*7\.\d+\.\s*([^\n]+)", content)
    implemented = re.findall(r"-\s*\*\*Implemented in:\*\*", content)
    if len(implemented) < len(submodels):
        missing_count = len(submodels) - len(implemented)
        return [f"{missing_count} submodelo(s) sem campo 'Implemented in:'"]
    return []


def check_blocking_tags(content: str) -> list[str]:
    """Verifica presenca de tags [DECISION NEEDED] que impedem simulacao."""
    tags = re.findall(r"\[DECISION NEEDED\][^\n]+", content)
    return [f"Tag bloqueante encontrada: {tag.strip()}" for tag in tags]


def check_assumptions(odd_content: str, log_content: str | None) -> list[str]:
    """Verifica se cada [ASSUMPTION] possui entrada correspondente no decision-log."""
    assumed_ids = re.findall(r"\[ASSUMPTION\][^(]+\(decision-log\s*#(\d+)\)", odd_content)
    if not assumed_ids:
        return []

    if log_content is None:
        return [f"{len(assumed_ids)} [ASSUMPTION] citadas, mas 'decision-log.md' nao existe."]

    missing_ids = [
        aid for aid in assumed_ids
        if not re.search(rf"\|\s*{aid}\s*\|", log_content)
    ]
    return [f"[ASSUMPTION] cita decision-log #{aid}, mas entrada nao existe no log." for aid in missing_ids]


def validate_model_odd(model_dir: Path) -> list[str]:
    """Executa todas as verificacoes do ODD e retorna lista de violacoes."""
    odd_path = model_dir / "odd.md"
    if not odd_path.exists():
        return [f"Arquivo '{odd_path}' nao encontrado."]

    odd_content = odd_path.read_text(encoding="utf-8")
    log_path = model_dir / "decision-log.md"
    log_content = log_path.read_text(encoding="utf-8") if log_path.exists() else None

    issues = []
    missing_secs = check_sections(odd_content)
    if missing_secs:
        issues.append(f"Secoes canonicas ausentes: {', '.join(missing_secs)}")

    issues.extend(check_submodel_links(odd_content))
    issues.extend(check_blocking_tags(odd_content))
    issues.extend(check_assumptions(odd_content, log_content))
    return issues


def main() -> None:
    target_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    issues = validate_model_odd(target_dir)

    print(f"\nAuditoria ODD: {target_dir.resolve()}")
    print("=" * 60)

    if issues:
        print("Problemas identificados:")
        for issue in issues:
            print(f"  [FALHA] {issue}")
        sys.exit(1)

    print("Status: 7 secoes presentes, submodelos mapeados, zero tags bloqueantes.")
    print("Veredito: Aprovado.")


if __name__ == "__main__":
    main()
