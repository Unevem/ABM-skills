---
description: Architecture, file separation, and coding conventions for Python and Mesa ABM components.
trigger: model_decision
---

# Rule: Code Organization & Architecture

## Objective
Enforce clean, decoupled separation of concerns so that researchers and other AI agents can inspect, test, and modify individual parts of an ABM without breaking unrelated components.

---

## Standard Project Layout

Every ABM project developed under this guideline must adhere to the following file layout:

```text
my-abm-project/
├── README.md              # High-level overview and run instructions
├── odd.md                 # Full scientific ODD protocol specification
├── decision-log.md        # Log of theoretical consensus and approved hypotheses
├── experiment-config.yaml # Parameter definitions and scenario sweeps
├── requirements.txt       # Dependencies (e.g., mesa>=3.0.0, numpy, matplotlib, pytest)
├── agents.py              # Agent classes, internal states, and individual behaviors
├── model.py               # Global environment, spatial grid/network, scheduling, collector
├── experiments.py         # Batch runner, scenario execution, parameter sweeps
├── metrics.py             # Metric calculations, summary tables, and plotting routines
└── tests/
    ├── __init__.py
    └── test_model.py      # Stage 4 checks: seed determinism, invariants, outputs
```

---

## Architectural Principles

1. **`agents.py` (Micro-Level Dynamics):**
   - Contains agent classes inheriting from `mesa.Agent` (or a base object if pure Python).
   - In modern Mesa 3.x: `super().__init__(model)` (do not force manual unique IDs if managed by the framework).
   - Agent methods should represent behavioral actions (e.g., `sense()`, `decide()`, `interact()`, `move()`).
   - Agents should not directly manipulate global simulation orchestration or batch logging.

2. **`model.py` (Macro-Level Orchestration):**
   - Contains the simulation controller inheriting from `mesa.Model`, calling `super().__init__(seed=seed)`.
   - Manages the space (prefer `mesa.discrete_space` cell spaces when available; legacy `mesa.space` grids, `ContinuousSpace`, or a NetworkX graph otherwise). Neighborhood, torus, and capacity are ODD decisions.
   - Mesa 3 has no schedulers: express the ODD scheduling with `AgentSet` operations (`self.agents.shuffle_do("step")`, `self.agents.do(...)`, two-phase for synchronous updates). The choice is a theoretical decision.
   - Initializes and triggers data collectors (`mesa.DataCollector`).

3. **`experiments.py` (In Silico Laboratory):**
   - Script or module to run single runs or parameter sweeps (`batch_run`).
   - Accepts command-line parameters or reads `experiment-config.yaml`.
   - Saves raw metrics to CSV/Parquet for independent statistical analysis.

4. **`metrics.py` (Analysis & Visualization):**
   - Clean, reproducible plotting routines (e.g., Matplotlib/Seaborn) or interactive visualization (e.g., Solara in Mesa 3.x).
   - Keeps presentation logic out of `model.py`.
