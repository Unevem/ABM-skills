---
description: Mandatory pre-commit audit and verification checks before staging or committing ABM code or documentation.
trigger: always_on
---

# Rule: Mandatory Pre-Commit Review Gate

## Objective
Prevent flawed, unverified, drifted, or theoretically hallucinated simulation code and documentation from ever entering the Git history.

---

## The Rule

Before proposing or executing any `git commit` or moving any stage to completion, the AI agent **must run the `abm-reviewer` audit protocol** on all modified files and present the verification verdict to the researcher.

Committing code with known defects, unexecuted config options, parameter range mismatches, or unverified tasks is **strictly forbidden**.

---

## Pre-Commit Verification Checklist

The agent must verify and report on these 6 checkpoints:

1. **Clean Test Suite:**
   - Execute `pytest tests/ -v` using the project's virtual environment.
   - All tests must pass with 0 failures and 0 unhandled warnings.
2. **Configuration Completeness:**
   - Confirm that all seeds, scenarios, and sweeps defined in `experiment-config.yaml` are actually executed by `experiments.py`.
   - Confirm that output CSVs include metadata columns (`seed`, `scenario`, etc.).
3. **Range Consistency Across 4 Layers:**
   - ODD Table A.1 == YAML config == Python `__init__` boundary validation == Test assertions.
4. **Decision Log & Tag Audit:**
   - Zero `[DECISION NEEDED]` in code.
   - Every `[ASSUMPTION]` has a corresponding entry in `decision-log.md`.
   - No fabricated consensus: all entries marked `researcher` reflect actual user answers.
   - All technical dependency/API changes are logged as `agent (technical)`.
5. **No Phantom Tasks:**
   - Every item marked `[x]` in `TASKS.md` has verifiable files on disk and recorded researcher approval.
6. **Empirical Honesty:**
   - Simulation results (e.g., cluster counts) must be reported exactly as computed. Any fringe clusters or deviations from canonical narratives must be noted, not hidden.

---

## Commit Gate Protocol

If any check fails:
1. Halt the commit.
2. List the specific discrepancies in a checkpoint report.
3. Fix the discrepancies or escalate blocking theoretical decisions to `TASKS.md` under `## Decisions Needed`.
4. Only when all 6 checkpoints pass may the agent suggest a Git commit to the researcher.
