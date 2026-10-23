# ABMforAI: Scientific Agent-Based Modeling with AI Assistants

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Mesa: 3.x](https://img.shields.io/badge/Mesa-3.5%2B-orange.svg)](https://mesa.readthedocs.io/)

Guidelines, templates, CLI tools, and agent skills designed to empower domain researchers (in social sciences, biology, economics, and ecology) to design, document, implement, and verify rigorous, reproducible computational simulations in Python without undocumented theoretical assumptions.

---

## The Core Problem

Agent-Based Modeling (ABM) is an essential methodology for studying complex emergent phenomena. However, domain researchers frequently encounter a steep software engineering hurdle, while generic AI assistants exhibit severe failure modes when left unconstrained:
- **Theoretical Hallucination:** Silently inventing utility functions, threshold rules, or equations without domain grounding.
- **Config Drift & Phantom Sweeps:** Defining parameter sweeps in YAML configurations that are never executed in simulation scripts.
- **Confirmation Bias:** Filtering out or smoothing over fringe empirical clusters to match canonical textbook narratives.
- **Arbitrary Task Completion:** Unilaterally declaring work "done" without running tests or producing verifiable proof.

**ABMforAI** solves this through **evidence-gated copiloting**: the researcher owns all theoretical and behavioral decisions; the AI provides software craftsmanship under strict, non-negotiable guardrails.

---

## Core Directives

1. **Never Invent Behavioral Rules Silently:** Missing theoretical details trigger an immediate halt. Unresolved questions are tagged `[DECISION NEEDED]` and block dependent implementation.
2. **Ground Every Implementation in ODD:** All agent classes, attributes, state transitions, and schedules trace directly to the standardized **ODD (Overview, Design Concepts, Details)** protocol ([Grimm et al., 2020](https://doi.org/10.18564/jasss.4259)).
3. **Evidence-Gated Completion (Grill-Me Protocol):** Tasks in `TASKS.md` cannot be marked completed without verifiable proof on disk (passing test suites, generated CSV/PNG outputs) and explicit researcher confirmation.
4. **CLI-Mediated Task Governance:** The AI cannot edit `TASKS.md` directly with file tools. State transitions must be commanded via `python tools/tasks.py`, enforcing human review gates.
5. **Strict Reproducibility:** Explicit pseudo-random number generator (RNG) seeding, parameter externalization via YAML, and automated invariance testing across four layers (ODD, YAML, Python, Tests).

---

## The 4-Stage Operational Workflow

The methodology enforces a gated, sequential progression:

```
[1. Elicit] ---------> [2. Formalize] -------> [3. Simulate] -------> [4. Verify]
Diagnostic Interview     ODD Protocol &         Modular Python/Mesa    Invariants, Tests &
(12 Dimensions)          Decision Log           Implementation         Multi-Seed Sweeps
```

1. **Stage 1: Elicit (Diagnostic Interview):** Socratic interview exploring entities, topology, behavioral rules, temporal scales, and observed metrics without generating code.
2. **Stage 2: Formalize (ODD Protocol):** Generates `odd.md`, `model-specification.md`, and `decision-log.md`. Any provisional choice accepted by the researcher is logged as `[ASSUMPTION] (decision-log #N)`.
3. **Stage 3: Simulate (Modular Python Implementation):** Implements `agents.py`, `model.py`, `metrics.py`, and `experiments.py` using Mesa 3.5+. Behavioral methods feature inline `# ODD: Section X.Y` annotations.
4. **Stage 4: Verify (Invariants & Experiments):** Executes automated pytest verification suites (V1 to V8), runs multi-seed baselines and parameter sweeps, and generates empirical verification reports.

---

## Repository Architecture

```text
ABMforAI/
├── README.md                          # Project presentation and usage guide
├── LICENSE                            # MIT License
├── CITATION.cff                       # Formal academic citation metadata
├── AGENTS.md                          # Universal governance rules for AI coding assistants
│
├── .agents/
│   ├── rules/                         # Workspace governance rules
│   │   ├── human-review.md            # Mandatory pause triggers for theoretical choices
│   │   ├── no-undocumented-assumptions.md # Strict tagging rules ([DECISION NEEDED] / [ASSUMPTION])
│   │   ├── task-management.md         # Task lifecycle and CLI mediation rules
│   │   ├── reproducibility.md         # Random seed control and numerical stability
│   │   ├── code-organization.md       # Modular file separation and Clean Code conventions
│   │   └── pre-commit-review.md       # 6-point pre-commit verification checklist
│   │
│   └── skills/
│       ├── abm-modeler/               # Self-contained modeling skill
│       │   ├── SKILL.md               # Workflow orchestrator
│       │   ├── references/            # Stage runbooks (stage-1 to stage-4) and guardrails
│       │   └── resources/             # Templates (ODD, spec, decision log, config)
│       └── abm-reviewer/              # Adversarial audit skill
│           └── SKILL.md               # Pre-commit multi-layer verification auditor
│
├── tools/                             # Clean, zero-dependency validation CLI tools
│   ├── tasks.py                       # CLI manager for TASKS.md with disk evidence checking
│   ├── odd_validator.py               # Static linter for ODD protocol completeness and tags
│   ├── verify_model.py                # Automated pytest runner and config verification
│   └── scaffold_abm.py                # New model project scaffolding tool
│
├── examples/
│   └── opinion-dynamics/              # Canonical Golden Example (Deffuant Bounded Confidence)
│       ├── README.md                  # Model documentation and execution guide
│       ├── TASKS.md                   # Model-level living task board
│       ├── specification.md           # Formalized elicitation interview
│       ├── odd.md                     # Full 7-section ODD protocol
│       ├── decision-log.md            # Recorded theoretical consensus (#1 to #12)
│       ├── experiment-config.yaml     # Baseline controls, scenarios, and sweeps
│       ├── agents.py                  # OpinionAgent with ODD annotations
│       ├── model.py                   # OpinionModel with Mesa 3.5+ AgentSet API
│       ├── metrics.py                 # Clustering metrics and trajectory plots
│       ├── experiments.py             # Scenario runner and batch parameter sweep
│       ├── verification-report.md     # Empirical audit and test results
│       ├── tests/                     # 8/8 automated verification test suite (V1-V8)
│       └── output/                    # Generated CSVs and publication figures
│
└── docs/
    └── development-audit-report.md    # Empirical failure modes post-mortem and audit report
```

---

## CLI Tools Ecosystem

All tools in `tools/` follow Clean Code and YAGNI principles (single-purpose functions, function dispatching, under 95 lines each):

### 1. Task Governance (`tools/tasks.py`)
Enforces the rule that AI cannot directly edit `TASKS.md` with file tools. Requires disk evidence before completing tasks.
```bash
# Initialize a new TASKS.md
python tools/tasks.py init --path models/my-model/TASKS.md

# Add a pending task or decision needed
python tools/tasks.py add "Determine boundary conditions" --section "Decisions Needed"

# Complete a task with mandatory evidence verification on disk
python tools/tasks.py complete "Implement agent step" --evidence models/my-model/agents.py
```

### 2. ODD Static Linter (`tools/odd_validator.py`)
Checks markdown files for ODD protocol compliance:
- Validates the presence of all 7 mandatory ODD sections.
- Ensures all submodels defined in Section 7 have anchors in Section 2.
- Flags any blocking `[DECISION NEEDED]` tags.
- Verifies that all `[ASSUMPTION]` tags link to entries in `decision-log.md`.
```bash
python tools/odd_validator.py examples/opinion-dynamics/
```

### 3. Model Verifier (`tools/verify_model.py`)
Runs the model verification test suite and checks for configuration files:
```bash
python tools/verify_model.py --model-dir examples/opinion-dynamics/
```

### 4. ABM Project Scaffolder (`tools/scaffold_abm.py`)
Scaffolds a complete, ready-to-use ABM directory structure with ODD template, decision log, experiment configuration, requirements, and an initialized `TASKS.md`:
```bash
python tools/scaffold_abm.py sugarscape-model --output-dir models/
```

---

## Quickstart: Using ABMforAI in Your Project

### 1. Installation

> [!NOTE]
> The `abmforai` npm package release is currently pending publication. You can install directly from GitHub using `npx github:Unevem/ABMforAI setup` or `npx skills add Unevem/ABMforAI`. Once published to npm, `npx abmforai setup` will become the primary shortcut.

#### Option A: Direct via GitHub npx (Recommended, no clone required)
Inside your simulation project directory, run:
```bash
npx github:Unevem/ABMforAI setup
```

#### Option B: Via Skills CLI (Universal skills package manager)
```bash
npx skills add Unevem/ABMforAI
```

#### Option C: Once published to the npm Registry
```bash
npx abmforai setup
```

All methods automatically install:
- `.agents/rules/`: Non-negotiable AI guardrails and verification checks.
- `.agents/skills/`: The `abm-modeler` and `abm-reviewer` skills.
- `AGENTS.md`: Core directives preventing theoretical hallucinations.
- `tools/`: Zero-dependency validation and task governance CLIs.

To verify that all components are correctly configured, run:
```bash
python tools/verify_model.py
# or when installed via npm:
npx abmforai doctor
```

---

### 2. Prompting Your AI Assistant
Open your AI coding assistant (Google Antigravity, Cursor, Claude Code, or GitHub Copilot) in your project directory and prompt:
```text
I want to build an agent-based model to study [describe your phenomenon]. 
Please read .agents/skills/abm-modeler/SKILL.md and begin with Stage 1: Elicit.
```

---

### 3. Creating a New Model
Scaffold an organized model directory with pre-configured ODD template, decision log, and task board:
```bash
python tools/scaffold_abm.py my-model
```

---

## Reference Implementation: Opinion Dynamics

The repository includes a complete reference model in `examples/opinion-dynamics/` demonstrating the full lifecycle:
- **Theory:** Deffuant bounded confidence model with continuous opinions in $[0.0, 1.0]$.
- **Mesa 3.5+ Implementation:** Modern `AgentSet.shuffle_do("step")` scheduling, explicit `rng` seeding, and vector-capable `DataCollector`.
- **Empirical Revision Tracking:** Documents real-world emergent nuances (minor fringe clusters at $\epsilon = 0.2$) with formal revision notes instead of data filtering.
- **Verification Suite:** 8 automated invariant checks passing with zero warnings in 2.7s.

To run the example:
```bash
cd examples/opinion-dynamics
pip install -r requirements.txt
pytest tests/ -v
python experiments.py
```

Generated outputs will be saved to `examples/opinion-dynamics/output/` including trajectory plots, opinion histograms, and batch sweep CSVs.

---

## Citation & Academic Use

This framework and its accompanying empirical study are designed for academic computational research. If you use ABMforAI in your simulations or publications, please cite:

```bibtex
@software{abmforai2026,
  title = {ABMforAI: Rigorous, Evidence-Based Agent-Based Modeling Guidelines and Skills for AI Assistants},
  author = {ABMforAI Contributors},
  year = {2026},
  version = {1.0.0},
  url = {https://github.com/Unevem/ABMforAI}
}
```

See also [CITATION.cff](CITATION.cff) for complete CFF metadata.

---

## License

This project is licensed under the [MIT License](LICENSE) - free for academic, scientific, and commercial use.
